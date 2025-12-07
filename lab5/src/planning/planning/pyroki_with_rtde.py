#!/usr/bin/env python3
"""
High-speed ball tracking with RTDE control for minimal latency
Bypasses ROS2 trajectory controller for direct robot communication
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from geometry_msgs.msg import PointStamped
import numpy as np
import time

# RTDE imports
import rtde_control
import rtde_receive

from planning.pyroki_test import PyRokiIKPlanner


class AggressiveCatcherRTDE(Node):
    """
    Ultra-low latency catcher using direct RTDE communication
    Bypasses ROS2 joint_trajectory_controller for speed
    """
    def __init__(self):
        super().__init__('aggressive_catcher_rtde')
        
        # Declare parameters
        self.declare_parameter('robot_ip', '192.168.1.101')  # Default UR IP
        self.declare_parameter('control_frequency', 500.0)  # Hz - RTDE supports up to 500Hz
        self.declare_parameter('servo_time', 0.002)  # 8ms for 125Hz
        self.declare_parameter('servo_lookahead', 0.03)
        self.declare_parameter('servo_gain', 1000)
        
        # Get parameters
        self.robot_ip = self.get_parameter('robot_ip').value
        self.control_freq = self.get_parameter('control_frequency').value
        self.servo_time = self.get_parameter('servo_time').value
        self.servo_lookahead = self.get_parameter('servo_lookahead').value
        self.servo_gain = self.get_parameter('servo_gain').value
        
        # Initialize RTDE connection
        self.get_logger().info(f'Connecting to robot at {self.robot_ip}...')
        try:
            self.ur_c = rtde_control.RTDEControlInterface(self.robot_ip)
            self.ur_r = rtde_receive.RTDEReceiveInterface(self.robot_ip)
            self.get_logger().info('✓ RTDE connection established!')
        except Exception as e:
            self.get_logger().error(f'Failed to connect to robot: {e}')
            raise
        
        # Initialize PyRoKi
        self.get_logger().info('Initializing PyRoKi IK solver...')
        self.pyroki_planner = PyRokiIKPlanner()
        
        # Warm up JAX (CRITICAL - do this once at startup!)
        self.get_logger().info('Warming up JAX compilation...')
        self.pyroki_planner.compute_ik_fast(0.4, 0.0, 0.3)
        self.get_logger().info('✓ JAX compiled and ready!')
        
        # Subscribe to ball position from RealSense/tracking
        self.ball_sub = self.create_subscription(
            PointStamped, '/ball_hitpoint_base',
            self.ball_callback, 10
        )

        # Subscribe to joint states (for monitoring only)
        self.joint_state_sub = self.create_subscription(
            JointState, '/joint_states',
            self.joint_state_callback, 10
        )

        self.current_joint_state = None
        self.ball_position = None
        self.last_ball_position = None
        self.ik_times = []
        self.servo_times = []
        
        # Control parameters
        self.CONTROL_FREQUENCY = self.control_freq
        
        # High-frequency control loop
        self.control_timer = self.create_timer(
            1.0 / self.CONTROL_FREQUENCY,
            self.control_loop
        )

        self.get_logger().info(f'High-speed RTDE tracker ready at {self.CONTROL_FREQUENCY}Hz')
        self.get_logger().info(f'Servo parameters: time={self.servo_time}s, lookahead={self.servo_lookahead}s, gain={self.servo_gain}')
        self.get_logger().info('Waiting for ball position...')
    
    def joint_state_callback(self, msg: JointState):
        """Store current joint state for monitoring"""
        self.current_joint_state = msg

    def ball_callback(self, msg):
        """Update ball position from tracking system"""
        self.ball_position = np.array([
            msg.point.x,
            msg.point.y,
            msg.point.z
        ])
    
    def get_current_joints_ordered(self):
        """Get current joints directly from RTDE (faster than ROS topic)"""
        try:
            # Get actual joint positions directly from robot
            q = self.ur_r.getActualQ()
            return q
        except Exception as e:
            self.get_logger().warn(f'Failed to get joints from RTDE: {e}')
            return None
    
    def control_loop(self):
        """Main control loop - executes at CONTROL_FREQUENCY Hz"""
        
        # Skip if no ball detected
        if self.ball_position is None:
            return
        
        # Skip if ball hasn't moved
        if self.last_ball_position is not None and np.allclose(self.ball_position, self.last_ball_position):
            return

        # Solve IK for received ball position
        ik_start = time.perf_counter()
        
        joints = self.pyroki_planner.compute_ik_fast(
            self.ball_position[0],
            self.ball_position[1],
            self.ball_position[2]
        )
        
        ik_time = (time.perf_counter() - ik_start) * 1000  # ms
        self.ik_times.append(ik_time)

        if joints is None:
            self.get_logger().warn(f'IK failed for position {self.ball_position}')
            return
        
        # Get current joint positions
        current_joints = self.get_current_joints_ordered()
        
        if current_joints is not None:
            # Calculate joint differences
            current = np.array(current_joints)
            target = np.array(joints.position)
            diff = np.abs(current - target)
            max_diff = np.max(diff)
            
            # Log every N iterations to reduce overhead
            if len(self.ik_times) % 10 == 0:
                self.get_logger().info(f'IK time: {ik_time:.2f}ms, Max joint diff: {max_diff:.3f} rad')
            
            # Send servo command using RTDE
            servo_start = time.perf_counter()
            self.send_servo_command(target)
            servo_time = (time.perf_counter() - servo_start) * 1000  # ms
            self.servo_times.append(servo_time)
            
            self.last_ball_position = self.ball_position.copy()
            
            # Log timing stats every 100 iterations
            if len(self.ik_times) % 100 == 0:
                avg_ik = np.mean(self.ik_times[-100:])
                avg_servo = np.mean(self.servo_times[-100:])
                total_loop = avg_ik + avg_servo
                self.get_logger().info(f'Avg timing - IK: {avg_ik:.2f}ms, Servo: {avg_servo:.2f}ms, Total: {total_loop:.2f}ms')

    def send_servo_command(self, target_joints):
        """
        Send servo command directly via RTDE
        ServoJ is designed for real-time control with minimal latency
        
        Args:
            target_joints: List/array of 6 joint positions [rad]
        """
        try:
            # servoJ(q, speed, acceleration, time, lookahead_time, gain)
            # time: the time the function is blocking [s] - should match control frequency
            # lookahead_time: smoothing time [0.03-0.2s] - lower = faster reaction
            # gain: proportional gain [100-2000] - higher = faster reaction
            self.ur_c.servoJ(
                target_joints,
                0,  # speed (not used in servoJ)
                0,  # acceleration (not used in servoJ)
                self.servo_time,
                self.servo_lookahead,
                self.servo_gain
            )
        except Exception as e:
            self.get_logger().error(f'Failed to send servo command: {e}')
    
    def stop_robot(self):
        """Emergency stop"""
        try:
            self.ur_c.servoStop()
            self.get_logger().info('Robot stopped')
        except Exception as e:
            self.get_logger().error(f'Failed to stop robot: {e}')
    
    def cleanup(self):
        """Clean shutdown"""
        self.get_logger().info('Shutting down RTDE connection...')
        try:
            self.ur_c.servoStop()
            self.ur_c.stopScript()
        except:
            pass


def main(args=None):
    rclpy.init(args=args)
    
    node = AggressiveCatcherRTDE()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Interrupted by user')
    finally:
        node.stop_robot()
        node.cleanup()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()