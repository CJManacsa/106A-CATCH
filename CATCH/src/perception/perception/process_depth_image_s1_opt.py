#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, CameraInfo
from geometry_msgs.msg import PointStamped
from catch_custom_msgs.msg import PointVel
import numpy as np
from cv_bridge import CvBridge
import cv2
from collections import deque


class RealSensePCSubscriber(Node):
    def __init__(self):
        super().__init__('realsense_pc_subscriber')

        # Subscribers
        self.pc_sub = self.create_subscription(
            Image,
            '/camera/camera/aligned_depth_to_color/image_raw',
            self.aligned_depth_to_color_callback,
            10
        )
        self.color_info_sub = self.create_subscription(
            CameraInfo,
            '/camera/camera/color/camera_info',
            self.camera_info_callback,
            10
        )
        self.image_mask_sub = self.create_subscription(
            Image,
            '/blob/image_mask',
            self.image_mask_callback,
            10
        )

        # Publishers
        self.ball_pose_pub = self.create_publisher(PointStamped, '/ball_pose', 1)
        self.ball_state_pub = self.create_publisher(PointVel, '/ball_state', 1)

        # Utilities
        self.bridge = CvBridge()
        self.mask_buffer = deque(maxlen=50)
        self.have_intrinsics = False

        # For velocity calculation
        self.prev_pos = None
        self.prev_time = None

        self.get_logger().info("Subscribed to depth, color info, and blob mask topics.")

    def camera_info_callback(self, msg):
        self.fx = msg.k[0]
        self.fy = msg.k[4]
        self.cx = msg.k[2]
        self.cy = msg.k[5]
        self.have_intrinsics = True

    def image_mask_callback(self, msg):
        """Store mask along with its timestamp."""
        try:
            mask_cv = self.bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')
            self.mask_buffer.append((msg.header.stamp, mask_cv))
        except Exception as e:
            self.get_logger().error(f"Failed to convert image mask: {e}")

    def aligned_depth_to_color_callback(self, msg: Image):
        """Compute 3D ball pose and velocity, using timestamp-matched mask."""
        if not self.have_intrinsics or not self.mask_buffer:
            return

        # Find closest mask in time
        depth_stamp = msg.header.stamp.sec + msg.header.stamp.nanosec * 1e-9
        closest_mask = None
        closest_dt = float('inf')
        for mask_stamp, mask_cv in self.mask_buffer:
            mask_time = mask_stamp.sec + mask_stamp.nanosec * 1e-9
            dt = abs(mask_time - depth_stamp)
            if dt < closest_dt:
                closest_dt = dt
                closest_mask = mask_cv

        # Skip if no mask is close enough (e.g., >50ms)
        if closest_mask is None or closest_dt > 0.05:
            return

        mask = closest_mask

        # Convert depth image to meters
        try:
            depth_img = self.bridge.imgmsg_to_cv2(msg, desired_encoding="passthrough")
        except Exception as e:
            self.get_logger().error(f"Depth conversion failed: {e}")
            return
        depth_m = depth_img.astype(np.float32) / 1000.0

        # Resize mask if needed
        if mask.shape != depth_m.shape:
            mask = cv2.resize(mask, (depth_m.shape[1], depth_m.shape[0]), interpolation=cv2.INTER_NEAREST)

        # Pixels where mask == 0
        ys, xs = np.where(mask == 0)
        if len(xs) == 0:
            self.get_logger().warn("Mask received but empty — no blob detected.")
            return

        # Keep only valid depth pixels
        depths = depth_m[ys, xs]
        valid = (depths > 0) & (~np.isnan(depths))
        xs, ys, depths = xs[valid], ys[valid], depths[valid]
        if len(xs) == 0:
            self.get_logger().warn("No valid depth pixels found in mask")
            return

        # Compute 3D points in camera frame
        Xs = (xs - self.cx) * depths / self.fx
        Ys = (ys - self.cy) * depths / self.fy
        Zs = depths

        # Median-based centroid
        X_med, Y_med, Z_med = np.median(Xs), np.median(Ys), np.median(Zs)

        # Radius filter (~baseball radius 0.036 m, 3x margin)
        R_ball = 0.036
        dist_to_med = np.sqrt((Xs - X_med) ** 2 + (Ys - Y_med) ** 2 + (Zs - Z_med) ** 2)
        inliers = dist_to_med < R_ball * 3
        Xs, Ys, Zs = Xs[inliers], Ys[inliers], Zs[inliers]
        if len(Xs) == 0:
            self.get_logger().warn("All points removed by radius filter")
            return

        # Weighted average around median
        dist_to_med = np.sqrt((Xs - X_med) ** 2 + (Ys - Y_med) ** 2 + (Zs - Z_med) ** 2)
        weights = np.exp(-dist_to_med**2 / (2 * (0.02**2)))
        X_final = np.average(Xs, weights=weights)
        Y_final = np.average(Ys, weights=weights)
        Z_final = np.average(Zs, weights=weights)

        if Z_final > 3.0:
            self.get_logger().warn(f"Ball too far away (Z={Z_final:.2f} m), not publishing")
            return

        # --- Publish PointStamped ---
        pt = PointStamped()
        pt.header = msg.header
        pt.point.x, pt.point.y, pt.point.z = float(X_final), float(Y_final), float(Z_final)
        self.ball_pose_pub.publish(pt)

        # --- Compute velocity ---
        curr_pos = np.array([X_final, Y_final, Z_final])
        curr_time = depth_stamp
        if self.prev_pos is not None:
            dt = max(curr_time - self.prev_time, 1e-6)
            vel = (curr_pos - self.prev_pos) / dt
        else:
            vel = np.zeros(3)

        self.prev_pos = curr_pos
        self.prev_time = curr_time

        # --- Publish PointVel ---
        pv = PointVel()
        pv.header = msg.header
        pv.x, pv.y, pv.z = float(X_final), float(Y_final), float(Z_final)
        pv.vx, pv.vy, pv.vz = float(vel[0]), float(vel[1]), float(vel[2])
        self.ball_state_pub.publish(pv)


def main(args=None):
    rclpy.init(args=args)
    node = RealSensePCSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()