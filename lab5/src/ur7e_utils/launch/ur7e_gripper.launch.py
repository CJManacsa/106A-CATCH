# File: launch/ur7e_full.launch.py
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription, ExecuteProcess, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    # Get robot name from environment
    robot_name = os.environ.get('EE106_UR_ROBOT_NAME', 'ur7e')    # Get package paths
    ur7e_utils_pkg = get_package_share_directory('ur7e_utils')
    ur_robot_driver_pkg = get_package_share_directory('ur_robot_driver')    # Construct calibration file path
    calib_file = os.path.join(
        ur7e_utils_pkg,
        'calibration',
        f"{robot_name}_calibration.yaml"
    )    # Path to UR control launch file
    ur_control_launch_file = os.path.join(
        ur_robot_driver_pkg,
        'launch',
        'ur_control.launch.py'
    )    # Service call to set speed slider (run after driver starts)
    set_speed_slider = ExecuteProcess(
        cmd=[
            'ros2', 'service', 'call',
            '/io_and_status_controller/set_speed_slider',
            'ur_msgs/srv/SetSpeedSliderFraction',
            '{speed_slider_fraction: 0.1}'
        ],
        output='screen'
    )    
    return LaunchDescription([
        # 1. Run enable_gripper node
        Node(
            package='ur7e_utils',
            executable='enable_gripper',
            name='enable_gripper',
            output='screen'
        ),        # 2. Launch ur_control.launch.py with required args
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(ur_control_launch_file),
            launch_arguments={
                'ur_type': 'ur7e',
                'robot_ip': os.environ.get('EE106_UR_ROBOT_IP', ''),
                'headless_mode': 'true',
                'kinematics_params_file': calib_file,
                'launch_rviz': 'false'
            }.items()
        ),
        # 3. Delay service call until controller is up (e.g. 10 s)
        TimerAction(period=5.0, actions=[set_speed_slider]),
    ])
