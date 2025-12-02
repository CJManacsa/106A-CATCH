import rclpy
from rclpy.node import Node
from tf2_ros import Buffer, TransformListener
from geometry_msgs.msg import PointStamped
import tf2_geometry_msgs.tf2_geometry_msgs as tf2_geom


class TransformCubePose(Node):
    def __init__(self):
        super().__init__('transform_cube_pose')

        # TF2 buffer and listener
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        # Subscriber and publisher
        self.cube_pose_sub = self.create_subscription(
            PointStamped,
            '/cube_pose',
            self.cube_pose_callback,
            10
        )
        self.cube_pose_pub = self.create_publisher(PointStamped, '/transform_cube_pose', 10)

    def cube_pose_callback(self, msg: PointStamped):
        """Receive /cube_pose and transform to base_link."""
        transformed_point = self.transform_cube_pose(msg)
        if transformed_point is not None:
            self.cube_pose_pub.publish(transformed_point)
            self.get_logger().info(
                f"Published transformed cube pose: "
                f"({transformed_point.point.x:.3f}, {transformed_point.point.y:.3f}, {transformed_point.point.z:.3f})"
            )

    def transform_cube_pose(self, msg: PointStamped):
        """Transform a PointStamped into the base_link frame."""
        try:
            transform = self.tf_buffer.lookup_transform(
                'base_link',                  # target frame
                msg.header.frame_id,          # source frame (e.g. camera_depth_optical_frame)
                rclpy.time.Time(),
                timeout=rclpy.duration.Duration(seconds=1.0)
            )

            transformed_point = tf2_geom.do_transform_point(msg, transform)
            transformed_point.header.frame_id = 'base_link'
            transformed_point.header.stamp = self.get_clock().now().to_msg()
            return transformed_point

        except Exception as e:
            self.get_logger().warn(f"Transform failed: {e}")
            return None


def main(args=None):
    rclpy.init(args=args)
    node = TransformCubePose()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
