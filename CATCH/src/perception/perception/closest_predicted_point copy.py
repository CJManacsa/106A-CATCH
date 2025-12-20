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
        self.reset_srv = self.create_service(Empty, "reset_trajectory_pred", self.reset_callback)

        # Frame names
        self.wrist_frame = "wrist_3_link"
        self.ball_frame = "camera_color_optical_frame"

        # Store last received cloud and precomputed closest point
        self.last_cloud = None
        self.last_cloud_time = None
        self.computed_closest = None
        self.published_last = False

        # Trajectory counter
        self.trajectory_count = 0
        self.min_trajectories_for_publish = 4  # need at least 3 valid trajectories before publishing

        # Timer parameters
        self.last_cloud_delay = 0.045  # 45 ms
        self.create_timer(0.01, self.check_last_cloud)

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

        # Precompute closest point immediately
        computed = self.compute_closest_point(cloud_msg)
        if computed is None:
            return

        self.computed_closest = computed
        self.last_cloud = cloud_msg
        self.last_cloud_time = self.get_clock().now()
        self.published_last = False

        # Increment trajectory count for valid clouds
        self.trajectory_count += 1

    def compute_closest_point(self, cloud_msg):
        # Transform wrist into camera frame
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

        # Convert cloud to numpy
        pred_pts = self.pointcloud2_to_xyz(cloud_msg)
        if pred_pts.shape[0] <= 1:  # skip empty or single-point clouds
            return None

        diffs = pred_pts - wrist_vec
        dists = np.linalg.norm(diffs, axis=1)
        idx = np.argmin(dists)
        closest_point = pred_pts[idx]

        # Return as PointStamped
        out = PointStamped()
        out.header = cloud_msg.header
        out.point.x = float(closest_point[0])
        out.point.y = float(closest_point[1])
        out.point.z = float(closest_point[2])
        return out

    def check_last_cloud(self):
        # Only publish if we have enough valid trajectories
        if self.last_cloud is None or self.published_last or self.computed_closest is None:
            return
        if self.trajectory_count < self.min_trajectories_for_publish:
            return

        elapsed = (self.get_clock().now() - self.last_cloud_time).nanoseconds * 1e-9
        if elapsed >= self.last_cloud_delay:
            # Publish precomputed closest point
            self.closest_pub.publish(self.computed_closest)
            self.published_last = True
            ts = self.get_clock().now().to_msg()
            # print(f"Last point printed from trajectory {self.trajectory_count}: {ts.sec}.{ts.nanosec:09d}")

    def reset_callback(self, request, response):
        """Reset all trajectory histories and counters."""
        self.last_cloud = None
        self.last_cloud_time = None
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
