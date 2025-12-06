import rclpy
from rclpy.node import Node
import numpy as np
import struct
from sensor_msgs.msg import PointCloud2
from geometry_msgs.msg import PointStamped
from tf2_ros import Buffer, TransformListener
import tf2_geometry_msgs
from std_srvs.srv import Empty  # Service type for reset


class ClosestPredictedPoint(Node):
    def __init__(self):
        super().__init__("closest_predicted_point")

        # Subscribe to latest predicted trajectory
        self.sub = self.create_subscription(
            PointCloud2,
            "/ball_latest_predicted_trajectory",
            self.pred_callback,
            10
        )

        # Publisher for the closest point
        self.closest_pub = self.create_publisher(
            PointStamped,
            "/ball_closest_predicted_point",
            1
        )

        # TF listener
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        # Service to reset trajectories
        self.reset_srv = self.create_service(Empty, "reset_closest_predicted_point", self.reset_callback)

        # Frame names
        self.wrist_frame = "wrist_3_link"
        self.ball_frame = "camera_color_optical_frame"  # input trajectory frame
        self.output_frame = "base_link"                 # NEW: output frame

        # Store last received cloud and precomputed closest point
        self.last_cloud = None
        self.computed_closest = None
        self.published_last = False

        # Trajectory counter
        self.trajectory_count = 0
        self.target_trajectory = 4  # Publish only on 5th valid trajectory

        self.get_logger().info("Closest predicted point node started.")

    def pointcloud2_to_xyz(self, cloud):
        pts = []
        data = cloud.data
        step = cloud.point_step
        for i in range(cloud.width):
            base = i * step
            x = struct.unpack_from('<f', data, base + 0)[0]
            y = struct.unpack_from('<f', data, base + 4)[0]
            z = struct.unpack_from('<f', data, base + 8)[0]
            pts.append([x, y, z])
        return np.array(pts, dtype=np.float32)

    def pred_callback(self, cloud_msg: PointCloud2):
        # Only consider this cloud if it has more than 1 point
        if cloud_msg.width <= 1:
            return

        # Increment trajectory counter for valid clouds only
        self.trajectory_count += 1
        self.get_logger().info(f"Received valid trajectory #{self.trajectory_count}")

        # Only compute/publish on the target trajectory
        if self.trajectory_count == self.target_trajectory:
            computed = self.compute_closest_point(cloud_msg)
            if computed is None:
                self.get_logger().warn("Failed to compute closest point for 5th trajectory.")
                return

            self.computed_closest = computed
            self.closest_pub.publish(self.computed_closest)
            self.published_last = True
            self.get_logger().info("Published closest point for the 5th trajectory.")

    def compute_closest_point(self, cloud_msg):
        # --- 1. Lookup wrist pose in ball frame ---
        try:
            tf = self.tf_buffer.lookup_transform(
                self.ball_frame,
                self.wrist_frame,
                rclpy.time.Time()
            )
            wrist_point = PointStamped()
            wrist_point.header.frame_id = self.wrist_frame
            wrist_point.point.x = wrist_point.point.y = wrist_point.point.z = 0.0
            wrist_in_ball = tf2_geometry_msgs.do_transform_point(wrist_point, tf)
            wrist_vec = np.array([
                wrist_in_ball.point.x,
                wrist_in_ball.point.y,
                wrist_in_ball.point.z
            ], dtype=np.float32)
        except Exception as e:
            self.get_logger().warn(f"TF lookup/transform failed: {e}")
            return None

        # --- 2. Extract predicted trajectory points ---
        pred_pts = self.pointcloud2_to_xyz(cloud_msg)
        if pred_pts.shape[0] <= 1:
            return None

        # --- 3. Find the closest point (in camera frame) ---
        diffs = pred_pts - wrist_vec
        dists = np.linalg.norm(diffs, axis=1)
        idx = np.argmin(dists)
        closest_point = pred_pts[idx]

        # --- 4. Create PointStamped in camera frame ---
        point_cam = PointStamped()
        point_cam.header = cloud_msg.header
        point_cam.point.x = float(closest_point[0])
        point_cam.point.y = float(closest_point[1])
        point_cam.point.z = float(closest_point[2])

        # --- 5. Transform the point to base_link (NEW) ---
        try:
            tf_to_base = self.tf_buffer.lookup_transform(
                self.output_frame,
                point_cam.header.frame_id,  # likely camera_color_optical_frame
                rclpy.time.Time()
            )
            point_base = tf2_geometry_msgs.do_transform_point(point_cam, tf_to_base)
            point_base.header.frame_id = self.output_frame
        except Exception as e:
            self.get_logger().warn(f"Failed to transform predicted point to base_link: {e}")
            return None

        return point_base

    def reset_callback(self, request, response):
        """Reset all trajectory histories and counters."""
        self.last_cloud = None
        self.computed_closest = None
        self.published_last = False
        self.trajectory_count = 0
        self.get_logger().info("Trajectory data reset via service call.")
        return response


def main(args=None):
    rclpy.init(args=args)
    node = ClosestPredictedPoint()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
