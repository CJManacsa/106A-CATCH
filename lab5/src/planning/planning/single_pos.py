#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from sensor_msgs.msg import JointState
from builtin_interfaces.msg import Duration
import time

class SimpleMoveTester(Node):
    def __init__(self):
        super().__init__('simple_move_tester')
        
        self.joint_sub = self.create_subscription(
            JointState,
            '/joint_states',
            self.joint_callback,
            10
        )
        
        self.traj_pub = self.create_publisher(
            JointTrajectory,
            '/joint_trajectory_controller/joint_trajectory',
            10
        )
        
        self.current_joints = None
        self.has_moved = False
        
        self.get_logger().info("Waiting for joint states...")
    
    def joint_callback(self, msg: JointState):
        if self.current_joints is None:
            self.current_joints = msg
            self.get_logger().info(f"Current joint positions: {[f'{j:.3f}' for j in msg.position[:6]]}")
            
            time.sleep(2)
            self.test_small_movement()
    
    def test_small_movement(self):
        if self.has_moved:
            return
        
        self.has_moved = True
        
        self.get_logger().info("Testing SMALL movement (just first joint +0.1 rad)...")
        
        # Get current position - REORDER to match joint_names order!
        # joint_states might not be in the same order as joint_names
        current_positions = {}
        for i, name in enumerate(self.current_joints.name):
            current_positions[name] = self.current_joints.position[i]
        
        joint_names = [
            'shoulder_pan_joint',
            'shoulder_lift_joint',
            'elbow_joint',
            'wrist_1_joint',
            'wrist_2_joint',
            'wrist_3_joint'
        ]
        
        current = [current_positions[name] for name in joint_names]
        
        # Make a small change
        target = current.copy()
        target[0] += 0.1  # Move shoulder_pan by 0.1 radians
        
        self.get_logger().info(f"Moving from: {[f'{j:.3f}' for j in current]}")
        self.get_logger().info(f"Moving to:   {[f'{j:.3f}' for j in target]}")
        
        # Create trajectory with TWO points (start + end)
        traj = JointTrajectory()
        traj.header.stamp = self.get_clock().now().to_msg()
        traj.joint_names = joint_names
        
        # Point 1: Current position (at t=0)
        point1 = JointTrajectoryPoint()
        point1.positions = current
        point1.velocities = [0.0] * 6
        point1.time_from_start = Duration(sec=0, nanosec=0)
        
        # Point 2: Target position (at t=3s)
        point2 = JointTrajectoryPoint()
        point2.positions = target
        point2.velocities = [0.0] * 6
        point2.time_from_start = Duration(sec=3, nanosec=0)
        
        traj.points = [point1, point2]
        
        self.get_logger().info("Publishing trajectory with 2 points (current -> target)...")
        self.traj_pub.publish(traj)
        self.get_logger().info("✓ Trajectory published! The robot should move now...")
        
        # Monitor for 5 seconds
        self.create_timer(1.0, self.monitor_movement)
        self.monitor_count = 0
    
    def monitor_movement(self):
        self.monitor_count += 1
        if self.monitor_count > 5:
            return
        
        current_positions = {}
        for i, name in enumerate(self.current_joints.name):
            current_positions[name] = self.current_joints.position[i]
        
        shoulder_pan = current_positions['shoulder_pan_joint']
        self.get_logger().info(f"[{self.monitor_count}s] shoulder_pan = {shoulder_pan:.3f} rad")

def main(args=None):
    rclpy.init(args=args)
    node = SimpleMoveTester()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()