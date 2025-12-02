#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from tf2_ros import TransformListener, Buffer

class PositionPrinter(Node):
    def __init__(self):
        super().__init__('position_printer')
        
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        
        self.timer = self.create_timer(1.0, self.print_ee_position)
    
    def print_ee_position(self):
        try:
            # Get transform from base to end-effector
            # Common frame names: 'tool0', 'ee_link', 'wrist_3_link'
            transform = self.tf_buffer.lookup_transform(
                'base_link',      # or 'base'
                'wrist_3_link',          # or 'ee_link' or 'wrist_3_link'
                rclpy.time.Time()
            )
            
            pos = transform.transform.translation
            self.get_logger().info(
                f'End-effector: x={pos.x:.3f}, y={pos.y:.3f}, z={pos.z:.3f}'
            )
        except Exception as e:
            self.get_logger().warn(f'Could not get transform: {e}')

def main():
    rclpy.init()
    node = PositionPrinter()
    rclpy.spin(node)

if __name__ == '__main__':
    main()