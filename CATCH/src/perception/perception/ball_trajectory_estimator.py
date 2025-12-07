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
    def __init__(self):
        self.g = 9.81  # +Y downward
        self.x = np.zeros((6, 1))  # [x, y, z, vx, vy, vz]
        self.P = np.eye(6)
        self.P[0:3,0:3] *= 1.0
        self.P[3:6,3:6] *= 2000.0
        self.Q = np.eye(6)
        self.Q[0:3,0:3] *= 0.0001
        self.Q[3:6,3:6] *= 0.25
        self.R = np.eye(6)
        self.R[0:3,0:3] *= 0.0015
        self.R[3:6,3:6] *= 0.15
        self.H = np.eye(6)

    def predict(self, dt):
        F = np.eye(6)
        F[0,3] = F[1,4] = F[2,5] = dt
        B = np.zeros((6,1))
        B[1,0] = 0.5*self.g*dt**2
        B[4,0] = self.g*dt
        self.x = F @ self.x + B
        self.P = F @ self.P @ F.T + self.Q

    def update(self, meas):
        z = meas.reshape((6,1))
        y = z - self.H @ self.x
        S = self.H @ self.P @ self.H.T + self.R
        K = self.P @ self.H.T @ np.linalg.inv(S)
        self.x = self.x + K @ y
        self.P = (np.eye(6) - K @ self.H) @ self.P

class BallTrajectoryEstimator(Node):
    def __init__(self):
        super().__init__('ball_trajectory_estimator')
        self.sub = self.create_subscription(PointVel, '/ball_state', self.ball_callback, 10)
        self.trajectory_pub = self.create_publisher(PointCloud2, '/ball_trajectory', 1)
        self.predicted_pub = self.create_publisher(PointCloud2, '/ball_predicted_trajectory', 1)
        self.latest_pred_pub = self.create_publisher(PointCloud2, '/ball_latest_predicted_trajectory', 1)

        self.reset_srv = self.create_service(Empty, 'reset_trajectory_estimator', self.reset_callback)

        self.positions = deque(maxlen=20)
        self.predicted_trajs = deque(maxlen=20)
        self.kf = KalmanFilter3D()
        self.kf.P[3:6, 3:6] = np.eye(3) * 5.0  # reduced vel uncertainty
        self.last_time = None
        self.header_frame = None
        self.pred_points = 40

        # --- New: count valid points ---
        self.valid_points_received = 0
        self.max_valid_points = 5  # stop publishing after this

    def ball_callback(self, msg: PointVel):
        if self.valid_points_received >= self.max_valid_points:
            return  # stop processing after 5 valid points

        curr_time = msg.header.stamp.sec + msg.header.stamp.nanosec*1e-9
        dt = max(curr_time - self.last_time, 1e-6) if self.last_time is not None else (1.0/60.0)
        self.last_time = curr_time
        self.header_frame = msg.header.frame_id

        # --- Append and smooth positions ---
        self.positions.append([msg.x, msg.y, msg.z])
        pos_array = np.array(self.positions)
        N = min(5, len(pos_array))
        if N >= 2:
            xs = pos_array[-N:,0]
            zs = pos_array[-N:,2]
            a, b = np.polyfit(xs, zs, 1)
            pos_array[-1,2] = a*xs[-1] + b
            self.positions[-1][2] = pos_array[-1,2]

        # --- Compute velocity ---
        if len(pos_array) >= 2:
            dx, dy, dz = pos_array[-1] - pos_array[-2]
            vx, vy, vz = dx/dt, dy/dt, dz/dt
            if len(self.positions) == 2:
                self.kf.x[3,0] = vx
                self.kf.x[4,0] = vy
                self.kf.x[5,0] = vz
        else:
            vx = vy = vz = 0.0

        meas = np.array([pos_array[-1,0], pos_array[-1,1], pos_array[-1,2], vx, vy, vz])

        # Kalman update
        self.kf.predict(dt)
        self.kf.update(meas)
        x, y, z, vx, vy, vz = self.kf.x.flatten()
        self.positions[-1] = [x, y, z]

        # --- Publish filtered trajectory ---
        self.publish_pointcloud(np.array(self.positions), self.trajectory_pub, msg.header, color=(0,255,0,255))

        # Predict future trajectory
        g = 9.81
        pred = []
        for i in range(1, self.pred_points+1):
            t = i*dt
            xp = x + vx*t
            yp = y + vy*t + 0.5*g*t**2
            zp = z + vz*t
            pred.append([xp, yp, zp])
        pred_array = np.array(pred)

        # Store older predictions
        if not hasattr(self, "last_pred"):
            self.last_pred = None
        if self.last_pred is not None:
            self.predicted_trajs.append(self.last_pred)
        self.last_pred = pred_array

        # NEW: publish only newest prediction (cyan)
        self.publish_pointcloud(pred_array, self.latest_pred_pub, msg.header, color=(0,255,255,255))

        # Fade older predictions for big topic
        all_points = []
        n = len(self.predicted_trajs)
        for i, traj in enumerate(self.predicted_trajs):
            fade = (i+1)/n
            r, g_col, b_col, a = 255, int(255*fade), 0, 255
            for p in traj:
                rgba = struct.unpack('<I', struct.pack('<BBBB', b_col, g_col, r, a))[0]
                all_points.append([p[0], p[1], p[2], rgba])
        self.publish_pointcloud(np.array(all_points), self.predicted_pub, msg.header, color=None)

        # --- Increment valid points counter ---
        self.valid_points_received += 1

    def reset_callback(self, req, res):
        self.positions.clear()
        self.predicted_trajs.clear()
        self.kf = KalmanFilter3D()
        self.last_time = None
        self.valid_points_received = 0  # reset counter

        header = Header()
        header.stamp = self.get_clock().now().to_msg()
        header.frame_id = self.header_frame if self.header_frame else "world"

        dummy = np.array([[0.0, 0.0, -10.0, 0]], dtype=np.float32)
        self.publish_pointcloud(dummy, self.trajectory_pub, header, color=(0,255,0,255))
        self.publish_pointcloud(dummy, self.predicted_pub, header, color=None)
        self.publish_pointcloud(dummy, self.latest_pred_pub, header, color=(255,255,0,255))
        self.get_logger().info("Trajectory reset.")

        # Fire-and-forget ClosestPredictedPoint reset
        client = self.create_client(Empty, "reset_closest_predicted_point")
        if client.wait_for_service(timeout_sec=1.0):
            req2 = Empty.Request()
            client.call_async(req2)
            self.get_logger().info("Triggered reset on ClosestPredictedPoint asynchronously.")
        else:
            self.get_logger().warn("ClosestPredictedPoint reset service not available.")
        return res

    def publish_pointcloud(self, points_array, publisher, header, color=None):
        if points_array.size == 0:
            return
        pts = []
        if color is not None:
            r, g, b, a = color
            for p in points_array:
                x, y, z = np.clip(p[:3], -1e6, 1e6)
                rgba = struct.unpack('<I', struct.pack('<BBBB', b, g, r, a))[0]
                pts.append([float(x), float(y), float(z), rgba])
        else:
            for p in points_array:
                if len(p) < 4:
                    continue
                x, y, z, rgba = p
                x, y, z = np.clip([x, y, z], -1e6, 1e6)
                pts.append([float(x), float(y), float(z), int(rgba)])
        if len(pts) == 0:
            return
        flat = b''.join([struct.pack('<fffI', *p) for p in pts])
        msg = PointCloud2()
        msg.header = header
        msg.height = 1
        msg.width = len(pts)
        msg.is_dense = True
        msg.is_bigendian = False
        msg.fields = [
            PointField(name='x', offset=0, datatype=PointField.FLOAT32, count=1),
            PointField(name='y', offset=4, datatype=PointField.FLOAT32, count=1),
            PointField(name='z', offset=8, datatype=PointField.FLOAT32, count=1),
            PointField(name='rgba', offset=12, datatype=PointField.UINT32, count=1),
        ]
        msg.point_step = 16
        msg.row_step = msg.point_step * len(pts)
        msg.data = flat
        publisher.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = BallTrajectoryEstimator()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
