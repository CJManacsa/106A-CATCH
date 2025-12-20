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
        self.positions_history = deque(maxlen=10)
        self.velocities_history = deque(maxlen=10)
        self.predicted_trajs = deque(maxlen=10)

        self.header = None

        self.get_logger().info("Ball Trajectory Estimator node started.")



    def reset_callback(self, request, response):
        # Clear histories
        self.positions_history.clear()
        self.velocities_history.clear()
        self.predicted_trajs.clear()

        # Publish a single dummy point far below scene to clear RViz
        dummy_points = np.array([[0.0, 0.0, -100.0, 0]], dtype=np.float32)
        header = Header()
        header.stamp = self.get_clock().now().to_msg()

        # Use last received header frame, or fallback to "world"
        if self.header is not None:
            header.frame_id = self.header.frame_id
        else:
            header.frame_id = "world"

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
