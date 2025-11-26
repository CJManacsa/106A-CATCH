import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2, PointField
from std_msgs.msg import Header
import numpy as np
from collections import deque
import struct
from catch_custom_msgs.msg import PointVel


class BallTrajectoryEstimator(Node):
    def __init__(self):
        super().__init__('ball_trajectory_estimator')

        # Subscribe to ball state topic
        self.sub = self.create_subscription(
            PointVel,
            '/ball_state',
            self.ball_callback,
            10
        )

        # Publishers
        self.trajectory_pub = self.create_publisher(PointCloud2, '/ball_trajectory', 1)
        self.predicted_pub = self.create_publisher(PointCloud2, '/ball_predicted_trajectory', 1)

        # History storage
        self.positions = deque(maxlen=10)
        self.velocities = deque(maxlen=10)
        self.predicted_trajs = deque(maxlen=10)  # store last 10 predicted trajectories

        self.get_logger().info("Ball Trajectory Estimator node started.")

    def smooth_latest_z(self, array: np.ndarray, window=3):
        """Smooth only the latest point's z (or vz) based on previous points."""
        N = len(array)
        if N < 2:
            return array
        start = max(0, N - window)
        z_to_average = array[start:, 2]
        array[-1, 2] = np.mean(z_to_average)
        return array

    def ball_callback(self, msg: PointVel):
        # Append current position and velocity
        pos = [msg.x, msg.y, msg.z]
        vel = [msg.vx, msg.vy, msg.vz]
        self.positions.append(pos)
        self.velocities.append(vel)

        if len(self.positions) < 2:
            return  # need at least 2 points to predict

        # Convert to arrays
        positions_array = np.array(self.positions)
        velocities_array = np.array(self.velocities)

        # Smooth only the newest z values
        positions_array = self.smooth_latest_z(positions_array, window=7)
        velocities_array = self.smooth_latest_z(velocities_array, window=7)

        dt = 0.033  # approximate time step

        # --- PUBLISH HISTORY TRAIL (NEON GREEN) ---
        self.publish_pointcloud(
            positions_array,
            self.trajectory_pub,
            msg.header,
            color=(0, 255, 0, 255)
        )

        # --- Use smoothed velocity for prediction ---
        v0 = velocities_array[-1]

        # --- PREDICT PROJECTILE TRAJECTORY ---
        g = 9.81
        num_predicted_points = 30
        t_step = dt
        last_pos = positions_array[-1]
        predicted_points = []

        for i in range(1, num_predicted_points + 1):
            t = i * t_step
            x = last_pos[0] + v0[0] * t
            y = last_pos[1] + v0[1] * t + 0.5 * g * t**2
            z = last_pos[2] + v0[2] * t
            predicted_points.append([x, y, z])

        predicted_array = np.array(predicted_points)
        predicted_array = self.smooth_latest_z(predicted_array, window=3)

        # Store this predicted trajectory
        self.predicted_trajs.append(predicted_array)

        # --- MERGE PREDICTIONS WITH NEON YELLOW → RED FADE + OPACITY FADE ---
        all_points = []
        N = len(self.predicted_trajs)

        for i, traj in enumerate(self.predicted_trajs):
            fade = (i + 1) / N  # 1 = newest, 0 = oldest

            # --- COLOR FADE ---
            # Newest = neon yellow
            # Older = fade toward red
            r = 255
            g_col = int(255 * fade)   # newest = 255, oldest = 0
            b_col = 0

            # --- OPACITY FADE ---
            alpha = int(255 * fade)

            for p in traj:
                rgba = struct.unpack(
                    '<I',
                    struct.pack('<BBBB', b_col, g_col, r, alpha)
                )[0]
                all_points.append([float(p[0]), float(p[1]), float(p[2]), int(rgba)])

        # Convert to numpy array
        all_points_array = np.array(all_points)

        # --- PUBLISH MERGED TRAJECTORY CLOUD ---
        self.publish_pointcloud(
            all_points_array,
            self.predicted_pub,
            msg.header,
            color=None
        )

        # Log smoothed velocity
        self.get_logger().info(
            f"Smoothed last velocity: vx={v0[0]:.2f}, vy={v0[1]:.2f}, vz={v0[2]:.2f}"
        )

    def publish_pointcloud(self, points_array: np.ndarray, publisher, header: Header, color=None):
        """Publish a PointCloud2 given points array (Nx3 or Nx4 if color included)."""
        points = []

        if color is not None:
            r, g, b, a = color
            for p in points_array:
                rgba = struct.unpack('<I', struct.pack('<BBBB', b, g, r, a))[0]
                points.append([float(p[0]), float(p[1]), float(p[2]), int(rgba)])
        else:
            for p in points_array:
                points.append([float(p[0]), float(p[1]), float(p[2]), int(p[3])])

        flat_points = b''.join([
            struct.pack('<fffI', p[0], p[1], p[2], int(p[3]))
            for p in points
        ])

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
