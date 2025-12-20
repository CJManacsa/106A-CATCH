#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PointStamped
from mover_services.srv import MoveAbs

class BallHitpointPublisher(Node):
    def __init__(self):
        super().__init__('ball_hitpoint_publisher')
        
        # Publisher: topic name and msg type
        self.pub = self.create_publisher(
            PointStamped, 
            'ball_hitpoint_base', 
            10
        )
        
        # Create service instead of timer
        self.srv = self.create_service(
            MoveAbs,
            'publish_hitpoint',
            self.publish_point_callback
        )
        
        self.get_logger().info("Ball hitpoint publisher service ready!")
        self.get_logger().info("Call service: ros2 service call /publish_hitpoint mover_services/srv/MoveAbs \"{x: 0.234, y: 0.608, z: 0.428}\"")
    
    def publish_point_callback(self, request, response):
        """Service callback - publishes point and returns success"""
        
        # Extract coordinates from service request
        x = request.x
        y = request.y
        z = request.z
        #0.134
        #0.608
        #0.428
        
        # Create and publish the message
        msg = PointStamped()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'base_link'
        msg.point.x = x
        msg.point.y = y
        msg.point.z = z
        
        self.pub.publish(msg)
        
        # Log the published point
        self.get_logger().info(
            f"Published hitpoint: ({x:.3f}, {y:.3f}, {z:.3f})"
        )
        
        # Set response
        response.success = True
        response.message = f"Successfully published point ({x:.3f}, {y:.3f}, {z:.3f})"
        
        return response

def main(args=None):
    rclpy.init(args=args)
    node = BallHitpointPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()