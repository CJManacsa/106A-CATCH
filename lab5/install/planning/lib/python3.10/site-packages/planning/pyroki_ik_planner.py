#!/usr/bin/env python3
"""
Clean PyRoKi IK planner (integrated with your working URDF loader)
Designed for UR7e + real-time target points.
"""

import os
import tempfile
import subprocess

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import numpy as np

# PyRoKi and dependencies
import pyroki as pk
import jax.numpy as jnp
import jaxlie
import jaxls
import jax_dataclasses as jdc
import yourdfpy


class PyrokiIKPlanner(Node):
    """
    Minimal IK planner used by BallCatchNode.
    Loads URDF correctly, subscribes to joint_states,
    and provides compute_ik(x,y,z).
    """

    def __init__(self,
                 xacro_path=None,
                 end_effector_link="tool0"):
        super().__init__("pyroki_ik_planner")

        self.target_link_name = end_effector_link

        # ----------------------------------------------------
        # 1. Load URDF (from xacro if needed)
        # ----------------------------------------------------
        if xacro_path is None:
            xacro_path = self._find_xacro()

        self.get_logger().info(f"Processing xacro: {xacro_path}")

        try:
            doc = self._process_xacro(xacro_path)
            urdf_xml = doc
        except Exception as e:
            self.get_logger().error(f"Xacro processing failed: {e}")
            raise

        try:
            urdf = yourdfpy.URDF.load(urdf_xml)
            self.get_logger().info("URDF successfully parsed with yourdfpy")
        except Exception as e:
            self.get_logger().error(f"URDF parsing failed: {e}")
            raise

        # ----------------------------------------------------
        # 2. Build PyRoKi robot model
        # ----------------------------------------------------
        self.robot = pk.Robot.from_urdf(urdf)
        self.end_effector_link = end_effector_link

        self.get_logger().info(
            f"PyRoKi robot loaded. Actuated joints: "
            f"{self.robot.joints.num_actuated_joints}"
        )

        # ----------------------------------------------------
        # 3. Joint state subscription (for rest cost)
        # ----------------------------------------------------
        self.current_joint_state = None
        self.joint_sub = self.create_subscription(
            JointState,
            "/joint_states",
            self.joint_state_callback,
            10
        )

        # Store target link index as int
        self.target_link_index = self.robot.links.names.index(self.target_link_name)
        self.get_logger().info(f"Target link '{self.target_link_name}' has index: {self.target_link_index}")

        self.get_logger().info("PyRoKi IK Planner initialized.")

    # ============================================================
    #                    URDF / XACRO Loading
    # ============================================================

    def _find_xacro(self):
        """Try to find the UR description xacro."""
        from ament_index_python.packages import get_package_share_directory

        ur_desc_dir = get_package_share_directory("ur_description")
        xacro_file = os.path.join(ur_desc_dir, "urdf", "ur.urdf.xacro")

        if not os.path.exists(xacro_file):
            raise FileNotFoundError(f"UR xacro not found: {xacro_file}")

        return xacro_file

    def _process_xacro(self, xacro_file):
        """
        Process the xacro file into a real URDF file.
        Returns the PATH to a generated .urdf file.
        """
        # Create temp file to store URDF output
        temp = tempfile.NamedTemporaryFile(delete=False, suffix=".urdf")
        temp_path = temp.name
        temp.close()

        # Run xacro with UR7e argument
        cmd = [
            "xacro",
            xacro_file,
            "ur_type:=ur7e",
            "name:=ur"
        ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )

        if result.returncode != 0:
            raise RuntimeError(
                f"xacro failed:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
            )

        # Write the URDF XML to the temp file
        with open(temp_path, "w") as f:
            f.write(result.stdout)

        return temp_path

    # ============================================================
    #                    Joint State Callback
    # ============================================================

    def joint_state_callback(self, msg):
        self.current_joint_state = msg

    # ============================================================
    #                    Public IK Interface
    # ============================================================

    def compute_ik(self, x, y, z):
        """
        Compute IK for position-only target.
        Orientation is ignored (end effector maintains current orientation).
        Returns JointState or None.
        """
        target_position = np.array([x, y, z])
        target_wxyz = np.array([1.0, 0.0, 0.0, 0.0])

        try:
            cfg = self._solve_ik_pyroki(target_wxyz, target_position)
        except Exception as e:
            self.get_logger().error(f"IK failure: {e}")
            import traceback
            traceback.print_exc()
            return None

        msg = JointState()
        msg.name = [
            'shoulder_pan_joint', 'shoulder_lift_joint',
            'elbow_joint', 'wrist_1_joint',
            'wrist_2_joint', 'wrist_3_joint'
        ]
        msg.position = cfg.tolist()
        return msg

    def compute_ik_fast(self, x, y, z):
        """
        Simplified wrapper - position only.
        """
        return self.compute_ik(x=x, y=y, z=z)

    # ============================================================
    #                    Internal IK Solver
    # ============================================================

    def _solve_ik_pyroki(self, target_wxyz: np.ndarray, target_position: np.ndarray) -> np.ndarray:
        """
        Prepare inputs and call jitted solver.
        Returns a numpy array of joint angles.
        """
        assert target_position.shape == (3,) and target_wxyz.shape == (4,)
        
        # Build SE3 target
        T_world_target = jaxlie.SE3(
            jnp.concatenate([jnp.array(target_wxyz), jnp.array(target_position)], axis=-1)
        )
        
        target_link_index = self.robot.links.names.index(self.target_link_name)
        
        # Get current config if available - used for rest cost
        if self.current_joint_state is not None and len(self.current_joint_state.position) >= 6:
            current_config = jnp.array(self.current_joint_state.position[:6])
        else:
            current_config = None
        
        # Call the JIT-compiled JAX function
        cfg = self._solve_ik_jax(
            self.robot,
            T_world_target,
            jnp.array(target_link_index),
            current_config,
        )
        
        assert cfg.shape == (self.robot.joints.num_actuated_joints,)
        return np.array(cfg)

    # ============================================================
    #                    JAX IK Solver (Position-Only)
    # ============================================================

    @staticmethod
    @jdc.jit
    def _solve_ik_jax(
        robot: pk.Robot,
        T_world_target: jaxlie.SE3,
        target_link_index: jnp.ndarray,
        current_config: jnp.ndarray = None,
    ) -> jnp.ndarray:
        """
        JIT'd IK solver for POSITION-ONLY.
        Uses pose_cost (not analytic_jac) to avoid batch dimension issues.
        """
        
        # Initialize with 0 (default) to avoid batch issues
        joint_var = robot.joint_var_cls(0)
        
        # Define cost factors
        factors = [
            # Use regular pose_cost instead of pose_cost_analytic_jac
            pk.costs.pose_cost(
                robot,
                joint_var,
                target_pose=T_world_target,
                target_link_index=target_link_index,
                pos_weight=50.0,  # High weight for position accuracy
                ori_weight=0.0,   # POSITION ONLY - ignore orientation
            ),
            pk.costs.limit_cost(
                robot,
                joint_var,
                weight=100.0,  # High weight to respect joint limits
            ),
        ]
        
        # Add strong rest cost if current config provided
        if current_config is not None:
            factors.append(
                pk.costs.rest_cost(
                    joint_var,
                    rest_pose=current_config,
                    weight=10.0,  # VERY STRONG weight to stay close to current config
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