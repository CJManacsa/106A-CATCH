import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2, PointField
from std_msgs.msg import Header
import numpy as np
from collections import deque
import struct
from catch_custom_msgs.msg import PointVel
from std_srvs.srv import Empty


class BallTrajectoryEstimator(Node):
    def __init__(self):
        super().__init__('ball_trajectory_estimator')

        # Subscribe to ball state topic
        self.sub = self.create_subscription(PointVel, '/ball_state', self.ball_callback, 10)

        # Publishers
        self.trajectory_pub = self.create_publisher(PointCloud2, '/ball_trajectory', 1)
        self.predicted_pub = self.create_publisher(PointCloud2, '/ball_predicted_trajectory', 1)

        # Reset service
        self.reset_srv = self.create_service(Empty, 'reset_trajectory', self.reset_callback)

        # History
        self.positions_history = deque(maxlen=20)
        self.velocities_history = deque(maxlen=10)
        self.predicted_trajs = deque(maxlen=20)

        self.header = None

        self.get_logger().info("Ball Trajectory Estimator node started.")

    def ball_callback(self, msg: PointVel):
        # Append new measurement
        self.positions_history.append([msg.x, msg.y, msg.z])
        self.velocities_history.append([msg.vx, msg.vy, msg.vz])

        positions_array = np.array(self.positions_history)
        velocities_array = np.array(self.velocities_history)
        self.header = msg.header

        # --- Publish green trail ---
        self.publish_pointcloud(positions_array, self.trajectory_pub, msg.header, color=(0, 255, 0, 255))

        # --- Smooth X and Z velocities ---
        vx_nonzero = velocities_array[-5:, 0][velocities_array[-5:, 0] != 0]
        vz_nonzero = velocities_array[-5:, 2][velocities_array[-5:, 2] != 0]

        vx_smooth = vx_nonzero.mean() if len(vx_nonzero) > 0 else velocities_array[-1, 0]
        vz_smooth = vz_nonzero.mean() if len(vz_nonzero) > 0 else velocities_array[-1, 2]

        # --- Y velocity: NO SMOOTHING ---
        vy_smooth = velocities_array[-1, 1]

        # --- Combine smoothed velocities ---
        v0 = np.array([vx_smooth, vy_smooth, vz_smooth])

        # --- Least squares Z smoothing ---
        positions_for_ls = positions_array[-5:]
        xs = positions_for_ls[:, 0]
        zs = positions_for_ls[:, 2]
        last_x = positions_for_ls[-1, 0]
        if len(xs) >= 2:
            a, b = np.polyfit(xs, zs, 1)
            z_smooth = a * last_x + b
        else:
            z_smooth = positions_for_ls[-1, 2]

        last_pos = np.array([positions_array[-1, 0], positions_array[-1, 1], z_smooth])

        # --- Only predict trajectory if at least 2 positions ---
        if len(positions_array) < 2:
            return

        # --- Predict trajectory ---
        dt = 0.033
        g = 9.81
        predicted_points = []
        for i in range(1, 11):
            t = i * dt
            x = last_pos[0] + v0[0] * t
            y = last_pos[1] + v0[1] * t + 0.5 * g * t**2
            z = last_pos[2] + v0[2] * t
            predicted_points.append([x, y, z])

        predicted_array = np.array(predicted_points)
        self.predicted_trajs.append(predicted_array)

        # --- Merge predictions with fade ---
        all_points = []
        N_trajs = len(self.predicted_trajs)
        for i, traj in enumerate(self.predicted_trajs):
            fade = (i + 1) / N_trajs
            r, g_col, b_col, alpha = 255, int(255 * fade), 0, 255 #int(255 * fade)
            for p in traj:
                rgba = struct.unpack('<I', struct.pack('<BBBB', b_col, g_col, r, alpha))[0]
                all_points.append([float(p[0]), float(p[1]), float(p[2]), int(rgba)])

        all_points_array = np.array(all_points)
        self.publish_pointcloud(all_points_array, self.predicted_pub, msg.header, color=None)

    def reset_callback(self, request, response):
        self.positions_history.clear()
        self.velocities_history.clear()
        self.predicted_trajs.clear()

        dummy_points = np.array([[0.0, 0.0, -100.0, 0]], dtype=np.float32)
        header = Header()
        header.stamp = self.get_clock().now().to_msg()
        header.frame_id = self.header.frame_id if self.header else "world"

        self.publish_pointcloud(dummy_points, self.trajectory_pub, header, color=(0, 255, 0, 255))
        self.publish_pointcloud(dummy_points, self.predicted_pub, header, color=None)

        self.get_logger().info("Trajectory data reset and dummy point published!")
        return response

    def publish_pointcloud(self, points_array: np.ndarray, publisher, header: Header, color=None):
        points = []
        if color is not None:
            r, g, b, a = color
            for p in points_array:
                rgba = struct.unpack('<I', struct.pack('<BBBB', b, g, r, a))[0]
                points.append([float(p[0]), float(p[1]), float(p[2]), int(rgba)])
        else:
            for p in points_array:
                points.append([float(p[0]), float(p[1]), float(p[2]), int(p[3])])

        flat_points = b''.join([struct.pack('<fffI', p[0], p[1], p[2], int(p[3])) for p in points])

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
