import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, CameraInfo
from geometry_msgs.msg import PointStamped
import numpy as np
import sensor_msgs_py.point_cloud2 as pc2
from cv_bridge import CvBridge
import cv2


class RealSensePCSubscriber(Node):
    def __init__(self):
        super().__init__('realsense_pc_subscriber')

        # Subscribers
        self.pc_sub = self.create_subscription(
            Image, '/camera/camera/aligned_depth_to_color/image_raw', self.aligned_depth_to_color_callback, 10
        )
        self.color_info_sub = self.create_subscription(
            CameraInfo,
            '/camera/camera/color/camera_info',
            self.camera_info_callback,
            10
        )

        self.image_mask_sub = self.create_subscription(
            Image, '/blob/image_mask', self.image_mask_callback, 10
        )

        # Publishers
        self.ball_pose_pub = self.create_publisher(PointStamped, '/ball_pose', 1)

        self.bridge = CvBridge()
        self.image_mask = None

        self.have_intrinsics = False

        self.get_logger().info("Subscribed to depth to color image and image mask topics.")


    def camera_info_callback(self, msg):
        self.fx = msg.k[0]
        self.fy = msg.k[4]
        self.cx = msg.k[2]
        self.cy = msg.k[5]
        self.have_intrinsics = True

        # You can log once
        # self.get_logger().info_once(f"Camera intrinsics loaded: fx={self.fx}, fy={self.fy}")

    def image_mask_callback(self, msg):
        """Receive the binary mask from the blob detector."""
        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')
            self.image_mask = cv_image
            # self.get_logger().info(f"Received image mask of shape: {self.image_mask.shape}")
        except Exception as e:
            self.get_logger().error(f"Failed to convert image mask: {e}")

    def aligned_depth_to_color_callback(self, msg: Image):
        """Compute 3D ball pose using robust centroid calculation with weighted averaging."""

        if not self.have_intrinsics:
            self.get_logger().warn("No camera intrinsics yet")
            return

        if self.image_mask is None:
            return  # no mask from blob detector yet

        # 1. Convert depth image to numpy (16UC1 → meters)
        try:
            depth_img = self.bridge.imgmsg_to_cv2(msg, desired_encoding="passthrough")
        except Exception as e:
            self.get_logger().error(f"Depth conversion failed: {e}")
            return

        depth_m = depth_img.astype(np.float32) / 1000.0  # mm → meters

        # 2. Resize mask to depth resolution if needed
        mask = self.image_mask
        if mask.shape != depth_m.shape:
            mask = cv2.resize(mask, (depth_m.shape[1], depth_m.shape[0]), interpolation=cv2.INTER_NEAREST)

        # 3. Inverted mask → ball is where pixel == 0
        ys, xs = np.where(mask == 0)
        if len(xs) == 0:
            self.get_logger().warn("Mask received but empty — no blob detected.")
            return

        # Keep only pixels with valid depth
        depths = depth_m[ys, xs]
        valid = (depths > 0) & (~np.isnan(depths))
        ys = ys[valid]
        xs = xs[valid]
        depths = depths[valid]

        if len(xs) == 0:
            self.get_logger().warn("No valid depth pixels found in mask")
            return

        # --- Compute 3D coords relative to camera frame ---
        Xs = (xs - self.cx) * depths / self.fx
        Ys = (ys - self.cy) * depths / self.fy
        Zs = depths

        # --- Median-based initial centroid ---
        X_med = np.median(Xs)
        Y_med = np.median(Ys)
        Z_med = np.median(Zs)

        # --- Radius filter (baseball radius ~0.036 m) ---
        R_ball = 0.036  # meters
        dist_to_median = np.sqrt((Xs - X_med) ** 2 + (Ys - Y_med) ** 2 + (Zs - Z_med) ** 2)
        inliers = dist_to_median < R_ball * 3  # 50% margin
        Xs = Xs[inliers]
        Ys = Ys[inliers]
        Zs = Zs[inliers]

        if len(Xs) == 0:
            self.get_logger().warn("All points removed by radius filter")
            return

        # --- Depth spread check ---
        # depth_std = np.std(Zs)
        # max_depth_std_allowed = 0.06  # 6 cm for a baseball
        # if depth_std > max_depth_std_allowed:
        #     self.get_logger().warn(f"Depth spread too large (std={depth_std:.3f} m), not publishing")
        #     return

        # --- Weighted average around median ---
        dist_to_median = np.sqrt((Xs - X_med) ** 2 + (Ys - Y_med) ** 2 + (Zs - Z_med) ** 2)
        weights = np.exp(-dist_to_median**2 / (2 * (0.02**2)))  # sigma=2cm → steeper drop-off

        X_final = np.average(Xs, weights=weights)
        Y_final = np.average(Ys, weights=weights)
        Z_final = np.average(Zs, weights=weights)

        # --- Check final Z distance ---
        if Z_final > 3.0:
            self.get_logger().warn(f"Ball too far away (Z={Z_final:.2f} m), not publishing")
            return

        # --- Publish final ball pose ---
        pt = PointStamped()
        pt.header = msg.header
        pt.point.x = float(X_final)
        pt.point.y = float(Y_final)
        pt.point.z = float(Z_final)
        self.ball_pose_pub.publish(pt)

        self.get_logger().info(
            f"Ball pose → X={X_final:.3f}  Y={Y_final:.3f}  Z={Z_final:.3f} "
            f"(pixels median u~{int(np.mean(xs))}, v~{int(np.mean(ys))}, depth std={depth_std:.3f} m)"
        )








def main(args=None):
    rclpy.init(args=args)
    node = RealSensePCSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
