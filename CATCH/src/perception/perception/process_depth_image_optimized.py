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
        """Optimized depth + mask fusion and velocity estimation."""

        if not self.have_intrinsics or not self.mask_buffer:
            return

        # --- Convert depth timestamp ---
        depth_time = msg.header.stamp.sec + msg.header.stamp.nanosec * 1e-9

        # --- Find closest mask using binary search (fast) ---
        mask_times = [t.sec + t.nanosec * 1e-9 for t, _ in self.mask_buffer]
        idx = np.searchsorted(mask_times, depth_time)

        # pick closest of idx or idx-1
        best_idx = None
        if 0 < idx < len(mask_times):
            best_idx = idx if abs(mask_times[idx] - depth_time) < abs(mask_times[idx-1] - depth_time) else idx-1
        elif idx == 0:
            best_idx = 0
        else:
            best_idx = len(mask_times) - 1

        closest_mask_time, mask = self.mask_buffer[best_idx]
        dt = abs((closest_mask_time.sec + closest_mask_time.nanosec * 1e-9) - depth_time)

        # tolerance increased (50ms)
        if dt > 0.05:
            return

        # --- Convert depth image ---
        try:
            depth_raw = self.bridge.imgmsg_to_cv2(msg, "passthrough")
        except Exception as e:
            self.get_logger().error(f"Depth conversion failed: {e}")
            return

        # Resize mask only if needed (rare)
        if mask.shape != depth_raw.shape:
            mask = cv2.resize(mask, (depth_raw.shape[1], depth_raw.shape[0]), cv2.INTER_NEAREST)

        # Extract masked pixels quickly
        masked = (mask == 0)
        if not masked.any():
            return

        ys, xs = np.where(masked)
        depths = depth_raw[ys, xs].astype(np.float32) * 0.001
        valid = (depths > 0.1) & (depths < 5.0)

        if not valid.any():
            return

        xs = xs[valid]
        ys = ys[valid]
        depths = depths[valid]

        # Camera model
        Xs = (xs - self.cx) * depths / self.fx
        Ys = (ys - self.cy) * depths / self.fy
        Zs = depths

        # Median centroid (fast, robust)
        X_med = float(np.median(Xs))
        Y_med = float(np.median(Ys))
        Z_med = float(np.median(Zs))

        # Filter by radius around median (avoid computing sqrt N times)
        R2 = (0.036 * 3) ** 2
        dist2 = (Xs - X_med)**2 + (Ys - Y_med)**2 + (Zs - Z_med)**2
        inliers = dist2 < R2

        if not inliers.any():
            return

        Xs = Xs[inliers]
        Ys = Ys[inliers]
        Zs = Zs[inliers]

        # Weighted average (stable)
        dist2 = (Xs - X_med)**2 + (Ys - Y_med)**2 + (Zs - Z_med)**2
        weights = np.exp(-dist2 / (2 * 0.02**2))

        X_final = float(np.average(Xs, weights=weights))
        Y_final = float(np.average(Ys, weights=weights))
        Z_final = float(np.average(Zs, weights=weights))

        if Z_final > 3.0:
            return

        # --- Publish ball pose ---
        pt = PointStamped()
        pt.header = msg.header
        pt.point.x = X_final
        pt.point.y = Y_final
        pt.point.z = Z_final
        self.ball_pose_pub.publish(pt)

        # --- Velocity ---
        curr_time = depth_time
        if self.prev_pos is not None:
            dt = max(curr_time - self.prev_time, 1e-6)
            vel = (np.array([X_final, Y_final, Z_final]) - self.prev_pos) / dt
        else:
            vel = np.zeros(3)

        self.prev_pos = np.array([X_final, Y_final, Z_final])
        self.prev_time = curr_time

        # Publish velocity
        pv = PointVel()
        pv.header = msg.header
        pv.x, pv.y, pv.z = X_final, Y_final, Z_final
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