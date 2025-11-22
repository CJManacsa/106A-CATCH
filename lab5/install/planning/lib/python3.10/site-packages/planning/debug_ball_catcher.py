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


class HighSpeedBallTracker(Node):
    """
    Tracks a moving ball at high frequency (50-100Hz)
    For real ball catching with RealSense
    """
    def __init__(self):
        super().__init__('highspeed_ball_tracker')
        
        # Initialize PyRoKi
        self.get_logger().info('Initializing PyRoKi IK solver...')
        self.pyroki_planner = PyRokiIKPlanner()
        
        # Warm up JAX (CRITICAL - do this once at startup!)
        self.get_logger().info('Warming up JAX compilation...')
        self.pyroki_planner.compute_ik_fast(0.4, 0.0, 0.3)
        self.get_logger().info('✓ JAX compiled and ready!')
        
        # Subscribe to joint states (for reference)
        self.joint_state_sub = self.create_subscription(
            JointState, '/joint_states',
            self.joint_state_callback, 10
        )
        
        # Subscribe to ball position from RealSense/tracking
        # TODO: Replace with your actual ball tracking topic
        self.ball_sub = self.create_subscription(
            PointStamped, '/ball_position',  # Change to your topic name
            self.ball_callback, 10
        )
        
        # Publisher for trajectory commands
        self.traj_pub = self.create_publisher(
            JointTrajectory,
            '/scaled_joint_trajectory_controller/joint_trajectory',
            10
        )
        
        self.current_joint_state = None
        self.ball_position = None
        self.last_command_time = 0
        
        # Control parameters
        self.CONTROL_FREQUENCY = 50  # Hz (50 Hz = 20ms between commands)
        self.TRAJECTORY_DURATION = 0.1  # 100ms lookahead
        
        # High-frequency control loop
        self.control_timer = self.create_timer(
            1.0 / self.CONTROL_FREQUENCY,
            self.control_loop
        )
        
        self.iteration = 0
        self.ik_times = []
        
        self.get_logger().info(f'High-speed tracker ready at {self.CONTROL_FREQUENCY}Hz')
        self.get_logger().info('Waiting for ball position...')
    
    def joint_state_callback(self, msg: JointState):
        """Store current joint state"""
        self.current_joint_state = msg
    
    def ball_callback(self, msg: PointStamped):
        """Receive ball position from camera/tracker"""
        self.ball_position = np.array([
            msg.point.x,
            msg.point.y,
            msg.point.z
        ])
    
    def control_loop(self):
        """
        Main control loop - runs at 50-100Hz
        Continuously sends updated trajectories based on ball position
        """
        # Need ball position to track
        if self.ball_position is None:
            return
        
        self.iteration += 1
        
        # Solve IK for current ball position
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
        
        # Check if IK is fast enough
        if ik_time > (1000.0 / self.CONTROL_FREQUENCY):
            self.get_logger().warn(
                f'IK too slow! {ik_time:.2f}ms exceeds {1000.0/self.CONTROL_FREQUENCY:.1f}ms budget'
            )
        
        # Send trajectory command
        self.send_trajectory(joints, self.TRAJECTORY_DURATION)
        
        # Log occasionally (every 1 second)
        if self.iteration % self.CONTROL_FREQUENCY == 0:
            avg_ik_time = np.mean(self.ik_times[-self.CONTROL_FREQUENCY:])
            self.get_logger().info(
                f'Tracking: pos=[{self.ball_position[0]:.3f}, {self.ball_position[1]:.3f}, {self.ball_position[2]:.3f}], '
                f'avg_IK={avg_ik_time:.2f}ms, freq={self.CONTROL_FREQUENCY}Hz'
            )
    
    def send_trajectory(self, joint_state: JointState, duration: float):
        """Send trajectory command to robot"""
        traj = JointTrajectory()
        traj.joint_names = joint_state.name
        
        point = JointTrajectoryPoint()
        point.positions = joint_state.position
        point.velocities = [0.0] * len(joint_state.position)
        point.time_from_start.sec = int(duration)
        point.time_from_start.nanosec = int((duration % 1) * 1e9)
        
        traj.points.append(point)
        
        self.traj_pub.publish(traj)


class SimulatedBallTracker(Node):
    """
    Simulates a falling ball for testing
    No camera needed - just demonstrates high-speed tracking
    """
    def __init__(self):
        super().__init__('simulated_ball_tracker')
        
        # Initialize PyRoKi
        self.pyroki_planner = PyRokiIKPlanner()
        self.pyroki_planner.compute_ik_fast(0.4, 0.0, 0.3)  # Warmup
        
        # Publisher
        self.traj_pub = self.create_publisher(
            JointTrajectory,
            '/scaled_joint_trajectory_controller/joint_trajectory',
            10
        )
        
        # Simulated ball position
        self.ball_x = 0.4
        self.ball_y = 0.0
        self.ball_z = 0.6  # Start high
        self.ball_vz = -0.1  # Falling
        
        # Control at 50Hz
        self.control_timer = self.create_timer(0.02, self.control_loop)
        
        self.iteration = 0
        self.start_time = time.time()
        
        self.get_logger().info('Simulated ball tracker started')
        self.get_logger().info(f'Ball starting at ({self.ball_x}, {self.ball_y}, {self.ball_z})')
        self.get_logger().info('Watch the robot track the falling ball!')
    
    def control_loop(self):
        """Update ball position and track it"""
        # Update simulated ball (falling)
        self.ball_z += self.ball_vz * 0.02  # Update at 50Hz
        
        # Stop when caught
        if self.ball_z < 0.25:
            elapsed = time.time() - self.start_time
            self.get_logger().info(f'\n✓ Ball caught after {elapsed:.2f} seconds!')
            self.get_logger().info(f'  Sent {self.iteration} trajectory commands')
            self.get_logger().info(f'  Average rate: {self.iteration/elapsed:.1f} Hz')
            self.control_timer.cancel()
            return
        
        # Solve IK
        start = time.perf_counter()
        joints = self.pyroki_planner.compute_ik_fast(
            self.ball_x,
            self.ball_y,
            self.ball_z
        )
        ik_time = (time.perf_counter() - start) * 1000
        
        if joints:
            # Send command
            traj = JointTrajectory()
            traj.joint_names = joints.name
            
            point = JointTrajectoryPoint()
            point.positions = joints.position
            point.velocities = [0.0] * len(joints.position)
            point.time_from_start.sec = 0
            point.time_from_start.nanosec = int(0.05 * 1e9)  # 50ms lookahead
            
            traj.points.append(point)
            self.traj_pub.publish(traj)
            
            self.iteration += 1
            
            # Log every 25 iterations (0.5s)
            if self.iteration % 25 == 0:
                self.get_logger().info(
                    f'z={self.ball_z:.3f}m, IK={ik_time:.2f}ms, cmds={self.iteration}'
                )


class AggressiveCatcher(Node):
    """
    Most aggressive version - very fast movements
    WARNING: Only use if you know the workspace is clear!
    """
    def __init__(self):
        super().__init__('aggressive_catcher')
        
        self.pyroki_planner = PyRokiIKPlanner()
        self.pyroki_planner.compute_ik_fast(0.4, 0.0, 0.3)
        
        self.traj_pub = self.create_publisher(
            JointTrajectory,
            '/scaled_joint_trajectory_controller/joint_trajectory',
            10
        )
        
        # Test: Move to 3 positions VERY quickly
        self.positions = [
            (0.5, 0.0, 0.4),
            (0.4, 0.2, 0.3),
            (0.3, -0.1, 0.5),
        ]
        self.current_pos = 0
        
        # Wait a bit then start
        self.create_timer(2.0, self.next_position)
        
        self.get_logger().info('Aggressive catcher ready - will move FAST!')
    
    def next_position(self):
        if self.current_pos >= len(self.positions):
            self.get_logger().info('All positions reached!')
            return
        
        x, y, z = self.positions[self.current_pos]
        self.get_logger().info(f'Moving to ({x}, {y}, {z}) in 0.3s...')
        
        joints = self.pyroki_planner.compute_ik_fast(x, y, z)
        
        if joints:
            traj = JointTrajectory()
            traj.joint_names = joints.name
            
            point = JointTrajectoryPoint()
            point.positions = joints.position
            point.velocities = [0.0] * len(joints.position)
            point.time_from_start.sec = 0
            point.time_from_start.nanosec = int(0.3 * 1e9)  # Only 300ms!
            
            traj.points.append(point)
            self.traj_pub.publish(traj)
        
        self.current_pos += 1
        self.create_timer(1.0, self.next_position)  # Wait 1s between moves


def main(args=None):
    rclpy.init(args=args)
    
    import sys
    if len(sys.argv) > 1:
        mode = sys.argv[1]
        if mode == 'sim':
            node = SimulatedBallTracker()
        elif mode == 'aggressive':
            node = AggressiveCatcher()
        else:
            node = HighSpeedBallTracker()
    else:
        # Default: simulated falling ball
        node = SimulatedBallTracker()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()