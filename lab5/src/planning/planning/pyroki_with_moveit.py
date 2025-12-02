#!/usr/bin/env python3
"""
Ball Catcher using TOPIC publishing (no action server required)
For when /follow_joint_trajectory action is not available
"""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PointStamped
from sensor_msgs.msg import JointState
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration
import numpy as np
import time

from planning.pyroki_ik_planner import PyRokiIKPlanner


class TopicBallCatcher(Node):
    """
    Uses topic publishing instead of action client
    Publishes to: /scaled_joint_trajectory_controller/joint_trajectory
    """
    def __init__(self):
        super().__init__('topic_ball_catcher')
        
        # Initialize PyRoKi
        self.get_logger().info('Initializing PyRoKi IK solver...')
        self.ik_solver = PyRokiIKPlanner()
        self.ik_solver.compute_ik_fast(0.4, 0.0, 0.3)  # Warmup
        self.get_logger().info('✓ IK solver ready!')
        
        # Publisher for trajectory (no action server needed!)
        self.traj_pub = self.create_publisher(
            JointTrajectory,
            '/scaled_joint_trajectory_controller/joint_trajectory',
            10
        )
        
        # Subscribe to ball hitpoint
        self.hitpoint_sub = self.create_subscription(
            PointStamped,
            '/ball_hitpoint_base',
            self.hitpoint_callback,
            10
        )
        
        # Subscribe to joint states
        self.joint_state_sub = self.create_subscription(
            JointState,
            '/joint_states',
            self.joint_state_callback,
            10
        )
        
        self.current_joints = None
        
        self.get_logger().info('=' * 70)
        self.get_logger().info('Topic Ball Catcher Ready!')
        self.get_logger().info('Publishing to: /scaled_joint_trajectory_controller/joint_trajectory')
        self.get_logger().info('No action server required!')
        self.get_logger().info('=' * 70)
    
    def joint_state_callback(self, msg: JointState):
        """Track current joint state"""
        self.current_joints = msg
    
    def hitpoint_callback(self, msg: PointStamped):
        """
        Receive ball hitpoint and execute catch
        """
        x, y, z = msg.point.x, msg.point.y, msg.point.z
        
        self.get_logger().info(f'Target: ({x:.3f}, {y:.3f}, {z:.3f})')
        
        if self.current_joints is None:
            self.get_logger().warn('No joint state yet')
            return
        
        # Solve IK
        start = time.perf_counter()
        joint_solution = self.ik_solver.compute_ik_fast(x, y, z)
        ik_time_ms = (time.perf_counter() - start) * 1000
        
        if joint_solution is None:
            self.get_logger().error(f'IK failed after {ik_time_ms:.2f}ms')
            return
        
        self.get_logger().info(f'IK solved in {ik_time_ms:.2f}ms')
        
        # Get current and target positions
        current_positions = {}
        for i, name in enumerate(self.current_joints.name):
            current_positions[name] = self.current_joints.position[i]
        
        current = np.array([current_positions[name] for name in joint_solution.name])
        target = np.array(joint_solution.position)
        
        diff = np.abs(target - current)
        max_diff = np.max(diff)
        
        self.get_logger().info(f'Max joint diff: {max_diff:.3f} rad ({np.degrees(max_diff):.1f}°)')
        
        # if max_diff > 3.14:
        #     self.get_logger().error('Movement too large! Aborting.')
        #     return
        
        # Create and publish trajectory
        self.publish_trajectory(current.tolist(), target.tolist(), joint_solution.name)
    
    def publish_trajectory(self, current_pos, target_pos, joint_names):
        """
        Publish trajectory directly to topic
        """
        # Calculate timing
        diff = np.array(target_pos) - np.array(current_pos)
        max_movement = np.max(np.abs(diff))
        move_time = max(0.5, 0.5 + 0.3 * max_movement)
        
        self.get_logger().info(f'Publishing trajectory ({move_time:.2f}s)...')
        
        # Build trajectory
        traj = JointTrajectory()
        traj.header.stamp = self.get_clock().now().to_msg()
        traj.joint_names = joint_names
        
        # Point 1: Current
        point1 = JointTrajectoryPoint()
        point1.positions = current_pos
        point1.velocities = [0.0] * len(current_pos)
        point1.time_from_start = Duration(sec=0, nanosec=0)
        
        # Point 2: Target
        point2 = JointTrajectoryPoint()
        point2.positions = target_pos
        point2.velocities = [0.0] * len(target_pos)
        sec = int(move_time)
        nanosec = int((move_time - sec) * 1e9)
        point2.time_from_start = Duration(sec=sec, nanosec=nanosec)
        
        traj.points = [point1, point2]
        
        # Publish
        self.traj_pub.publish(traj)
        self.get_logger().info('✓ Trajectory published!')


def main(args=None):
    rclpy.init(args=args)
    node = TopicBallCatcher()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Shutting down...')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()