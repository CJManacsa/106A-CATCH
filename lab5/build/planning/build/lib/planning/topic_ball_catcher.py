#!/usr/bin/env python3
"""
Ball catching using PyRoKi IK + trajectory topic (not action server)
Based on your lab's joint_pos_control approach
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
import numpy as np
import time

from planning.pyroki_test import PyRokiIKPlanner


class TopicBallCatcher(Node):
    """
    Ball catcher using trajectory topic (simpler than action server)
    """
    def __init__(self):
        super().__init__('topic_ball_catcher')
        
        # Initialize PyRoKi
        self.get_logger().info('Initializing PyRoKi...')
        self.pyroki_planner = PyRokiIKPlanner()
        
        # Warm up JAX
        self.get_logger().info('Warming up JAX...')
        self.pyroki_planner.compute_ik_fast(0.3, 0.0, 0.3)
        self.get_logger().info('✓ Ready!')
        
        # Subscribe to joint states
        self.joint_state_sub = self.create_subscription(
            JointState, '/joint_states',
            self.joint_state_callback, 10
        )
        
        # Publisher for trajectory commands (like your lab code!)
        self.traj_pub = self.create_publisher(
            JointTrajectory,
            '/scaled_joint_trajectory_controller/joint_trajectory',
            10
        )
        
        self.current_joint_state = None
        self.started = False
        
        self.get_logger().info('Waiting for joint states...')
    
    def joint_state_callback(self, msg: JointState):
        self.current_joint_state = msg
        
        if not self.started and self.current_joint_state is not None:
            self.started = True
            time.sleep(1.0)  # Give publisher time to connect
            self.run_catch_demo()
    
    def run_catch_demo(self):
        """Run ball catching demo"""
        self.get_logger().info('\n' + '='*60)
        self.get_logger().info('BALL CATCHING DEMO - Using Trajectory Topic')
        self.get_logger().info('='*60)
        
        # Test different catch positions
        positions = [
            (0.4, 0.1, 0.4, "Position 1"),
            (0.5, -0.1, 0.3, "Position 2"),
            (0.3, 0.2, 0.5, "Position 3"),
        ]
        
        for x, y, z, label in positions:
            self.get_logger().info(f'\n--- {label}: ({x:.2f}, {y:.2f}, {z:.2f}) ---')
            
            # Solve IK
            start = time.perf_counter()
            joints = self.pyroki_planner.compute_ik_fast(x, y, z)
            ik_time = (time.perf_counter() - start) * 1000
            
            if joints is None:
                self.get_logger().error('IK failed!')
                continue
            
            self.get_logger().info(f'IK solved in {ik_time:.2f}ms')
            
            # Show joint angles
            self.get_logger().info('Target joints:')
            for name, pos in zip(joints.name, joints.position):
                self.get_logger().info(f'  {name}: {pos:.3f} rad ({np.degrees(pos):.1f}°)')
            
            # Move robot
            self.move_to_joints(joints, duration_sec=2.0)
            
            # Wait for movement
            time.sleep(3.0)
        
        self.get_logger().info('\n' + '='*60)
        self.get_logger().info('Demo complete!')
        self.get_logger().info('='*60)
    
    def move_to_joints(self, joint_state: JointState, duration_sec: float):
        """
        Move robot to joint configuration using trajectory topic
        (Based on your lab's joint_pos_control.py)
        """
        # Create trajectory message
        traj = JointTrajectory()
        traj.joint_names = joint_state.name
        
        # Create trajectory point
        point = JointTrajectoryPoint()
        point.positions = joint_state.position
        point.velocities = [0.0] * len(joint_state.position)
        point.time_from_start.sec = int(duration_sec)
        point.time_from_start.nanosec = int((duration_sec % 1) * 1e9)
        
        # Add point to trajectory
        traj.points.append(point)
        
        # Publish!
        self.get_logger().info(f'Publishing trajectory ({duration_sec}s duration)...')
        self.traj_pub.publish(traj)
        self.get_logger().info('✓ Command sent!')


class SimpleCatcher(Node):
    """
    Ultra-simple version - just catch one position
    """
    def __init__(self):
        super().__init__('simple_catcher')
        
        # Initialize PyRoKi
        self.pyroki_planner = PyRokiIKPlanner()
        self.pyroki_planner.compute_ik_fast(0.3, 0.0, 0.3)  # Warmup
        
        # Publisher
        self.traj_pub = self.create_publisher(
            JointTrajectory,
            '/scaled_joint_trajectory_controller/joint_trajectory',
            10
        )
        
        # Subscribe to joint states
        self.joint_state_sub = self.create_subscription(
            JointState, '/joint_states',
            self.on_joint_state, 10
        )
        
        self.moved = False
        
    def on_joint_state(self, msg):
        if self.moved:
            return
        
        self.moved = True
        time.sleep(1.0)
        
        # Catch position
        x, y, z = 0.5, 0.0, 0.4
        
        self.get_logger().info(f'Catching ball at ({x}, {y}, {z})...')
        
        # Solve IK
        joints = self.pyroki_planner.compute_ik_fast(x, y, z)
        
        if joints:
            self.get_logger().info('IK solved! Moving robot...')
            
            # Create and publish trajectory
            traj = JointTrajectory()
            traj.joint_names = joints.name
            
            point = JointTrajectoryPoint()
            point.positions = joints.position
            point.velocities = [0.0] * len(joints.position)
            point.time_from_start.sec = 2
            
            traj.points.append(point)
            
            self.traj_pub.publish(traj)
            self.get_logger().info('✓ Trajectory published!')
        else:
            self.get_logger().error('IK failed!')


def main(args=None):
    rclpy.init(args=args)
    
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'simple':
        node = SimpleCatcher()
    else:
        node = TopicBallCatcher()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()