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
        self.reset_srv = self.create_service(
            Empty, "reset_closest_predicted_point", self.reset_callback
        )

        # Frames
        self.wrist_frame = "wrist_3_link"
        self.ball_frame = "camera_color_optical_frame"
        self.output_frame = "base_link"

        # Storage
        self.last_cloud = None
        self.computed_closest = None
        self.published_last = False

        # Only publish on 5th trajectory
        self.trajectory_count = 0
        self.target_trajectory = 5

        self.get_logger().info("Closest predicted point node started.")

    def pointcloud2_to_xyz(self, cloud):
        pts = []
        data = cloud.data
        step = cloud.point_step
        for i in range(cloud.width):
            base = i * step
            x = struct.unpack_from("<f", data, base + 0)[0]
            y = struct.unpack_from("<f", data, base + 4)[0]
            z = struct.unpack_from("<f", data, base + 8)[0]
            pts.append([x, y, z])
        return np.array(pts, dtype=np.float32)

    def pred_callback(self, cloud_msg: PointCloud2):

        if cloud_msg.width <= 1:
            self.published_last = False
            return

        self.trajectory_count += 1
        self.get_logger().info(f"Received valid trajectory #{self.trajectory_count}")

        if self.trajectory_count == self.target_trajectory:
            computed = self.compute_closest_point(cloud_msg)

            if computed is None:
                self.get_logger().warn("Failed to compute closest point on 5th trajectory.")
                return

            self.computed_closest = computed
            self.closest_pub.publish(self.computed_closest)
            self.published_last = True
            self.get_logger().info("Published closest point for 5th trajectory.")

    def compute_closest_point(self, cloud_msg):
        # --- 1. Wrist → ball frame transform ---
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
            self.get_logger().warn(f"TF lookup failed: {e}")
            return None

        # --- 2. Extract points ---
        pred_pts = self.pointcloud2_to_xyz(cloud_msg)
        if pred_pts.shape[0] <= 1:
            return None

        # --- 3. Filter points by Y range (0.30 → 0.65) ---
        y_mask = (pred_pts[:, 1] >= 0.30) & (pred_pts[:, 1] <= 0.65)
        pred_pts = pred_pts[y_mask]
        if pred_pts.shape[0] == 0:
            self.get_logger().warn("No points in Y range 0.30–0.65.")
            return None

        # --- 4. Filter by ≤ 1 meter distance from wrist ---
        dists = np.linalg.norm(pred_pts - wrist_vec, axis=1)
        close_mask = dists <= 1.0
        pred_pts = pred_pts[close_mask]
        if pred_pts.shape[0] == 0:
            self.get_logger().warn("No predicted points within 1 meter of the wrist.")
            return None

        # --- 5. Transform all remaining candidate points to base_link ---
        try:
            tf_to_base = self.tf_buffer.lookup_transform(
                self.output_frame,
                cloud_msg.header.frame_id,
                rclpy.time.Time()
            )
            points_base = []
            for p in pred_pts:
                pt = PointStamped()
                pt.header = cloud_msg.header
                pt.point.x, pt.point.y, pt.point.z = p
                pt_base = tf2_geometry_msgs.do_transform_point(pt, tf_to_base)
                points_base.append(pt_base)
        except Exception as e:
            self.get_logger().warn(f"Failed to transform points to base_link: {e}")
            return None

        # --- 6. Pick the closest point to wrist (already in base_link frame) ---
        dists_base = [np.linalg.norm(
            np.array([pt.point.x, pt.point.y, pt.point.z]) - wrist_vec
        ) for pt in points_base]
        closest_idx = int(np.argmin(dists_base))
        return points_base[closest_idx]


    def reset_callback(self, request, response):
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
