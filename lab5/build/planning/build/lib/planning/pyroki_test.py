#!/usr/bin/env python3
"""
Fast IK solver using PyRoKi for real-time ball catching with UR7e
Based on actual PyRoKi API from pyroki_snippets
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from geometry_msgs.msg import PoseStamped
import numpy as np
from scipy.spatial.transform import Rotation as R
import time

# PyRoKi imports - based on actual pyroki_snippets code
import pyroki as pk
import jax.numpy as jnp
import jaxlie
import jaxls
import jax_dataclasses as jdc
import yourdfpy  # CRITICAL: PyRoKi uses yourdfpy to parse URDF


class PyRokiIKPlanner(Node):
    def __init__(self, urdf_path=None):
        super().__init__('pyroki_ik_planner')
        
        # If no URDF path provided, try to find it from ur_description package
        if urdf_path is None:
            urdf_path = self._find_ur7e_urdf()
        
        self.get_logger().info(f'Loading URDF from: {urdf_path}')
        
        # Load URDF using yourdfpy (PyRoKi expects a yourdfpy.URDF object, not a path!)
        try:
            urdf = yourdfpy.URDF.load(urdf_path)
            self.get_logger().info(f'URDF loaded successfully')
        except Exception as e:
            self.get_logger().error(f'Failed to load URDF: {e}')
            raise
        
        # Initialize PyRoKi robot model - actual API
        self.robot = pk.Robot.from_urdf(urdf)
        
        self.target_link_name = 'tool0'  # UR7e end effector
        self.current_joint_state = None
        
        # Subscribe to joint states for reference
        self.joint_sub = self.create_subscription(
            JointState,
            '/joint_states',
            self.joint_state_callback,
            10
        )
        
        self.get_logger().info('PyRoKi IK Planner initialized')
        self.get_logger().info(f'Robot has {self.robot.joints.num_actuated_joints} actuated joints')
    
    def _find_ur7e_urdf(self):
        """Try to find the UR7e URDF file in common locations"""
        import os
        from ament_index_python.packages import get_package_share_directory
        import subprocess
        import tempfile
        
        try:
            ur_desc_path = get_package_share_directory('ur_description')
            self.get_logger().info(f'Found ur_description package at: {ur_desc_path}')
            
            # The UR description uses xacro files, we need to process them
            xacro_file = os.path.join(ur_desc_path, 'urdf', 'ur.urdf.xacro')
            
            if not os.path.exists(xacro_file):
                raise FileNotFoundError(f'Could not find xacro file: {xacro_file}')
            
            self.get_logger().info(f'Found xacro file: {xacro_file}')
            self.get_logger().info('Processing xacro to generate URDF for UR7e...')
            
            # Create a temporary file for the processed URDF
            temp_urdf = tempfile.NamedTemporaryFile(mode='w', suffix='.urdf', delete=False)
            temp_urdf_path = temp_urdf.name
            temp_urdf.close()
            
            # Process xacro file with ur_type:=ur7e parameter
            # This generates the URDF for the UR7e specifically
            try:
                result = subprocess.run(
                    ['xacro', xacro_file, 'ur_type:=ur7e', 'name:=ur'],
                    capture_output=True,
                    text=True,
                    check=True
                )
                
                # Write the output to temp file
                with open(temp_urdf_path, 'w') as f:
                    f.write(result.stdout)
                
                self.get_logger().info(f'Successfully generated URDF at: {temp_urdf_path}')
                return temp_urdf_path
                
            except subprocess.CalledProcessError as e:
                self.get_logger().error(f'Failed to process xacro: {e.stderr}')
                raise
            except FileNotFoundError:
                self.get_logger().error('xacro command not found. Install with: sudo apt install ros-humble-xacro')
                raise
            
        except Exception as e:
            self.get_logger().error(f'Error finding/processing URDF: {e}')
            raise
    
    def joint_state_callback(self, msg: JointState):
        """Store current joint state for reference"""
        self.current_joint_state = msg
    
    def compute_ik_fast(self, x, y, z, qx=0.0, qy=1.0, qz=0.0, qw=0.0):
        """
        Fast IK computation using PyRoKi (based on actual solve_ik from pyroki_snippets)
        
        Args:
            x, y, z: Target position in base_link frame
            qx, qy, qz, qw: Target orientation quaternion (xyzw order)
        
        Returns:
            JointState message with solution, or None if failed
        """
        
        # Convert to wxyz order (as PyRoKi expects)
        target_wxyz = np.array([qw, qx, qy, qz])
        target_position = np.array([x, y, z])
        
        start_time = time.perf_counter()
        
        try:
            # Call the actual PyRoKi solve_ik function
            cfg = self._solve_ik_pyroki(
                target_wxyz=target_wxyz,
                target_position=target_position
            )
            
            solve_time_ms = (time.perf_counter() - start_time) * 1000
            
            # Convert to JointState message
            joint_solution = JointState()
            joint_solution.name = [
                'shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint',
                'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint'
            ]
            joint_solution.position = cfg.tolist()
            
            self.get_logger().info(f'IK solved in {solve_time_ms:.2f}ms')
            
            return joint_solution
            
        except Exception as e:
            solve_time_ms = (time.perf_counter() - start_time) * 1000
            self.get_logger().error(f'IK failed after {solve_time_ms:.2f}ms: {e}')
            return None
    
    def _solve_ik_pyroki(self, target_wxyz: np.ndarray, target_position: np.ndarray) -> np.ndarray:
        """
        Direct implementation based on pyroki_snippets/_solve_ik.py
        
        This is the actual PyRoKi IK solver setup
        """
        assert target_position.shape == (3,) and target_wxyz.shape == (4,)
        
        target_link_index = self.robot.links.names.index(self.target_link_name)
        
        # Get current config if available (for rest cost)
        current_config = None
        if self.current_joint_state is not None and len(self.current_joint_state.position) >= 6:
            current_config = jnp.array(self.current_joint_state.position[:6])
        
        # Call the JIT-compiled JAX function
        cfg = self._solve_ik_jax(
            self.robot,
            jnp.array(target_link_index),
            jnp.array(target_wxyz),
            jnp.array(target_position),
            current_config,  # Pass current config for rest cost
        )
        
        assert cfg.shape == (self.robot.joints.num_actuated_joints,)
        return np.array(cfg)
    
    @staticmethod
    @jdc.jit
    def _solve_ik_jax(
        robot: pk.Robot,
        target_link_index: jnp.ndarray,
        target_wxyz: jnp.ndarray,
        target_position: jnp.ndarray,
        current_config: jnp.ndarray = None,  # Add current config parameter
    ) -> jnp.ndarray:
        """
        JAX-compiled IK solver - based on pyroki_snippets/_solve_ik.py
        
        This uses:
        - pose_cost_analytic_jac: Fast analytical Jacobian for pose matching
        - limit_cost: Keeps joints within limits
        - rest_cost: Bias toward current configuration (avoid big jumps)
        - LeastSquaresProblem with Levenberg-Marquardt solver
        """
        # Create joint variable
        joint_var = robot.joint_var_cls(0)
        
        # Define cost factors
        factors = [
            pk.costs.pose_cost_analytic_jac(
                robot,
                joint_var,
                jaxlie.SE3.from_rotation_and_translation(
                    jaxlie.SO3(target_wxyz), target_position
                ),
                target_link_index,
                pos_weight=50.0,  # High weight for position accuracy
                ori_weight=10.0,   # Lower weight for orientation
            ),
            pk.costs.limit_cost(
                robot,
                joint_var,
                weight=100.0,  # High weight to respect joint limits
            ),
        ]
        
        # Add rest cost if current config provided (bias toward current pose)
        if current_config is not None:
            factors.append(
                pk.costs.rest_cost(
                    joint_var,
                    rest_pose=current_config,
                    weight=0.1,  # Low weight - just a preference, not a requirement
                )
            )
        
        # Solve using Levenberg-Marquardt
        sol = (
            jaxls.LeastSquaresProblem(factors, [joint_var])
            .analyze()
            .solve(
                verbose=False,
                linear_solver="dense_cholesky",
                trust_region=jaxls.TrustRegionConfig(lambda_initial=1.0),
            )
        )
        
        return sol[joint_var]
    
    def compute_ik_with_current_state(self, current_joint_state, x, y, z, 
                                     qx=0.0, qy=1.0, qz=0.0, qw=0.0):
        """
        Compatibility wrapper that matches the MoveIt IK interface
        
        Args:
            current_joint_state: JointState (currently not used for seeding, but could be)
            x, y, z: Target position
            qx, qy, qz, qw: Target orientation quaternion
        
        Returns:
            JointState with solution or None
        """
        # For now, we don't use current_joint_state as seed
        # PyRoKi's default initialization seems to work well
        # TODO: Could add rest_cost to bias toward current configuration
        
        return self.compute_ik_fast(x, y, z, qx, qy, qz, qw)


class FastBallCatcher(Node):
    """
    Example node for testing fast IK with a fixed target point
    """
    def __init__(self):
        super().__init__('fast_ball_catcher')
        
        # Initialize PyRoKi IK planner
        self.pyroki_planner = PyRokiIKPlanner()
        
        # Subscribe to joint states
        self.joint_state_sub = self.create_subscription(
            JointState, '/joint_states', 
            self.joint_state_callback, 10
        )
        
        self.current_joint_state = None
        self.has_solved = False  # Only solve once for testing
        
        self.get_logger().info('Fast Ball Catcher initialized - waiting for joint states')
    
    def joint_state_callback(self, msg: JointState):
        self.current_joint_state = msg
        
        # Test with a fixed point once
        if not self.has_solved and self.current_joint_state is not None:
            self.test_fixed_point()
    
    def test_fixed_point(self):
        """Test IK solver with a fixed target point"""
        self.has_solved = True
        
        # Use a reachable test point (similar to your cube grasping)
        target_x = 0.4
        target_y = 0.1
        target_z = 0.3
        
        self.get_logger().info(f'Testing PyRoKi IK to reach point ({target_x}, {target_y}, {target_z})')
        
        solution = self.pyroki_planner.compute_ik_fast(
            target_x, target_y, target_z
        )
        
        if solution:
            self.get_logger().info(f'✓ IK Solution found!')
            self.get_logger().info(f'Joint angles: {[f"{j:.3f}" for j in solution.position]}')
            
            # Benchmark speed
            self.benchmark_ik_speed()
        else:
            self.get_logger().error(f'✗ IK failed')
    
    def benchmark_ik_speed(self):
        """Run multiple IK solves to benchmark speed"""
        self.get_logger().info('\nBenchmarking IK solver speed...')
        
        num_tests = 20
        solve_times = []
        
        # Test different target positions
        for i in range(num_tests):
            # Vary the target position
            x = 0.3 + i * 0.01
            y = 0.0 + (i % 5) * 0.02
            z = 0.2 + (i % 3) * 0.03
            
            start = time.perf_counter()
            solution = self.pyroki_planner.compute_ik_fast(x, y, z)
            elapsed = (time.perf_counter() - start) * 1000
            
            if solution:
                solve_times.append(elapsed)
        
        if solve_times:
            avg_time = np.mean(solve_times)
            max_time = np.max(solve_times)
            min_time = np.min(solve_times)
            
            self.get_logger().info(f'\nIK Speed Benchmark Results ({len(solve_times)}/{num_tests} successful):')
            self.get_logger().info(f'  Average: {avg_time:.2f}ms')
            self.get_logger().info(f'  Min: {min_time:.2f}ms')
            self.get_logger().info(f'  Max: {max_time:.2f}ms')
            
            # Note: First solve will be slower due to JAX JIT compilation
            if len(solve_times) > 1:
                avg_after_first = np.mean(solve_times[1:])
                self.get_logger().info(f'  Avg (after JIT): {avg_after_first:.2f}ms')
            
            if avg_time < 10:
                self.get_logger().info('✓ PyRoKi is FAST enough for real-time ball catching!')
            else:
                self.get_logger().warn('⚠ Average solve time may be on the edge for 1s flight time')


def main(args=None):
    rclpy.init(args=args)
    
    # Test the fast ball catcher
    node = FastBallCatcher()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()