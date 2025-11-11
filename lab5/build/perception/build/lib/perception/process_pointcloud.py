import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2, Image
from geometry_msgs.msg import PointStamped, Point
import numpy as np
import sensor_msgs_py.point_cloud2 as pc2
from std_msgs.msg import Header
from cv_bridge import CvBridge
import cv2

class RealSensePCSubscriber(Node):
    def __init__(self):
        super().__init__('realsense_pc_subscriber')
        
        # Subscribers
        self.pc_sub = self.create_subscription(PointCloud2, '/camera/camera/depth/color/points', self.pointcloud_callback, 10)
        self.blob_point_sub = self.create_subscription(Point, '/blob/point_blob', self.blob_point_callback, 10)
        self.image_mask_sub = self.create_subscription(Image, '/blob/image_mask', self.image_mask_callback, 10)

        # Publishers
        self.ball_pose_pub = self.create_publisher(PointStamped, '/ball_pose', 1)
        self.filtered_points_pub = self.create_publisher(PointCloud2, '/filtered_points', 1)

        self.get_logger().info("Subscribed to PointCloud2 topic, blob point, and image mask")

        # For converting ROS Image to OpenCV format
        self.bridge = CvBridge()

        # Placeholder for blob point and mask
        self.blob_point = None
        self.image_mask = None

    def blob_point_callback(self, msg):
        """Callback for the blob point."""
        self.blob_point = msg
        self.get_logger().info(f"Received blob point: ({self.blob_point.x}, {self.blob_point.y}, {self.blob_point.z})")

    def image_mask_callback(self, msg):
        """Callback for the image mask."""
        try:
            # Convert ROS Image message to OpenCV image format
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')
            self.image_mask = cv_image
            self.get_logger().info(f"Received image mask of shape: {self.image_mask.shape}")
        except Exception as e:
            self.get_logger().error(f"Failed to convert image message: {e}")

    def pointcloud_callback(self, msg: PointCloud2):
        """Point cloud callback where the point cloud data is processed."""
        # Convert PointCloud2 to Nx3 array
        points = []
        for p in pc2.read_points(msg, field_names=('x', 'y', 'z'), skip_nans=True):
            points.append([p[0], p[1], p[2]])
        points = np.array(points)

        if self.blob_point is not None and self.image_mask is not None:
            # Apply mask based on the blob point
            filtered_points = self.filter_points(points)

            # Use blob data to refine the point cloud filtering
            ball_x, ball_y, ball_z = self.get_ball_center(filtered_points)

            # Publish filtered points and ball pose
            ball_pose = PointStamped()
            ball_pose.header = msg.header
            ball_pose.point.x = ball_x
            ball_pose.point.y = ball_y
            ball_pose.point.z = ball_z

            self.get_logger().info(f"Ball Center: x:{ball_x}, y:{ball_y}, z:{ball_z}")

            self.ball_pose_pub.publish(ball_pose)
            self.publish_filtered_points(filtered_points, msg.header)

        else:
            self.get_logger().warn("Blob point or image mask not yet received.")

    def filter_points(self, points):
        """Filter points using the blob point and image mask."""
        if self.blob_point is None or self.image_mask is None:
            return np.array([])  # If blob point or mask is invalid, discard all points
        
        # Step 1: Scale the blob point from percentage to pixel coordinates in the image
        blob_x = self.blob_point.x  # This is a percentage (0 to 1)
        blob_y = self.blob_point.y  # This is a percentage (0 to 1)
        
        # The resolution of the image and point cloud
        rgb_width = 960
        rgb_height = 540
        pc_width = 848
        pc_height = 480
        
        # Scale the blob point to pixel coordinates in the RGB image
        x_rgb = int(blob_x * rgb_width)  # Scaled to pixel coordinates in RGB frame
        y_rgb = int(blob_y * rgb_height)  # Scaled to pixel coordinates in RGB frame
        
        # Step 2: Rescale the coordinates to the point cloud resolution
        x_scaled = x_rgb * (pc_width / rgb_width)
        y_scaled = y_rgb * (pc_height / rgb_height)
        
        # Step 3: Resize the mask to match the point cloud's resolution
        resized_mask = cv2.resize(self.image_mask, (pc_width, pc_height), interpolation=cv2.INTER_NEAREST)

        # Step 4: Check bounds to avoid out-of-bounds access
        if int(y_scaled) < 0 or int(y_scaled) >= resized_mask.shape[0] or int(x_scaled) < 0 or int(x_scaled) >= resized_mask.shape[1]:
            self.get_logger().warn(f"Blob point ({x_scaled}, {y_scaled}) is out of mask bounds.")
            return np.array([])  # Return empty points if blob point is out of bounds
        
        # Step 5: Check the mask at the scaled blob point (inverted mask logic)
        mask = resized_mask[int(y_scaled), int(x_scaled)]  # Mask value at the blob point
        
        # Since the mask is inverted, we check for a value of 0 (the ball region)
        if mask != 0:
            self.get_logger().warn(f"Mask at blob point ({x_scaled}, {y_scaled}) is not valid, discarding points.")
            return np.array([])  # Return empty points if the mask at the blob point is invalid
        
        # Step 6: Filter points based on proximity to the blob point (distance threshold)
        pointcloud_xy = points[:, :2]  # (N, 2)
        distance_threshold = 0.05  # Adjust this based on ball size and noise level
        distances = np.linalg.norm(pointcloud_xy - np.array([x_scaled, y_scaled]), axis=1)
        filtered_points = points[distances < distance_threshold]

        return filtered_points




    def get_ball_center(self, filtered_points):
        """Compute the center of the ball (or object) from filtered points."""
        if filtered_points.shape[0] > 0:
            ball_center = np.mean(filtered_points, axis=0)  # shape (3,)
            ball_x, ball_y, ball_z = map(float, ball_center)
        else:
            ball_x = ball_y = ball_z = float('nan')
        
        return ball_x, ball_y, ball_z

    def publish_filtered_points(self, filtered_points: np.ndarray, header: Header):
        """Publish the filtered point cloud."""
        # Convert the filtered point cloud to a PointCloud2 message
        filtered_msg = pc2.create_cloud_xyz32(header, filtered_points.tolist())
        # Publish the filtered point cloud message
        self.filtered_points_pub.publish(filtered_msg)

def main(args=None):
    rclpy.init(args=args)
    node = RealSensePCSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
