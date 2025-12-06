# File: launch/ur7e_full_with_pedestal.launch.py
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os
import xacro

def generate_launch_description():
    # -----------------------------
    # Get robot name and package paths
    # -----------------------------
    robot_name = os.environ.get('EE106_UR_ROBOT_NAME', 'ur7e')
    ur7e_utils_pkg = get_package_share_directory('ur7e_utils')
    ur_robot_driver_pkg = get_package_share_directory('ur_robot_driver')

    # -----------------------------
    # Calibration YAML path
    # -----------------------------
    calib_file = os.path.join(
        ur7e_utils_pkg,
        'calibration',
        f"{robot_name}_calibration.yaml"
    )

    # -----------------------------
    # Pedestal + UR7e XACRO path
    # -----------------------------
    pedestal_xacro = os.path.join(
        ur7e_utils_pkg,
        'urdf',
        'ur7e_with_pedestal.urdf.xacro'
    )

    # Process XACRO into XML string
    robot_description_config = xacro.process_file(pedestal_xacro).toxml()

    # -----------------------------
    # Path to ur_control.launch.py
    # -----------------------------
    ur_control_launch_file = os.path.join(
        ur_robot_driver_pkg,
        'launch',
        'ur_control.launch.py'
    )

    # -----------------------------
    # Launch Description
    # -----------------------------
    return LaunchDescription([
        # 1. Enable gripper node
        Node(
            package='ur7e_utils',
            executable='enable_gripper',
            name='enable_gripper',
            output='screen'
        ),

        # 2. Launch UR driver with pedestal in robot_description
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(ur_control_launch_file),
            launch_arguments={
                'ur_type': 'ur7e',
                'robot_ip': os.environ.get('EE106_UR_ROBOT_IP', ''),
                'headless_mode': 'true',
                'kinematics_params_file': calib_file,
                'launch_rviz': 'false',  # Set false if headless
                'robot_description': robot_description_config
            }.items()
        )
    ])

