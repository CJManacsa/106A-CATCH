import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2, PointField
from std_msgs.msg import Header
import numpy as np
from collections import deque
import struct
from catch_custom_msgs.msg import PointVel
from std_srvs.srv import Empty


class KalmanFilter3D:
    def __init__(self, dt=0.033):
        self.dt = dt
        self.g = 9.81   # +Y downward

        # -------------------------------
        # State vector: [x y z vx vy vz]
        # -------------------------------
        self.x = np.zeros((6, 1))

        # -------------------------------
        # INITIAL UNCERTAINTY
        # -------------------------------
        self.P = np.eye(6)
        self.P[0:3, 0:3] *= 1.0       # very confident in initial position
        self.P[3:6, 3:6] *= 2000.0    # DO NOT trust initial velocity at all

        # -------------------------------
        # PROCESS NOISE (model freedom)
        # -------------------------------
        self.Q = np.eye(6)
        self.Q[0:3, 0:3] *= 0.0001    # very stable positions
        self.Q[3:6, 3:6] *= 0.25      # velocities adapt quickly

        # -------------------------------
        # MEASUREMENT NOISE
        # -------------------------------
        self.R = np.eye(6)
        self.R[0:3, 0:3] *= 0.0015    # positions: trust strongly
        self.R[3:6, 3:6] *= 0.15      # velocities: trust, but not blindly

        self.H = np.eye(6)

    def predict(self):
        dt = self.dt
        g = self.g

        # -------------------------------
        # State transition matrix
        # -------------------------------
        F = np.eye(6)
        F[0, 3] = dt   # x += vx*dt
        F[1, 4] = dt   # y += vy*dt
        F[2, 5] = dt   # z += vz*dt

        # -------------------------------
        # Gravity (downwards +Y)
        # -------------------------------
        B = np.zeros((6, 1))
        B[1, 0] = 0.5 * g * dt * dt   # affects y position
        B[4, 0] = g * dt              # affects y velocity

        # Predict state
        self.x = F @ self.x + B

        # Predict covariance
        self.P = F @ self.P @ F.T + self.Q

        return self.x.copy()

    def update(self, meas):
        z = meas.reshape((6, 1))

        # Innovation
        y = z - self.H @ self.x

        # Innovation covariance
        S = self.H @ self.P @ self.H.T + self.R

        # Kalman gain
        K = self.P @ self.H.T @ np.linalg.inv(S)

        # Updated state
        self.x = self.x + K @ y

        # Updated covariance
        I = np.eye(6)
        self.P = (I - K @ self.H) @ self.P

        return self.x.copy()

class BallTrajectoryEstimator(Node):
    def __init__(self):
        super().__init__('ball_trajectory_estimator')

        self.sub = self.create_subscription(PointVel, '/ball_state', self.ball_callback, 10)

        self.trajectory_pub = self.create_publisher(PointCloud2, '/ball_trajectory', 1)
        self.predicted_pub = self.create_publisher(PointCloud2, '/ball_predicted_trajectory', 1)

        self.reset_srv = self.create_service(Empty, 'reset_trajectory', self.reset_callback)

        self.pred_points = 20

        self.positions_history = deque(maxlen=20)
        self.predicted_trajs = deque(maxlen=20)

        self.header = None
        self.dt = 0.033

        # ✔ NEW Kalman filter
        self.kf = KalmanFilter3D(self.dt)

        self.get_logger().info("Ball Trajectory Estimator + Kalman Filter started.")

    def ball_callback(self, msg: PointVel):
        # Measurement vector
        meas = np.array([
            msg.x, msg.y, msg.z,
            msg.vx, msg.vy, msg.vz
        ])

        # Kalman filter update
        self.kf.predict()
        state = self.kf.update(meas)

        x, y, z, vx, vy, vz = state.flatten()

        # Save filtered position
        self.positions_history.append([x, y, z])
        positions_array = np.array(self.positions_history)

        self.header = msg.header

        # Green position history
        self.publish_pointcloud(positions_array, self.trajectory_pub, msg.header, color=(0, 255, 0, 255))

        # -------- Predict Future Trajectory (yellow) --------
        g = 9.81
        predicted = []
        px, py, pz = x, y, z
        vx0, vy0, vz0 = vx, vy, vz

        for i in range(1, self.pred_points + 1):
            t = i * self.dt
            xp = px + vx0 * t
            yp = py + vy0 * t + 0.5 * g * t * t
            zp = pz + vz0 * t
            predicted.append([xp, yp, zp])

        predicted_array = np.array(predicted)
        self.predicted_trajs.append(predicted_array)

        # Fade older predictions
        all_points = []
        n = len(self.predicted_trajs)
        for i, traj in enumerate(self.predicted_trajs):
            fade = (i + 1) / n
            r, g_col, b_col, alpha = 255, int(255 * fade), 0, 255 #int(255 * fade)
            for p in traj:
                rgba = struct.unpack('<I', struct.pack('<BBBB', b_col, g_col, r, alpha))[0]
                all_points.append([p[0], p[1], p[2], rgba])

        all_points_array = np.array(all_points)
        self.publish_pointcloud(all_points_array, self.predicted_pub, msg.header, color=None)

    def reset_callback(self, request, response):
        self.positions_history.clear()
        self.predicted_trajs.clear()

        # Reset Kalman filter
        self.kf = KalmanFilter3D(self.dt)

        dummy = np.array([[0.0, 0.0, -100.0, 0]], dtype=np.float32)
        header = Header()
        header.stamp = self.get_clock().now().to_msg()
        header.frame_id = self.header.frame_id if self.header else "world"

        self.publish_pointcloud(dummy, self.trajectory_pub, header, color=(0, 255, 0, 255))
        self.publish_pointcloud(dummy, self.predicted_pub, header, color=None)

        self.get_logger().info("Trajectory reset.")
        return response

    def publish_pointcloud(self, points_array, publisher, header, color=None):
        points = []
        if color is not None:
            r, g, b, a = color
            for p in points_array:
                rgba = struct.unpack('<I', struct.pack('<BBBB', b, g, r, a))[0]
                points.append([float(p[0]), float(p[1]), float(p[2]), rgba])
        else:
            for p in points_array:
                points.append([float(p[0]), float(p[1]), float(p[2]), int(p[3])])

        flat = b''.join([struct.pack('<fffI', p[0], p[1], p[2], p[3]) for p in points])

        msg = PointCloud2()
        msg.header = header
        msg.height = 1
        msg.width = len(points)
        msg.is_dense = True
        msg.is_bigendian = False
        msg.fields = [
            PointField(name='x', offset=0, datatype=PointField.FLOAT32, count=1),
            PointField(name='y', offset=4, datatype=PointField.FLOAT32, count=1),
            PointField(name='z', offset=8, datatype=PointField.FLOAT32, count=1),
            PointField(name='rgba', offset=12, datatype=PointField.UINT32, count=1),
        ]
        msg.point_step = 16
        msg.row_step = msg.point_step * len(points)
        msg.data = flat
        publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = BallTrajectoryEstimator()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
