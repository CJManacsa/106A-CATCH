import rclpy
from rclpy.node import Node
from rclpy.duration import Duration

from tf2_ros import Buffer, TransformListener, TransformBroadcaster, TransformException
from geometry_msgs.msg import TransformStamped
from ros2_aruco_interfaces.srv import StoreTransform
import numpy as np


class ArucoStaticTFNode(Node):

    def __init__(self):
        super().__init__('aruco_static_tf_node')

        # Listen to live TF tree
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        # Broadcast transforms continuously
        self.broadcaster = TransformBroadcaster(self)

        # Store recent transforms for averaging
        self.recent_transforms = {}  # key: (parent, child), value: list of TransformStamped

        # Service
        self.srv = self.create_service(
            StoreTransform,
            'store_transform',
            self.store_transform
        )

        # Timer to rebroadcast averaged transforms
        self.timer = self.create_timer(0.1, self.broadcast_averaged_transforms)

        # Max history for averaging
        self.max_history = 10

        self.get_logger().info("Aruco Static TF Node ready.")

    def store_transform(self, request, response):
        parent = request.parent_frame
        child = request.child_frame

        try:
            # Lookup the live transform
            t = self.tf_buffer.lookup_transform(
                parent,
                child,
                rclpy.time.Time(),
                timeout=Duration(seconds=1.0)
            )

            key = (parent, child)
            if key not in self.recent_transforms:
                self.recent_transforms[key] = []

            # Keep last max_history transforms
            self.recent_transforms[key].append(t)
            if len(self.recent_transforms[key]) > self.max_history:
                self.recent_transforms[key].pop(0)

            msg = f"Stored TF reading {parent} -> {child}"
            self.get_logger().info(msg)
            response.success = True
            response.message = msg

        except TransformException as e:
            response.success = False
            response.message = f"TF lookup failed: {e}"
            self.get_logger().error(response.message)

        return response

    def broadcast_averaged_transforms(self):
        now = self.get_clock().now().to_msg()

        for (parent, child), transforms in self.recent_transforms.items():
            if not transforms:
                continue

            # Average translation
            translations = np.array([
                [t.transform.translation.x,
                 t.transform.translation.y,
                 t.transform.translation.z]
                for t in transforms
            ])
            avg_trans = np.mean(translations, axis=0)

            # Average rotation using quaternions
            quats = np.array([
                [t.transform.rotation.x,
                 t.transform.rotation.y,
                 t.transform.rotation.z,
                 t.transform.rotation.w]
                for t in transforms
            ])
            # Simple quaternion averaging (normalize sum)
            q_avg = np.sum(quats, axis=0)
            q_avg /= np.linalg.norm(q_avg)

            tf_msg = TransformStamped()
            tf_msg.header.stamp = now
            tf_msg.header.frame_id = parent
            tf_msg.child_frame_id = child
            tf_msg.transform.translation.x = avg_trans[0]
            tf_msg.transform.translation.y = avg_trans[1]
            tf_msg.transform.translation.z = avg_trans[2]
            tf_msg.transform.rotation.x = q_avg[0]
            tf_msg.transform.rotation.y = q_avg[1]
            tf_msg.transform.rotation.z = q_avg[2]
            tf_msg.transform.rotation.w = q_avg[3]

            self.broadcaster.sendTransform(tf_msg)


def main(args=None):
    rclpy.init(args=args)
    node = ArucoStaticTFNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
