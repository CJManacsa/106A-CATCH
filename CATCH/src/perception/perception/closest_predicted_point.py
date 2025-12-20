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
        self.target_trajectory = 4

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
        # --- 1. TF: wrist → base_link ---
        try:
            wrist_tf = self.tf_buffer.lookup_transform(
                self.output_frame,        # base_link
                self.wrist_frame,         # wrist
                rclpy.time.Time()
            )

            wrist_pt = PointStamped()
            wrist_pt.header.frame_id = self.wrist_frame
            wrist_pt.point.x = wrist_pt.point.y = wrist_pt.point.z = 0.0

            wrist_in_base = tf2_geometry_msgs.do_transform_point(wrist_pt, wrist_tf)
            wrist_vec = np.array([
                wrist_in_base.point.x,
                wrist_in_base.point.y,
                wrist_in_base.point.z
            ], dtype=np.float32)

        except Exception as e:
            self.get_logger().warn(f"TF lookup failed for wrist position: {e}")
            return None

        # --- 2. Convert point cloud to xyz ---
        pred_pts = self.pointcloud2_to_xyz(cloud_msg)
        if pred_pts.shape[0] <= 1:
            self.get_logger().warn("Not enough predicted points.")
            return None

        # --- 3. Transform all predicted points to base_link ---
        try:
            tf_to_base = self.tf_buffer.lookup_transform(
                self.output_frame,           # base_link
                cloud_msg.header.frame_id,   # camera frame
                rclpy.time.Time()
            )

            pts_base = []
            for p in pred_pts:
                pt = PointStamped()
                pt.header = cloud_msg.header
                pt.point.x, pt.point.y, pt.point.z = map(float, p)
                pt_base = tf2_geometry_msgs.do_transform_point(pt, tf_to_base)
                pts_base.append([
                    pt_base.point.x,
                    pt_base.point.y,
                    pt_base.point.z
                ])

            pts_base = np.array(pts_base, dtype=np.float32)

        except Exception as e:
            self.get_logger().warn(f"Point transform failed: {e}")
            return None

        # --- 4. Apply Filters (in base_link frame) ---

        # 4.1 Keep points within 0.8m sphere
        dist_origin = np.linalg.norm(pts_base, axis=1)
        mask = dist_origin <= 0.8
        pts_base = pts_base[mask]

        if pts_base.shape[0] == 0:
            self.get_logger().warn("Filter 4.1 (sphere <= 0.8m) removed all points.")
            return None

        # 4.2 Remove points inside 0.5m cylinder
        radial_dist = np.linalg.norm(pts_base[:, :2], axis=1)
        mask = radial_dist >= 0.5
        pts_base = pts_base[mask]

        if pts_base.shape[0] == 0:
            self.get_logger().warn("Filter 4.2 (remove cylinder r < 0.5m) removed all points.")
            return None

        # 4.3 Keep z <= 0.4
        mask = pts_base[:, 2] <= 0.4
        pts_base = pts_base[mask]

        if pts_base.shape[0] == 0:
            self.get_logger().warn("Filter 4.3 (z <= 0.4) removed all points.")
            return None

        # 4.4 Keep y >= 0.1
        mask = pts_base[:, 1] >= 0.1
        pts_base = pts_base[mask]

        if pts_base.shape[0] == 0:
            self.get_logger().warn("Filter 4.4 (y >= 0.1) removed all points.")
            return None

        # 4.5 Keep z >= -0.256
        mask = pts_base[:, 2] >= -0.256
        pts_base = pts_base[mask]

        if pts_base.shape[0] == 0:
            self.get_logger().warn("Filter 4.5 (z >= -0.256) removed all points.")
            return None

        # --- 5. Select point closest to the wrist ---
        dists = np.linalg.norm(pts_base - wrist_vec, axis=1)
        idx = int(np.argmin(dists))
        cp = pts_base[idx]

        # --- 6. Construct output and apply Y offset ---
        result = PointStamped()
        result.header.stamp = cloud_msg.header.stamp
        result.header.frame_id = self.output_frame
        result.point.x = float(cp[0])
        result.point.y = float(cp[1] - 0.08)
        result.point.z = float(cp[2])

        return result


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
