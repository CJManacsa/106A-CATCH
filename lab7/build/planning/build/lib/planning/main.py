import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from sensor_msgs.msg import JointState
from trajectory_msgs.msg import JointTrajectory
from control_msgs.action import FollowJointTrajectory
from tf2_ros import Buffer, TransformListener, TransformException
from planning.ik import IKPlanner
from mover_services.srv import MoveDir, MoveAbs  # Both services

class MoveServer(Node):
    def __init__(self):
        super().__init__('move_server')

        # --- Subscribers ---
        self.joint_state = None
        self.joint_state_sub = self.create_subscription(
            JointState, '/joint_states', self.joint_state_callback, 1
        )

        # --- Action client for trajectories ---
        self.exec_ac = ActionClient(
            self,
            FollowJointTrajectory,
            '/scaled_joint_trajectory_controller/follow_joint_trajectory'
        )

        # --- IK Planner ---
        self.ik_planner = IKPlanner()

        # --- Services ---
        self.dir_srv = self.create_service(
            MoveDir,
            'move_dir',
            self.handle_move_dir_request
        )
        self.abs_srv = self.create_service(
            MoveAbs,
            'move_abs',
            self.handle_move_abs_request
        )

        self.get_logger().info("MoveServer started. Waiting for service calls...")

    # --- Joint state callback ---
    def joint_state_callback(self, msg):
        self.joint_state = msg

    # --- Handle relative move service ---
    def handle_move_dir_request(self, request, response):
        if self.joint_state is None:
            response.success = False
            response.message = "No joint state received yet."
            return response

        self.get_logger().info(f"MoveDir request: '{request.direction}' by {request.distance} m")
        self.move_dir(request.direction.lower(), request.distance)
        response.success = True
        response.message = f"MoveDir '{request.direction}' executed."
        return response

    # --- Handle absolute move service ---
    def handle_move_abs_request(self, request, response):
        if self.joint_state is None:
            response.success = False
            response.message = "No joint state received yet."
            return response

        self.get_logger().info(f"MoveAbs request: move to ({request.x:.3f}, {request.y:.3f}, {request.z:.3f})")
        self.move_abs(request.x, request.y, request.z)
        response.success = True
        response.message = "MoveAbs executed."
        return response

    # --- Get latest EE transform ---
    def lookup_ee_transform_latest(self, timeout=3.0):
        start = self.get_clock().now()
        while (self.get_clock().now() - start).nanoseconds * 1e-9 < timeout:
            try:
                return self.tf_buffer.lookup_transform(
                    "base_link",
                    "wrist_3_link",
                    rclpy.time.Time()
                )
            except TransformException:
                rclpy.spin_once(self, timeout_sec=0.05)
        self.get_logger().error("Could not find latest transform for base_link -> wrist_3_link")
        return None

    # --- Relative move ---
    def move_dir(self, direction: str, distance: float):
        transform = self.lookup_ee_transform_latest()
        if transform is None:
            return

        x = transform.transform.translation.x
        y = transform.transform.translation.y
        z = transform.transform.translation.z

        # Update coordinates based on direction
        if direction == "+z" or direction == "up":
            z += distance
        elif direction == "-z" or direction == "down":
            z -= distance
        elif direction == "+x" or direction == "forward":
            x += distance
        elif direction == "-x" or direction == "backward":
            x -= distance
        elif direction == "+y" or direction == "left":
            y += distance
        elif direction == "-y" or direction == "right":
            y -= distance
        else:
            self.get_logger().error(f"Unknown direction '{direction}'")
            return

        self.move_abs(x, y, z)

    # --- Absolute move ---
    def move_abs(self, x: float, y: float, z: float):
        target_joint_state = self.ik_planner.compute_ik(self.joint_state, x, y, z)
        if target_joint_state is None:
            self.get_logger().error("IK failed for MoveAbs.")
            return

        traj = self.ik_planner.plan_to_joints(target_joint_state)
        if traj is None:
            self.get_logger().error("Planning failed for MoveAbs.")
            return

        self.get_logger().info(f"Executing move to ({x:.3f}, {y:.3f}, {z:.3f})")
        self.execute_trajectory(traj.joint_trajectory)

    # --- Execute trajectory ---
    def execute_trajectory(self, joint_traj: JointTrajectory):
        self.exec_ac.wait_for_server()
        goal = FollowJointTrajectory.Goal()
        goal.trajectory = joint_traj
        send_future = self.exec_ac.send_goal_async(goal)
        send_future.add_done_callback(self.on_goal_sent)

    def on_goal_sent(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().error("Trajectory was rejected.")
            return
        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(lambda f: self.get_logger().info("Execution completed."))


def main(args=None):
    rclpy.init(args=args)
    node = MoveServer()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
