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

        # Publishers
        self.trajectory_pub = self.create_publisher(PointCloud2, '/ball_trajectory', 1)
        self.predicted_pub = self.create_publisher(PointCloud2, '/ball_predicted_trajectory', 1)

        # Keep a deque of the last 10 positions
        self.positions = deque(maxlen=10)

        self.get_logger().info("Ball Trajectory Estimator node started.")

    def smooth_z(self, positions_array: np.ndarray, window=3):
        """
        Simple moving average smoothing along the z-axis.
        positions_array: Nx3 array
        window: number of points to average over
        """
        z = positions_array[:, 2]
        window = min(window, len(z))  # <--- avoid negative dimensions
        smoothed_z = np.convolve(z, np.ones(window)/window, mode='valid')
        
        pad = np.full((len(z) - len(smoothed_z),), smoothed_z[0])
        smoothed_z = np.concatenate([pad, smoothed_z])
        positions_array[:, 2] = smoothed_z
        return positions_array


    def ball_callback(self, msg: PointStamped):
        # Append current position
        pos = [msg.point.x, msg.point.y, msg.point.z]
        self.positions.append(pos)

        if len(self.positions) < 2:
            return  # need at least 2 points to estimate velocity

        # Convert to array and smooth z-axis
        positions_array = np.array(self.positions)
        positions_array = self.smooth_z(positions_array, window=7)

        dt = 0.033  # approximate time between points

        # --- PUBLISH HISTORY TRAIL (NEON GREEN) ---
        self.publish_pointcloud(positions_array, self.trajectory_pub, msg.header.frame_id, color=(0, 255, 0))

        # --- ESTIMATE INITIAL VELOCITY FROM LAST 2 POINTS ---
        v0 = (positions_array[-1] - positions_array[-2]) / dt

        # --- PREDICT PROJECTILE TRAJECTORY (gravity along y-axis) ---
        g = 9.81  # gravity in m/s^2
        num_predicted_points = 30
        predicted_points = []
        t_step = dt  # small step for smooth trajectory

        last_pos = positions_array[-1]
        for i in range(1, num_predicted_points + 1):
            t = i * t_step
            x = last_pos[0] + v0[0] * t       # lateral
            y = last_pos[1] + v0[1] * t + 0.5 * g * t**2  # vertical
            z = last_pos[2] + v0[2] * t       # depth
            predicted_points.append([x, y, z])

        predicted_array = np.array(predicted_points)
        # Optional: smooth predicted z too
        predicted_array = self.smooth_z(predicted_array, window=3)

        # --- PUBLISH PREDICTED TRAIL (NEON YELLOW) ---
        self.publish_pointcloud(predicted_array, self.predicted_pub, msg.header.frame_id, color=(255, 255, 0))

        # Log estimated velocity
        self.get_logger().info(
            f"Estimated last velocity vector: vx={v0[0]:.2f}, vy={v0[1]:.2f}, vz={v0[2]:.2f}"
        )

    def publish_pointcloud(self, points_array: np.ndarray, publisher, frame_id: str, color=(255, 255, 0)):
        """
        Publish a PointCloud2 given a points array (Nx3) and a color (RGB tuple)
        """
        r, g, b = color
        a = 255
        points = []
        for p in points_array:
            rgba = struct.unpack('<I', struct.pack('<BBBB', b, g, r, a))[0]
            points.append([p[0], p[1], p[2], rgba])

        flat_points = b''.join([struct.pack('<fffI', p[0], p[1], p[2], p[3]) for p in points])

        header = Header()
        header.stamp = self.get_clock().now().to_msg()
        header.frame_id = frame_id

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

        publisher.publish(pc2_msg)

def main(args=None):
    rclpy.init(args=args)
    node = BallTrajectoryEstimator()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
