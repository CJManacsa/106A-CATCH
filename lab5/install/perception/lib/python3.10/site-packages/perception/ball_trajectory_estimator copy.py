import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PointStamped
from sensor_msgs.msg import PointCloud2, PointField
from std_msgs.msg import Header
import numpy as np
from collections import deque
import struct

class BallTrajectoryEstimator(Node):
    def __init__(self):
        super().__init__('ball_trajectory_estimator')

        # Subscribe to the ball position topic
        self.sub = self.create_subscription(
            PointStamped,
            '/ball_pose',
            self.ball_callback,
            10
        )

        # Publish trajectory as PointCloud2
        self.trajectory_pub = self.create_publisher(PointCloud2, '/ball_trajectory', 1)

        # Keep a deque of the last 10 positions
        self.positions = deque(maxlen=10)

        self.get_logger().info("Ball Trajectory Estimator node started.")

    def ball_callback(self, msg: PointStamped):
        # Append current position
        pos = [msg.point.x, msg.point.y, msg.point.z]
        self.positions.append(pos)

        if len(self.positions) < 1:
            return

        # Build PointCloud2 points with RGBA (neon yellow)
        points = []
        for p in self.positions:
            r, g, b, a = 255, 255, 0, 255  # neon yellow
            # Pack in little-endian BGRA for ROS2
            rgba = struct.unpack('<I', struct.pack('<BBBB', b, g, r, a))[0]
            points.append([p[0], p[1], p[2], rgba])

        # Flatten points for PointCloud2 using struct (correct for uint32 color)
        flat_points = b''.join([struct.pack('<fffI', p[0], p[1], p[2], p[3]) for p in points])

        # Create PointCloud2 message
        header = Header()
        header.stamp = self.get_clock().now().to_msg()
        header.frame_id = msg.header.frame_id

        pc2_msg = PointCloud2()
        pc2_msg.header = header
        pc2_msg.height = 1
        pc2_msg.width = len(points)
        pc2_msg.is_dense = True
        pc2_msg.is_bigendian = False
        pc2_msg.fields = [
            PointField(name='x', offset=0, datatype=PointField.FLOAT32, count=1),
            PointField(name='y', offset=4, datatype=PointField.FLOAT32, count=1),
            PointField(name='z', offset=8, datatype=PointField.FLOAT32, count=1),
            PointField(name='rgba', offset=12, datatype=PointField.UINT32, count=1),
        ]
        pc2_msg.point_step = 16
        pc2_msg.row_step = pc2_msg.point_step * len(points)
        pc2_msg.data = flat_points

        # Publish the trajectory
        self.trajectory_pub.publish(pc2_msg)

        # Optional: log estimated velocity
        if len(self.positions) >= 2:
            positions_array = np.array(self.positions)
            dt = 0.033  # assume ~30 Hz
            velocities = np.diff(positions_array, axis=0) / dt
            avg_velocity = np.mean(velocities, axis=0)
            self.get_logger().info(
                f"Estimated velocity vector: vx={avg_velocity[0]:.2f}, "
                f"vy={avg_velocity[1]:.2f}, vz={avg_velocity[2]:.2f}"
            )

def main(args=None):
    rclpy.init(args=args)
    node = BallTrajectoryEstimator()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
