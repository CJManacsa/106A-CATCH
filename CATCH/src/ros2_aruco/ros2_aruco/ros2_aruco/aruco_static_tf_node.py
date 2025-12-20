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

        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.broadcaster = TransformBroadcaster(self)

        # Will hold final averaged transforms
        self.final_transforms = {}  # key: (parent, child) -> TransformStamped

        self.srv = self.create_service(
            StoreTransform,
            'store_transform',
            self.store_transform
        )

        self.timer = self.create_timer(0.1, self.broadcast_final_transforms)

        self.samples_to_collect = 100

        self.get_logger().info("Aruco Static TF Node ready.")

    def store_transform(self, request, response):
        parent = request.parent_frame
        child = request.child_frame
        key = (parent, child)

        translations = []
        quaternions = []

        self.get_logger().info(f"Sampling {parent}->{child} transform {self.samples_to_collect} times...")

        for i in range(self.samples_to_collect):
            try:
                t = self.tf_buffer.lookup_transform(
                    parent,
                    child,
                    rclpy.time.Time(),
                    timeout=Duration(seconds=1.0)
                )

                translations.append([
                    t.transform.translation.x,
                    t.transform.translation.y,
                    t.transform.translation.z
                ])

                quaternions.append([
                    t.transform.rotation.x,
                    t.transform.rotation.y,
                    t.transform.rotation.z,
                    t.transform.rotation.w
                ])

                rclpy.spin_once(self, timeout_sec=0.01)

            except TransformException as e:
                response.success = False
                response.message = f"TF lookup failed during sampling: {e}"
                self.get_logger().error(response.message)
                return response

        translations = np.array(translations)
        quaternions = np.array(quaternions)

        avg_trans = np.mean(translations, axis=0)

        q_avg = np.sum(quaternions, axis=0)
        q_avg /= np.linalg.norm(q_avg)

        tf_msg = TransformStamped()
        tf_msg.header.frame_id = parent
        tf_msg.child_frame_id = child

        tf_msg.transform.translation.x = avg_trans[0]
        tf_msg.transform.translation.y = avg_trans[1]
        tf_msg.transform.translation.z = avg_trans[2]

        tf_msg.transform.rotation.x = q_avg[0]
        tf_msg.transform.rotation.y = q_avg[1]
        tf_msg.transform.rotation.z = q_avg[2]
        tf_msg.transform.rotation.w = q_avg[3]

        self.final_transforms[key] = tf_msg

        response.success = True
        response.message = f"Averaged transform stored for {parent}->{child}"

        self.get_logger().info(response.message)
        return response

    def broadcast_final_transforms(self):
        now = self.get_clock().now().to_msg()
        for tf_msg in self.final_transforms.values():
            tf_msg.header.stamp = now
            self.broadcaster.sendTransform(tf_msg)


def main(args=None):
    rclpy.init(args=args)
    node = ArucoStaticTFNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    rclpy.shutdown()


if __name__ == "__main__":
    main()