#!/usr/bin/env python3
import cv2
import numpy as np
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from geometry_msgs.msg import PointStamped
from cv_bridge import CvBridge
from builtin_interfaces.msg import Time as TimeMsg


class BallTracker(Node):
    """Simple HSV-based color tracker for the 106A project."""

    def __init__(self):
        super().__init__("ball_tracker")

        # === Parameters ===
        self.declare_parameter("camera_topic", "/camera/color/image_raw")
        self.declare_parameter("resize_width", 320)
        self.declare_parameter("resize_height", 240)
        self.declare_parameter("h_low", 5)
        self.declare_parameter("s_low", 120)
        self.declare_parameter("v_low", 100)
        self.declare_parameter("h_high", 20)
        self.declare_parameter("s_high", 255)
        self.declare_parameter("v_high", 255)
        self.declare_parameter("min_area_px", 150)
        self.declare_parameter("publish_debug_image", True)

        self.bridge = CvBridge()

        # Load params
        self.topic = self.get_parameter("camera_topic").value
        self.w = int(self.get_parameter("resize_width").value)
        self.h = int(self.get_parameter("resize_height").value)
        self.lower = np.array([
            int(self.get_parameter("h_low").value),
            int(self.get_parameter("s_low").value),
            int(self.get_parameter("v_low").value),
        ])
        self.upper = np.array([
            int(self.get_parameter("h_high").value),
            int(self.get_parameter("s_high").value),
            int(self.get_parameter("v_high").value),
        ])
        self.min_area = int(self.get_parameter("min_area_px").value)
        self.pub_dbg = bool(self.get_parameter("publish_debug_image").value)

        # === I/O ===
        self.sub = self.create_subscription(Image, self.topic, self.image_cb, 2)
        self.pub_centroid = self.create_publisher(PointStamped, "/ball/centroid", 10)
        if self.pub_dbg:
            self.pub_debug = self.create_publisher(Image, "/ball/debug_image", 1)
        else:
            self.pub_debug = None

        self.get_logger().info(f"Tracking color on topic {self.topic}")

    # ==========================================================
    def image_cb(self, msg: Image):
        """Main callback for camera frames."""
        try:
            frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
        except Exception as e:
            self.get_logger().warn(f"cv_bridge error: {e}")
            return

        frame = cv2.resize(frame, (self.w, self.h))
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.lower, self.upper)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        best = max(contours, key=cv2.contourArea, default=None)

        if best is not None and cv2.contourArea(best) > self.min_area:
            M = cv2.moments(best)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                msg_pt = PointStamped()
                msg_pt.header.stamp = TimeMsg(sec=msg.header.stamp.sec,
                                              nanosec=msg.header.stamp.nanosec)
                msg_pt.header.frame_id = msg.header.frame_id
                msg_pt.point.x = float(cx)
                msg_pt.point.y = float(cy)
                msg_pt.point.z = 0.0
                self.pub_centroid.publish(msg_pt)
        else:
            cx = cy = None

        if self.pub_debug:
            dbg = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
            if best is not None and cx is not None:
                cv2.drawContours(dbg, [best], -1, (0, 255, 0), 2)
                cv2.circle(dbg, (cx, cy), 4, (255, 0, 0), -1)
            dbg_msg = self.bridge.cv2_to_imgmsg(dbg, encoding="bgr8")
            dbg_msg.header = msg.header
            self.pub_debug.publish(dbg_msg)


def main(args=None):
    rclpy.init(args=args)
    node = BallTracker()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()