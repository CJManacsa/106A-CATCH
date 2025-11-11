#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np

class ColorIdentifier(Node):
    def __init__(self):
        super().__init__('color_identifier')
        self.bridge = CvBridge()

        # Subscribe to RealSense color image
        self.subscription = self.create_subscription(
            Image,
            '/camera/camera/color/image_raw',
            self.image_callback,
            10)
        self.subscription  # prevent unused variable warning

        self.window_name = "Color Identifier"
        cv2.namedWindow(self.window_name)
        cv2.setMouseCallback(self.window_name, self.mouse_callback)
        self.current_frame = None

        self.get_logger().info("Click on the ball to identify its color (RGB + HSV). Press 'q' to quit.")

    def image_callback(self, msg):
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        self.current_frame = frame
        cv2.imshow(self.window_name, frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            rclpy.shutdown()

    def mouse_callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN and self.current_frame is not None:
            bgr = self.current_frame[y, x].astype(np.uint8)
            hsv = cv2.cvtColor(np.uint8([[bgr]]), cv2.COLOR_BGR2HSV)[0][0]
            print(f"\nClicked pixel at ({x}, {y}):")
            print(f"  BGR: {bgr}")
            print(f"  HSV: {hsv}")
            print("Record these values to build your color range.\n")

def main(args=None):
    rclpy.init(args=args)
    node = ColorIdentifier()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        cv2.destroyAllWindows()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
