import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2
from geometry_msgs.msg import PointStamped
import numpy as np
import sensor_msgs_py.point_cloud2 as pc2
from std_msgs.msg import Header

class RealSensePCSubscriber(Node):
    def __init__(self):
        super().__init__('realsense_pc_subscriber')

        # Plane coefficients and max distance (meters)
        self.declare_parameter('plane.a', 0.0)
        self.declare_parameter('plane.b', 0.0)
        self.declare_parameter('plane.c', 0.0)
        self.declare_parameter('plane.d', 0.0)
        self.declare_parameter('max_distance', 0.6)

        self.a = self.get_parameter('plane.a').value
        self.b = self.get_parameter('plane.b').value
        self.c = self.get_parameter('plane.c').value
        self.d = self.get_parameter('plane.d').value
        self.max_distance = self.get_parameter('max_distance').value

        # Subscribers
        self.pc_sub = self.create_subscription(
            PointCloud2,
            '/camera/camera/depth/color/points',
            self.pointcloud_callback,
            10
        )

        # Publishers
        self.cube_pose_pub = self.create_publisher(PointStamped, '/cube_pose', 1)
        self.filtered_points_pub = self.create_publisher(PointCloud2, '/filtered_points', 1)

        self.get_logger().info("Subscribed to PointCloud2 topic and marker publisher ready")

    def pointcloud_callback(self, msg: PointCloud2):
        # Convert PointCloud2 to Nx3 array
        points = []
        for p in pc2.read_points(msg, field_names=('x','y','z'), skip_nans=True):
            points.append([p[0], p[1], p[2]])

        points = np.array(points)
        # ------------------------
        #TODO: Add your code here!
        # ------------------------

        # Compute distance of each point in point cloud to the plane 
        norm = np.sqrt(self.a**2 + self.b**2 + self.c**2)
        distances_to_plane = (self.a*points[:,0] + self.b*points[:,1] + self.c*points[:,2] + self.d) / norm

        # Filter above plane
        above_plane = distances_to_plane > 0  # keep points above

        # filter in z direction
        dist_from_cam = np.linalg.norm(points, axis=1)  # Euclidean distance from origin
        within_range = dist_from_cam < self.max_distance

        # Combine filters
        mask = np.logical_and(above_plane, within_range)
        filtered_points = points[mask] # Filter the point cloud to only the points in our mask

        # Find the mean of the points we have to identify center of cube
        if filtered_points.shape[0] > 0:
            cube_center = np.mean(filtered_points, axis=0)  # shape (3,)
            cube_x, cube_y, cube_z = map(float, cube_center)
        else:
            cube_x = cube_y = cube_z = float('nan')

        
        # Apply max distance filter

       
        # # Apply other filtering relative to plane
        # filtered_points = []

        # # Compute position of the cube via remaining points
        # cube_x = 0.0
        # cube_y = 0.0
        # cube_z = 0.0

        self.get_logger().info(f"Filtered points: {filtered_points.shape[0]}")

        cube_pose = PointStamped()
        # Fill in message
        cube_pose.header = msg.header
        cube_pose.point.x = cube_x
        cube_pose.point.y = cube_y
        cube_pose.point.z = cube_z
        self.get_logger().info(f"Cube Center: x:{cube_x}, y:{cube_y}, z:{cube_z}\n")

        self.cube_pose_pub.publish(cube_pose)

        self.publish_filtered_points(filtered_points, msg.header)

    def publish_filtered_points(self, filtered_points: np.ndarray, header: Header):
        # Create PointCloud2 message from filtered Nx3 array
        filtered_msg = pc2.create_cloud_xyz32(header, filtered_points.tolist())
        self.filtered_points_pub.publish(filtered_msg)


def main(args=None):
    rclpy.init(args=args)
    node = RealSensePCSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()