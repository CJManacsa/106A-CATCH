#!/usr/bin/env python3
"""
Simplified real-time robot control with PyRoKi IK
Uses callbacks instead of blocking waits to avoid deadlocks
"""

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from sensor_msgs.msg import JointState
from control_msgs.action import FollowJointTrajectory
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration
import time

# Import your PyRoKi IK planner
from planning.pyroki_test import PyRokiIKPlanner


class SimpleBallCatcher(Node):
    """
    Simplified ball catching demo - sends commands without blocking
    """
    def __init__(self):
        super().__init__('simple_ball_catcher')
        
        # Initialize PyRoKi
        self.get_logger().info('Initializing PyRoKi...')
        self.pyroki_planner = PyRokiIKPlanner()
        
        # Warm up JAX
        self.get_logger().info('Warming up JAX (2 seconds)...')
        self.pyroki_planner.compute_ik_fast(0.3, 0.0, 0.3)
        self.get_logger().info('✓ Ready!')
        
        # Subscribe to joint states
        self.joint_state_sub = self.create_subscription(
            JointState, '/joint_states',
            self.joint_state_callback, 10
        )
        
        # Action client
        self.exec_ac = ActionClient(
            self, FollowJointTrajectory,
            '/scaled_joint_trajectory_controller/follow_joint_trajectory'
        )
        
        self.current_joint_state = None
        self.started = False
        
    def joint_state_callback(self, msg: JointState):
        self.current_joint_state = msg
        
        if not self.started and self.current_joint_state is not None:
            self.started = True
            
            # Wait for action server
            self.get_logger().info('Waiting for action server...')
            if not self.exec_ac.wait_for_server(timeout_sec=10.0):
                self.get_logger().error('Action server not available!')
                return
            
            self.get_logger().info('✓ Action server ready!')
            self.start_demo()
    
    def start_demo(self):
        """Start the ball catching demo"""
        self.get_logger().info('\n' + '='*60)
        self.get_logger().info('SIMPLE BALL CATCHING DEMO')
        self.get_logger().info('='*60)
        
        # Solve IK for catch position
        catch_x, catch_y, catch_z = -0.8, -0.2, -0.6
        
        self.get_logger().info(f'\nCatch point: ({catch_x}, {catch_y}, {catch_z})')
        
        # Solve IK
        start = time.perf_counter()
        joints = self.pyroki_planner.compute_ik_fast(catch_x, catch_y, catch_z)
        ik_time = (time.perf_counter() - start) * 1000
        
        if joints:
            self.get_logger().info(f'IK solved in {ik_time:.2f}ms')
            self.get_logger().info(f'Target joints: {[f"{j:.3f}" for j in joints.position]}')
            
            # Send to robot
            self.send_trajectory(joints, duration=1.0)
        else:
            self.get_logger().error('IK failed!')
    
    def send_trajectory(self, joint_state: JointState, duration: float):
        """Send trajectory to robot (non-blocking)"""
        # Build trajectory
        traj = JointTrajectory()
        traj.joint_names = joint_state.name
        
        point = JointTrajectoryPoint()
        point.positions = joint_state.position
        point.time_from_start = Duration(sec=int(duration), nanosec=int((duration % 1) * 1e9))
        
        traj.points = [point]
        
        # Create goal
        goal = FollowJointTrajectory.Goal()
        goal.trajectory = traj
        
        # Send goal with callback
        self.get_logger().info(f'Sending trajectory ({duration}s duration)...')
        
        send_goal_future = self.exec_ac.send_goal_async(
            goal,
            feedback_callback=self.feedback_callback
        )
        send_goal_future.add_done_callback(self.goal_response_callback)
    
    def goal_response_callback(self, future):
        """Called when goal is accepted/rejected"""
        goal_handle = future.result()
        
        if not goal_handle.accepted:
            self.get_logger().error('✗ Goal rejected!')
            return
        
        self.get_logger().info('✓ Goal accepted, robot moving...')
        
        # Get result when done
        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self.result_callback)
    
    def feedback_callback(self, feedback_msg):
        """Called during motion"""
        # Optionally log feedback
        pass
    
    def result_callback(self, future):
        """Called when motion completes"""
        result = future.result().result
        self.get_logger().info('✓ Motion complete!')
        self.get_logger().info('🎾 BALL CAUGHT!')
        self.get_logger().info('\n' + '='*60)
        self.get_logger().info('Demo complete. Press Ctrl+C to exit.')
        self.get_logger().info('='*60)


class HighSpeedTracker(Node):
    """
    High-speed tracking demo - continuously sends commands
    """
    def __init__(self):
        super().__init__('highspeed_tracker')
        
        # Initialize PyRoKi
        self.pyroki_planner = PyRokiIKPlanner()
        self.pyroki_planner.compute_ik_fast(0.3, 0.0, 0.3)  # Warmup
        
        # Subscribe to joint states  
        self.joint_state_sub = self.create_subscription(
            JointState, '/joint_states',
            lambda msg: None, 10
        )
        
        # Action client
        self.exec_ac = ActionClient(
            self, FollowJointTrajectory,
            '/scaled_joint_trajectory_controller/follow_joint_trajectory'
        )
        
        # Wait for server
        self.get_logger().info('Waiting for action server...')
        if not self.exec_ac.wait_for_server(timeout_sec=10.0):
            self.get_logger().error('Action server not available!')
            return
        
        self.get_logger().info('✓ Ready for high-speed tracking')
        
        # Simulated ball position
        self.ball_z = 0.5
        self.ball_vz = -0.05  # Falling
        
        # Control loop at 50Hz (20ms)
        self.timer = self.create_timer(0.02, self.control_loop)
        self.iteration = 0
    
    def control_loop(self):
        """Called at 50Hz"""
        # Update ball position
        self.ball_z += self.ball_vz * 0.02
        
        if self.ball_z < 0.25:
            self.get_logger().info('Ball caught!')
            self.timer.cancel()
            return
        
        # Solve IK
        start = time.perf_counter()
        joints = self.pyroki_planner.compute_ik_fast(0.4, 0.1, self.ball_z)
        ik_time = (time.perf_counter() - start) * 1000
        
        if joints and ik_time < 5.0:
            # Send trajectory (very short duration for tracking)
            traj = JointTrajectory()
            traj.joint_names = joints.name
            
            point = JointTrajectoryPoint()
            point.positions = joints.position
            point.time_from_start = Duration(sec=0, nanosec=int(0.05 * 1e9))  # 50ms
            traj.points = [point]
            
            goal = FollowJointTrajectory.Goal()
            goal.trajectory = traj
            
            # Fire and forget
            self.exec_ac.send_goal_async(goal)
            
            # Log occasionally
            self.iteration += 1
            if self.iteration % 25 == 0:  # Every 0.5s
                self.get_logger().info(
                    f'Tracking: z={self.ball_z:.3f}m, IK={ik_time:.2f}ms'
                )


def main(args=None):
    rclpy.init(args=args)
    
    # Choose demo
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'track':
        node = HighSpeedTracker()
    else:
        node = SimpleBallCatcher()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()