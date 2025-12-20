#!/usr/bin/env python3
import math
import yaml

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient

from moveit_msgs.srv import GetMotionPlan
from moveit_msgs.msg import Constraints, JointConstraint
from control_msgs.action import FollowJointTrajectory
from trajectory_msgs.msg import JointTrajectoryPoint


class Tuck(Node):
    def __init__(self):
        super().__init__('Tuck')

        self.plan_cli = self.create_client(GetMotionPlan, '/plan_kinematic_path')
        while not self.plan_cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for /plan_kinematic_path...')

        self.exec_ac = ActionClient(
            self, FollowJointTrajectory,
            '/scaled_joint_trajectory_controller/follow_joint_trajectory'
        )

        req = GetMotionPlan.Request()
        req.motion_plan_request.group_name = 'ur_manipulator'
        # This is the default planning time in Rviz, idk if we want to make it longer or not 
        req.motion_plan_request.allowed_planning_time = 5.0

        goal = Constraints()
        # Again, these are all default tolerances
        # I should probably make this into a yaml
        goal.joint_constraints.append(JointConstraint(
            joint_name='shoulder_pan_joint',
            position=math.radians(64.3),#271.0),
            tolerance_above=0.01, tolerance_below=0.01, weight=1.0
        ))
        goal.joint_constraints.append(JointConstraint(
            joint_name='shoulder_lift_joint',
            position=math.radians(-73.5),#-106.0),
            tolerance_above=0.01, tolerance_below=0.01, weight=1.0
        ))
        goal.joint_constraints.append(JointConstraint(
            joint_name='elbow_joint',
            position=math.radians(79.7),#-82.0),
            tolerance_above=0.01, tolerance_below=0.01, weight=1.0
        ))
        goal.joint_constraints.append(JointConstraint(
            joint_name='wrist_1_joint',
            position=math.radians(264.0),#-96.2),
            tolerance_above=0.01, tolerance_below=0.01, weight=1.0
        ))
        goal.joint_constraints.append(JointConstraint(
            joint_name='wrist_2_joint',
            position=math.radians(-90.0),#91.0),
            tolerance_above=0.01, tolerance_below=0.01, weight=1.0
        ))
        goal.joint_constraints.append(JointConstraint(
            joint_name='wrist_3_joint',
            position=math.radians(-205.6),#-180.0),
            tolerance_above=0.01, tolerance_below=0.01, weight=1.0
        ))
        req.motion_plan_request.goal_constraints.append(goal)

        future = self.plan_cli.call_async(req)
        future.add_done_callback(self._on_plan)

    def _on_plan(self, future):
        try:
            res = future.result()
        except Exception as e:
            self.get_logger().error(f'Planning service failed: {e}')
            rclpy.shutdown()
            return

        mpr = res.motion_plan_response
        err = mpr.error_code.val
        if err != 1 or not mpr.trajectory.joint_trajectory.points:
            self.get_logger().error(f'Planning failed (error_code={err}).')
            rclpy.shutdown()
            return

        jt = mpr.trajectory.joint_trajectory
        self.get_logger().info('Trajectory created successfully')

        # Execute the plan via FollowJointTrajectory
        self._execute_joint_trajectory(jt)

    def _execute_joint_trajectory(self, joint_traj):
        self.get_logger().info('Waiting for controller action server...')
        self.exec_ac.wait_for_server()

        goal = FollowJointTrajectory.Goal()
        goal.trajectory = joint_traj

        self.get_logger().info('Sending trajectory to controller...')
        send_future = self.exec_ac.send_goal_async(goal)
        send_future.add_done_callback(self._on_goal_sent)

    def _on_goal_sent(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().error('bonk')
            rclpy.shutdown()
            return

        self.get_logger().info('Executing...')
        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self._on_exec_done)

    def _on_exec_done(self, future):
        try:
            result = future.result().result
            self.get_logger().info("Tuck finished")
        except Exception as e:
            self.get_logger().error(f'Execution failed: {e}')
        finally:
            rclpy.shutdown()


def main():
    rclpy.init()
    node = Tuck()
    rclpy.spin(node)


if __name__ == '__main__':
    main()

