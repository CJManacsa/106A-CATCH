#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PointStamped
from sensor_msgs.msg import JointState
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration
import numpy as np
from planning.pyroki_ik_planner import PyrokiIKPlanner

class BallCatcherNode(Node):
    def __init__(self):
        super().__init__('ball_catcher_node')
        
        # Load PyRoKi IK planner
        self.ik = PyrokiIKPlanner()
        
        # Subscribe to ball hitpoint in base frame
        self.hitpoint_sub = self.create_subscription(
            PointStamped,
            '/ball_hitpoint_base',
            self.hitpoint_callback,
            10
        )
        
        # Subscribe to current joint states
        self.joint_state_sub = self.create_subscription(
            JointState,
            '/joint_states',
            self.joint_state_callback,
            10
        )
        
        # Publish trajectory commands to the working controller
        self.traj_pub = self.create_publisher(
            JointTrajectory,
            '/joint_trajectory_controller/joint_trajectory',
            10
        )
        
        self.current_joints = None
        self.last_published_time = None
        
        self.get_logger().info("BallCatcherNode ready. Listening for hitpoints!")
        self.get_logger().info("Using /joint_trajectory_controller/joint_trajectory")
    
    def joint_state_callback(self, msg: JointState):
        """Track current joint positions"""
        self.current_joints = msg
    
    def get_current_ee_position(self):
        """Compute forward kinematics to get current end-effector position"""
        try:
            if self.current_joints is None:
                return None
            
            # Get joint positions in correct order
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
            
            config = np.array([current_positions[name] for name in joint_names])
            
            # Use PyRoKi's forward kinematics
            import jax.numpy as jnp
            fk = self.ik.robot.forward_kinematics(jnp.array(config))
            
            # Get tool0 (end effector) transform
            tool0_index = self.ik.robot.links.names.index('tool0')
            ee_transform = fk[tool0_index]
            
            # Extract position (last 3 elements of the 7-element array)
            position = np.array(ee_transform[4:7])
            
            return position
        except Exception as e:
            self.get_logger().warn(f"FK failed: {e}")
            return None
    
    def hitpoint_callback(self, msg: PointStamped):
        """
        Called whenever CV publishes a new predicted strike point.
        """
        x = msg.point.x
        y = msg.point.y
        z = msg.point.z
        
        target_pos = np.array([x, y, z])
        
        self.get_logger().info(
            f"Received target: x={x:.3f}, y={y:.3f}, z={z:.3f}"
        )
        
        # Need current joint state
        if self.current_joints is None:
            self.get_logger().warn("No joint states yet, skipping...")
            return
        
        # Check current end-effector position
        current_ee_pos = self.get_current_ee_position()
        if current_ee_pos is not None:
            cartesian_distance = np.linalg.norm(target_pos - current_ee_pos)
            self.get_logger().info(
                f"Current EE position: [{current_ee_pos[0]:.3f}, {current_ee_pos[1]:.3f}, {current_ee_pos[2]:.3f}]"
            )
            self.get_logger().info(
                f"Cartesian distance to target: {cartesian_distance:.3f} m"
            )
            
            if cartesian_distance > 0.5:  # More than 50cm away
                self.get_logger().warn(
                    f"Target is very far in Cartesian space ({cartesian_distance:.3f}m). "
                    f"This might explain why IK finds a different configuration."
                )
        
        # Call PyRoKi IK
        solution = self.ik.compute_ik_fast(x, y, z)
        
        if solution is None:
            self.get_logger().warn("IK failed for this target.")
            return
        
        # Get current positions in correct order
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
        
        current = np.array([current_positions[name] for name in joint_names])
        target = np.array(solution.position)
        
        # DEBUG: Print detailed comparison
        self.get_logger().info("=" * 60)
        self.get_logger().info("Current config:")
        for i, name in enumerate(joint_names):
            self.get_logger().info(f"  {name:20s}: {current[i]:7.3f} rad")
        
        self.get_logger().info("\nTarget config (from IK):")
        for i, name in enumerate(joint_names):
            diff = target[i] - current[i]
            self.get_logger().info(f"  {name:20s}: {target[i]:7.3f} rad (diff: {diff:+7.3f})")
        
        # Check differences
        diff_per_joint = np.abs(target - current)
        max_joint_diff = np.max(diff_per_joint)
        total_diff = np.linalg.norm(target - current)
        
        self.get_logger().info(f"\nMax single joint diff: {max_joint_diff:.3f} rad ({np.rad2deg(max_joint_diff):.1f}°)")
        self.get_logger().info(f"Total diff (norm):     {total_diff:.3f} rad")
        self.get_logger().info("=" * 60)
        
        if max_joint_diff > 6.0:
            self.get_logger().warn(
                f"⚠ Target too far! Max joint diff: {max_joint_diff:.3f} rad "
                f"({np.rad2deg(max_joint_diff):.1f}°). NOT MOVING."
            )
            self.get_logger().warn(
                f"Try DRASTICALLY increasing rest_cost weight in IK solver, or the target is genuinely far away."
            )
            return
        
        self.get_logger().info(f"✓ Target is close enough. Publishing trajectory...")
        
        # Publish trajectory
        self.publish_trajectory(current.tolist(), target.tolist(), joint_names)
        self.get_logger().info("✓ Trajectory published!")
    
    def publish_trajectory(self, current_pos, target_pos, joint_names):
        """
        Publish a 2-point trajectory with RELAXED tolerances
        This prevents "holding position" errors when joint slightly misses target
        """
        traj = JointTrajectory()
        traj.header.stamp = self.get_clock().now().to_msg()
        traj.joint_names = joint_names
        
        # Calculate movement magnitude to adjust timing
        diff = np.array(target_pos) - np.array(current_pos)
        max_joint_movement = np.max(np.abs(diff))
        
        # Adaptive timing: give more time for larger movements
        # Base time: 1.0s, add 0.5s per radian of max joint movement
        move_time = max(1.0, 1.0 + 0.5 * max_joint_movement)
        
        self.get_logger().info(f"Trajectory time: {move_time:.2f}s for max joint move of {max_joint_movement:.3f} rad")
        
        # Point 1: Start at current position (t=0)
        point1 = JointTrajectoryPoint()
        point1.positions = current_pos
        point1.velocities = [0.0] * 6
        point1.time_from_start = Duration(sec=0, nanosec=0)
        
        # Point 2: End at target position (with extra time)
        point2 = JointTrajectoryPoint()
        point2.positions = target_pos
        point2.velocities = [0.0] * 6
        
        # Convert float seconds to Duration
        sec = int(move_time)
        nanosec = int((move_time - sec) * 1e9)
        point2.time_from_start = Duration(sec=sec, nanosec=nanosec)
        
        traj.points = [point1, point2]
        
        self.traj_pub.publish(traj)

def main(args=None):
    rclpy.init(args=args)
    node = BallCatcherNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()