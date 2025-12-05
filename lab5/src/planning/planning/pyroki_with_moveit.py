#!/usr/bin/env python3
"""
High-speed ball tracking for real-time catching
Continuously publishes trajectories as the ball moves
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from geometry_msgs.msg import PointStamped
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
import numpy as np
import time

from planning.pyroki_test import PyRokiIKPlanner


class AggressiveCatcher(Node):
    """
    Most aggressive version - very fast movements
    WARNING: Only use if you know the workspace is clear!
    """
    def __init__(self):
        super().__init__('aggressive_catcher')
        
        # Initialize PyRoKi
        self.get_logger().info('Initializing PyRoKi IK solver...')
        self.pyroki_planner = PyRokiIKPlanner()
        
        # Warm up JAX (CRITICAL - do this once at startup!)
        self.get_logger().info('Warming up JAX compilation...')
        self.pyroki_planner.compute_ik_fast(0.4, 0.0, 0.3)
        self.get_logger().info('✓ JAX compiled and ready!')
        
        self.traj_pub = self.create_publisher(
            JointTrajectory,
            '/scaled_joint_trajectory_controller/joint_trajectory',
            10
        )
                
        # Subscribe to ball position from RealSense/tracking
        self.ball_sub = self.create_subscription(
            PointStamped, '/ball_hitpoint_base',  # Change to your topic name
            self.ball_callback, 10
        )

        # Subscribe to joint states (for reference)
        self.joint_state_sub = self.create_subscription(
            JointState, '/joint_states',
            self.joint_state_callback, 10
        )

        self.current_joint_state = None
        self.ball_position = None
        self.last_ball_position = None

        # self.iteration = 0
        self.ik_times = []

         # Control parameters
        self.CONTROL_FREQUENCY = 50  # Hz (50 Hz = 20ms between commands)
        
        # High-frequency control loop
        self.control_timer = self.create_timer(
            1.0 / self.CONTROL_FREQUENCY,
            self.control_loop
        )

        self.get_logger().info(f'High-speed tracker ready at {self.CONTROL_FREQUENCY}Hz')
        self.get_logger().info('Waiting for ball position...')
    
    def joint_state_callback(self, msg: JointState):
        """Store current joint state"""
        self.current_joint_state = msg

    def ball_callback(self, msg):
        self.ball_position = np.array([
            msg.point.x,
            msg.point.y,
            msg.point.z
        ])
    
    def get_current_joints_ordered(self):
        """Get current joints in correct UR order (matching IK output)"""
        if self.current_joint_state is None:
            return None
        
        # Build dictionary from joint_states
        current_positions = {}
        for i, name in enumerate(self.current_joint_state.name):
            current_positions[name] = self.current_joint_state.position[i]

                # CRITICAL: Define the correct UR joint order
        joint_names = [
            'shoulder_pan_joint', 
            'shoulder_lift_joint', 
            'elbow_joint',
            'wrist_1_joint', 
            'wrist_2_joint', 
            'wrist_3_joint'
        ]
        
        # Return in CORRECT order (matching IK solver)
        return [current_positions[name] for name in joint_names]
    
    def control_loop(self):

        if self.ball_position is None:
            return
        
        if self.last_ball_position is not None and np.allclose(self.ball_position, self.last_ball_position):
            return

        # Solve IK for received ball position
        start = time.perf_counter()
        
        joints = self.pyroki_planner.compute_ik_fast(
            self.ball_position[0],
            self.ball_position[1],
            self.ball_position[2]
        )
        
        ik_time = (time.perf_counter() - start) * 1000  # ms
        self.ik_times.append(ik_time)

        if joints is None:
            self.get_logger().warn(f'IK failed for position {self.ball_position}')
            return
        
        # Show joints calculated
        current_ordered = self.get_current_joints_ordered()
        
        # Logging could slow down performance: get rid of logs if trajectory is not sending (could be preventing correct loop timer)
        if current_ordered is not None: self.get_logger().info(f'Current joints (UR order): {[f"{j:.3f}" for j in current_ordered]}')
        if joints is not None: 
            self.get_logger().info(f'IK joints (UR order):  {[f"{j:.3f}" for j in joints.position]}')
                # Fix wrist_2 (index 4) and wrist_3 (index 5) to keep current values
            modified_positions = list(joints.position)  # Copy IK solution
            # modified_positions[4] = current_ordered[4]  # Keep current wrist_2
            modified_positions[5] = current_ordered[5]  # Keep current wrist_3
            
            # Create modified JointState
            fixed_joints = JointState()
            fixed_joints.name = joints.name
            fixed_joints.position = modified_positions
            self.get_logger().info(f'fixed joints (UR order):  {[f"{j:.3f}" for j in fixed_joints.position]}')

            
            self.send_trajectory(fixed_joints)
            self.last_ball_position = self.ball_position.copy()
        

    def send_trajectory(self, joints: JointState):
        traj = JointTrajectory()
        traj.joint_names = joints.name

        point = JointTrajectoryPoint()
        point.positions = joints.position
        point.velocities = [0.0] * len(joints.position)
        point.time_from_start.sec = 0 # Change to 10 for first moving around the entire loop
        point.time_from_start.nanosec = int(0.1 * 1e9)  # Tested in ranges 0.05 - 0.3

        traj.points.append(point)
        self.traj_pub.publish(traj)
        


def main(args=None):
    rclpy.init(args=args)
    
    import sys

    node = AggressiveCatcher()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
