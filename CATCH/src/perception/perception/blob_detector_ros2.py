#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import cv2
import time
import numpy as np

from sensor_msgs.msg import Image
from cv_bridge import CvBridge

from perception.blob_detector import (
    blob_detect, blur_outside, draw_window, draw_frame, draw_keypoints
)

class BlobDetectorNode(Node):
    def __init__(self):
        super().__init__('blob_detector')
        self.get_logger().info("Starting Blob Detector Node (ROS2)")

        # --- HSV thresholds
        self.thr_min = (95, 118, 53)
        self.thr_max = (107, 255, 255)

        # Region of interest (full frame)
        self.detection_window = [0.0, 0.0, 1.0, 1.0]
        self.blur = 0

        # --- Blob detector parameters
        params = cv2.SimpleBlobDetector_Params()
        params.filterByArea = True
        params.minArea = 100
        params.maxArea = 1e6
        params.filterByCircularity = True
        params.minCircularity = 0.5
        params.filterByConvexity = True
        params.minConvexity = 0.5
        params.filterByInertia = False
        self.blob_params = params

        # --- CV Bridge
        self.bridge = CvBridge()

        # --- Subscribers
        self.image_sub = self.create_subscription(
            Image,
            '/camera/camera/color/image_raw',
            self.image_callback,
            10
        )

        # --- Publishers
        self.image_blob_pub = self.create_publisher(Image, '/blob/image_blob', 1)
        self.image_mask_true_pub = self.create_publisher(Image, '/blob/image_mask_true', 1)
        self.image_mask_pub = self.create_publisher(Image, '/blob/image_mask', 1)

        self._t0 = time.time()
        self.get_logger().info("Subscribed to /camera/camera/color/image_raw")

    def image_callback(self, msg: Image):
        # --- Convert ROS Image → OpenCV
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        rows, cols, _ = frame.shape

        if rows < 60 or cols < 60:
            return

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

        # --- Publish debug image with correct header
        img_blob_msg = self.bridge.cv2_to_imgmsg(frame_disp, "bgr8")
        img_blob_msg.header = msg.header
        self.image_blob_pub.publish(img_blob_msg)

        # --- Publish raw mask (with timestamp)
        mask_true_msg = self.bridge.cv2_to_imgmsg(mask, "8UC1")
        mask_true_msg.header = msg.header
        self.image_mask_true_pub.publish(mask_true_msg)

        # --- Publish processed mask (white mask if no blobs)
        if len(keypoints) == 0:
            mask_proc = np.ones_like(mask, dtype=np.uint8) * 255
        else:
            mask_proc = mask
        mask_proc_msg = self.bridge.cv2_to_imgmsg(mask_proc, "8UC1")
        mask_proc_msg.header = msg.header
        self.image_mask_pub.publish(mask_proc_msg)

        # --- Compute and log FPS
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
