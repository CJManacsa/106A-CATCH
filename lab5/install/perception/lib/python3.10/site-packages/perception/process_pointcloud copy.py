import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2, Image
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
            PointCloud2, '/camera/camera/depth/color/points', self.pointcloud_callback, 10
        )
        self.image_mask_sub = self.create_subscription(
            Image, '/blob/image_mask', self.image_mask_callback, 10
        )

        # Publishers
        self.ball_pose_pub = self.create_publisher(PointStamped, '/ball_pose', 1)
        self.filtered_points_pub = self.create_publisher(PointCloud2, '/filtered_points', 1)

        self.bridge = CvBridge()
        self.image_mask = None

        self.get_logger().info("Subscribed to PointCloud2 and image mask topics.")

    def image_mask_callback(self, msg):
        """Receive the binary mask from the blob detector."""
        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')
            self.image_mask = cv_image
            self.get_logger().info(f"Received image mask of shape: {self.image_mask.shape}")
        except Exception as e:
            self.get_logger().error(f"Failed to convert image mask: {e}")

    def pointcloud_callback(self, msg: PointCloud2):
        """Filter the point cloud using only the binary mask (no spatial filtering)."""
        
        if self.image_mask is None:
            return  # No mask yet

        # --- Debug: print the pointcloud frame and mask info
        self.get_logger().info(
            f"PointCloud frame_id: {msg.header.frame_id}, "
            f"Mask shape: {self.image_mask.shape}"
        )

        depth_h, depth_w = msg.height, msg.width
        assert self.image_mask.shape[:2] == (depth_h, depth_w), \
            f"Mask shape {self.image_mask.shape[:2]} doesn't match pointcloud {depth_h, depth_w}"

        # Invert mask: keep where mask == 0
        mask_flat = (self.image_mask.flatten() == 0)

        # Collect filtered points based on mask
        filtered_points = []
        for i, p in enumerate(pc2.read_points(msg, field_names=('x', 'y', 'z'), skip_nans=False)):
            if mask_flat[i]:
                filtered_points.append((p[0], p[1], p[2]))

        if not filtered_points:
            self.get_logger().warn("No points passed the mask.")
            return

        filtered_points = np.array(filtered_points, dtype=np.float32)

        # Compute mean center of masked region
        ball_center = np.mean(filtered_points, axis=0)
        ball_x, ball_y, ball_z = map(float, ball_center)

        # Publish ball center
        ball_pose = PointStamped()
        ball_pose.header = msg.header
        ball_pose.point.x = ball_x
        ball_pose.point.y = ball_y
        ball_pose.point.z = ball_z
        self.ball_pose_pub.publish(ball_pose)

        # Publish filtered cloud (XYZ only)
        filtered_msg = pc2.create_cloud_xyz32(msg.header, filtered_points.tolist())
        self.filtered_points_pub.publish(filtered_msg)

        self.get_logger().info(
            f"Published filtered cloud ({len(filtered_points)} pts), "
            f"Ball center: x={ball_x:.3f}, y={ball_y:.3f}, z={ball_z:.3f}"
        )



def main(args=None):
    rclpy.init(args=args)
    node = RealSensePCSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
