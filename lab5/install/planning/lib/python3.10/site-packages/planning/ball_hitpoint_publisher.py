#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PointStamped
from builtin_interfaces.msg import Time

class BallHitpointPublisher(Node):
    def __init__(self):
        super().__init__('ball_hitpoint_publisher')

        # Publisher: topic name and msg type
        self.pub = self.create_publisher(PointStamped, 
                                         'ball_hitpoint_base', 
                                         10)

        # Publish at 10 Hz
        self.timer = self.create_timer(0.1, self.publish_point)

        # Example point — modify however you want
        self.x = 0.126
        self.y = 0.614
        self.z = 0.517

        self.get_logger().info("ball_hitpoint_publisher started.")

    def publish_point(self):
        msg = PointStamped()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'base_link'   # Make sure this matches your IK frame

        msg.point.x = self.x
        msg.point.y = self.y
        msg.point.z = self.z

        self.pub.publish(msg)
        self.get_logger().info(
            f"Published hitpoint: ({self.x:.3f}, {self.y:.3f}, {self.z:.3f})"
        )

def main(args=None):
    rclpy.init(args=args)
    node = BallHitpointPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
