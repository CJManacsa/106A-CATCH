import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np

class BallTracker(Node):
    def __init__(self):
        super().__init__('ball_tracker')
        self.bridge = CvBridge()
        self.sub = self.create_subscription(Image, '/camera/color/image_raw', self.callback, 10)
        self.get_logger().info("Ball tracker started.")

    def callback(self, msg):
        img = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Example HSV range for a red ball (you’ll update these from the identifier)
        lower = np.array([16, 53, 122])
        upper = np.array([40, 141, 205])
        mask = cv2.inRange(hsv, lower, upper)

        # Find the largest contour
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            c = max(contours, key=cv2.contourArea)
            (x, y), radius = cv2.minEnclosingCircle(c)
            if radius > 10:
                cv2.circle(img, (int(x), int(y)), int(radius), (0, 255, 0), 2)
                self.get_logger().info(f"Ball center: ({x:.1f}, {y:.1f}) radius: {radius:.1f}")

        cv2.imshow("mask", mask)
        cv2.imshow("tracking", img)
        cv2.waitKey(1)

def main(args=None):
    rclpy.init(args=args)
    node = BallTracker()
    rclpy.spin(node)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
