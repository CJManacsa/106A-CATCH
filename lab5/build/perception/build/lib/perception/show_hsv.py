import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np


class HSVViewer(Node):
    def __init__(self):
        super().__init__("hsv_viewer")
        self.declare_parameter("camera_topic", "/camera/camera/color/image_raw")
        self.topic = self.get_parameter("camera_topic").value
        self.bridge = CvBridge()
        self.sub = self.create_subscription(Image, self.topic, self.image_cb, 10)
        self.get_logger().info(f"Subscribed to {self.topic}")

    def image_cb(self, msg):
        try:
            frame = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        except Exception as e:
            self.get_logger().warn(f"cv_bridge error: {e}")
            return

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        combined = np.hstack((
            frame,
            cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        ))

        cv2.imshow("HSV Viewer (press q to quit)", combined)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            rclpy.shutdown()


def main():
    rclpy.init()
    node = HSVViewer()
    rclpy.spin(node)
    node.destroy_node()
    cv2.destroyAllWindows()
    rclpy.shutdown()


if __name__ == "__main__":
    main()