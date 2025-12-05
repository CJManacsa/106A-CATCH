from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import (
    Command,
    FindExecutable,
    LaunchConfiguration,
    PathJoinSubstitution,
)
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue
import os


def generate_launch_description():
    pkg_dir = os.path.dirname(os.path.abspath(__file__))

    # Declare the arguments ur_control.launch.py will pass
    declared_arguments = [
        DeclareLaunchArgument("ur_type", description="UR robot type"),
        DeclareLaunchArgument("robot_ip", description="Robot IP address"),
    ]

    ur_type = LaunchConfiguration("ur_type")
    robot_ip = LaunchConfiguration("robot_ip")

    # Your custom files (hardcoded)
    kinematics_file = os.path.join(pkg_dir, "number-5_calibration.yaml")
    description_file = os.path.join(pkg_dir, "ur7e_with_pedestal_and_gripper.urdf.xacro")

    # Standard UR parameter files
    joint_limit_params = PathJoinSubstitution([
        FindPackageShare("ur_description"), "config", ur_type, "joint_limits.yaml"
    ])
    physical_params = PathJoinSubstitution([
        FindPackageShare("ur_description"), "config", ur_type, "physical_parameters.yaml"
    ])
    visual_params = PathJoinSubstitution([
        FindPackageShare("ur_description"), "config", ur_type, "visual_parameters.yaml"
    ])
    script_filename = PathJoinSubstitution([
        FindPackageShare("ur_client_library"), "resources", "external_control.urscript"
    ])
    input_recipe = PathJoinSubstitution([
        FindPackageShare("ur_robot_driver"), "resources", "rtde_input_recipe.txt"
    ])
    output_recipe = PathJoinSubstitution([
        FindPackageShare("ur_robot_driver"), "resources", "rtde_output_recipe.txt"
    ])

    # Build robot description
    robot_description_content = Command([
        PathJoinSubstitution([FindExecutable(name="xacro")]), " ",
        description_file, " ",
        "robot_ip:=", robot_ip, " ",
        "joint_limit_params:=", joint_limit_params, " ",
        "kinematics_params:=", kinematics_file, " ",
        "physical_params:=", physical_params, " ",
        "visual_params:=", visual_params, " ",
        "safety_limits:=true", " ",
        "safety_pos_margin:=0.15", " ",
        "safety_k_position:=20", " ",
        "name:=", ur_type, " ",
        "script_filename:=", script_filename, " ",
        "input_recipe_filename:=", input_recipe, " ",
        "output_recipe_filename:=", output_recipe, " ",
        "tf_prefix:=", " ",
        "use_mock_hardware:=false", " ",
        "mock_sensor_commands:=false", " ",
        "headless_mode:=false", " ",
        "use_tool_communication:=false", " ",
        "tool_parity:=0", " ",
        "tool_baud_rate:=115200", " ",
        "tool_stop_bits:=1", " ",
        "tool_rx_idle_chars:=1.5", " ",
        "tool_tx_idle_chars:=3.5", " ",
        "tool_device_name:=/tmp/ttyUR", " ",
        "tool_tcp_port:=54321", " ",
        "reverse_ip:=0.0.0.0", " ",
        "script_command_port:=50004", " ",
        "reverse_port:=50001", " ",
        "script_sender_port:=50002", " ",
        "trajectory_port:=50003",
    ])

    robot_description = {
        "robot_description": ParameterValue(robot_description_content, value_type=str)
    }

    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="both",
        parameters=[robot_description],
    )

    return LaunchDescription(declared_arguments + [robot_state_publisher_node])
