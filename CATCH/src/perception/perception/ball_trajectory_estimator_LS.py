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
        self.sub = self.create_subscription(PointVel, '/ball_state', self.ball_callback, 10)
        self.trajectory_pub = self.create_publisher(PointCloud2, '/ball_trajectory', 1)
        self.predicted_pub = self.create_publisher(PointCloud2, '/ball_predicted_trajectory', 1)
        self.latest_pred_pub = self.create_publisher(PointCloud2, '/ball_latest_predicted_trajectory', 1)

        self.reset_srv = self.create_service(Empty, 'reset_trajectory_estimator', self.reset_callback)

        self.positions = deque(maxlen=20)
        self.timestamps = deque(maxlen=5)
        self.predicted_trajs = deque(maxlen=20)
        self.last_time = None
        self.header_frame = None
        self.pred_points = 60
        self.g = 9.81

        self.valid_points_received = 0
        self.max_valid_points = 5

    def fit_projectile(self):
        """Fit projectile motion using least squares"""
        n = len(self.positions)
        if n < 3:
            return None
        
        # Get last 5 points
        pos = np.array(list(self.positions)[-5:])
        times = np.array(list(self.timestamps)[-5:])
        times = times - times[0]  # Relative time
        
        # Fit x(t) = x0 + vx*t (no acceleration in x)
        A = np.column_stack([np.ones(len(times)), times])
        x_coeffs = np.linalg.lstsq(A, pos[:,0], rcond=None)[0]
        
        # Fit z(t) = z0 + vz*t (no acceleration in z)
        z_coeffs = np.linalg.lstsq(A, pos[:,2], rcond=None)[0]
        
        # Fit y(t) = y0 + vy*t + 0.5*g*t^2
        A_quad = np.column_stack([np.ones(len(times)), times, times**2])
        y_coeffs = np.linalg.lstsq(A_quad, pos[:,1], rcond=None)[0]
        
        # Extract parameters at current time (last point)
        t = times[-1]
        x = x_coeffs[0] + x_coeffs[1] * t
        y = y_coeffs[0] + y_coeffs[1] * t + y_coeffs[2] * t**2
        z = z_coeffs[0] + z_coeffs[1] * t
        
        vx = x_coeffs[1]
        vz = z_coeffs[1]
        vy = y_coeffs[1] + 2 * y_coeffs[2] * t
        
        return x, y, z, vx, vy, vz

    def ball_callback(self, msg: PointVel):
        if self.valid_points_received >= self.max_valid_points:
            return

        curr_time = msg.header.stamp.sec + msg.header.stamp.nanosec*1e-9
        dt = max(curr_time - self.last_time, 1e-6) if self.last_time is not None else (1.0/60.0)
        self.last_time = curr_time
        self.header_frame = msg.header.frame_id

        # Store raw measurements
        self.positions.append([msg.x, msg.y, msg.z])
        self.timestamps.append(curr_time)

        # Fit projectile motion if we have enough points
        if len(self.positions) >= 3:
            result = self.fit_projectile()
            if result is not None:
                x, y, z, vx, vy, vz = result
                # Replace last position with fitted value
                self.positions[-1] = [x, y, z]
            else:
                x, y, z = self.positions[-1]
                vx = vy = vz = 0.0
        else:
            x, y, z = self.positions[-1]
            vx = vy = vz = 0.0

        # Publish filtered trajectory
        self.publish_pointcloud(np.array(self.positions), self.trajectory_pub, msg.header, color=(0,255,0,255))

        # Predict future trajectory
        pred = []
        for i in range(1, self.pred_points+1):
            t = i*dt
            xp = x + vx*t
            yp = y + vy*t + 0.5*self.g*t**2
            zp = z + vz*t
            pred.append([xp, yp, zp])
        pred_array = np.array(pred)

        # Store older predictions
        if not hasattr(self, "last_pred"):
            self.last_pred = None
        if self.last_pred is not None:
            self.predicted_trajs.append(self.last_pred)
        self.last_pred = pred_array

        # Publish newest prediction (cyan)
        self.publish_pointcloud(pred_array, self.latest_pred_pub, msg.header, color=(0,255,255,255))

        # Fade older predictions
        all_points = []
        n = len(self.predicted_trajs)
        for i, traj in enumerate(self.predicted_trajs):
            fade = (i+1)/n
            r, g_col, b_col, a = 255, int(255*fade), 0, 255
            for p in traj:
                rgba = struct.unpack('<I', struct.pack('<BBBB', b_col, g_col, r, a))[0]
                all_points.append([p[0], p[1], p[2], rgba])
        self.publish_pointcloud(np.array(all_points), self.predicted_pub, msg.header, color=None)

        self.valid_points_received += 1

    def reset_callback(self, req, res):
        self.positions.clear()
        self.timestamps.clear()
        self.predicted_trajs.clear()
        self.last_time = None
        self.valid_points_received = 0

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