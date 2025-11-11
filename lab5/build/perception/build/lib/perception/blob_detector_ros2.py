#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import cv2
import time
import numpy as np

from sensor_msgs.msg import Image
from geometry_msgs.msg import Point
from cv_bridge import CvBridge

# --- Import your existing blob detection functions
# Ensure this is in your PYTHONPATH or same folder
from perception.blob_detector import blob_detect, blur_outside, draw_window, draw_frame, draw_keypoints, get_blob_relative_position


class BlobDetectorNode(Node):
    def __init__(self):
        super().__init__('blob_detector')
        self.get_logger().info("Starting Blob Detector Node (ROS2)")

        # --- Parameters (tweak with ColorIdentifier)
        self.thr_min = (92, 197, 50)
        self.thr_max = (106, 255, 255)
        self.blur = 0
        self.detection_window = [0.0, 0.0, 1.0, 1.0]

        # --- Configure blob parameters
        params = cv2.SimpleBlobDetector_Params()
        params.filterByArea = True
        params.minArea = 100
        params.maxArea = 1e6
        params.filterByCircularity = True
        params.minCircularity = 0.6
        params.filterByConvexity = True
        params.minConvexity = 0.2
        params.filterByInertia = True
        params.minInertiaRatio = 0.7
        self.blob_params = params

        # --- CV Bridge
        self.bridge = CvBridge()

        # --- Topics
        self.image_sub = self.create_subscription(
            Image,
            '/camera/camera/color/image_raw',  # RealSense topic
            self.image_callback,
            10
        )

        self.image_blob_pub = self.create_publisher(Image, '/blob/image_blob', 1)
        self.image_mask_pub = self.create_publisher(Image, '/blob/image_mask', 1)
        self.point_blob_pub = self.create_publisher(Point, '/blob/point_blob', 1)

        self._t0 = time.time()
        self.get_logger().info("Subscribed to /camera/camera/color/image_raw")

    def image_callback(self, msg):
        # --- Convert ROS Image → OpenCV
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        rows, cols, _ = frame.shape

        if cols > 60 and rows > 60:
            # --- Detect blobs
            keypoints, mask = blob_detect(
                frame, self.thr_min, self.thr_max, self.blur,
                blob_params=self.blob_params,
                search_window=self.detection_window
            )

            # --- Draw visualization
            frame_disp = blur_outside(frame.copy(), 10, self.detection_window)
            frame_disp = draw_window(frame_disp, self.detection_window, line=1)
            frame_disp = draw_frame(frame_disp)
            frame_disp = draw_keypoints(frame_disp, keypoints)

            # --- Publish debug images
            self.image_blob_pub.publish(self.bridge.cv2_to_imgmsg(frame_disp, "bgr8"))
            self.image_mask_pub.publish(self.bridge.cv2_to_imgmsg(mask, "8UC1"))

            # --- Publish first blob position and draw a small circle at the blob center
            for i, kp in enumerate(keypoints):
                # Get the blob's relative position in the image
                x, y = get_blob_relative_position(frame, kp)
                
                # Draw a small circle at the blob's center
                radius = 10  # You can adjust the radius size as needed
                color = (0, 255, 0)  # Circle color in BGR format (Green in this case)
                thickness = 2  # Line thickness (2 pixels)

                # Draw the circle on the frame
                cv2.circle(frame_disp, (int(x), int(y)), radius, color, thickness)

                # Create a Point message and publish it
                point_msg = Point()
                point_msg.x = float(x)
                point_msg.y = float(y)
                self.point_blob_pub.publish(point_msg)

                self.get_logger().info(f"Blob {i}: x={x:.2f}, y={y:.2f}")

                # Only publish the first detected blob for now
                break

            # --- Compute FPS
            fps = 1.0 / (time.time() - self._t0)
            self._t0 = time.time()
            self.get_logger().info(f"FPS: {fps:.1f}")



def main(args=None):
    rclpy.init(args=args)
    node = BlobDetectorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
