from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
import os  
def generate_launch_description():
    pkg_dir = os.path.dirname(os.path.abspath(__file__))
    declared_arguments = []
    declared_arguments.append(
    DeclareLaunchArgument(
              "robot_ip",
              description="IP address of the robot"
          )
    )      
    robot_ip = LaunchConfiguration("robot_ip")      
    ur_control_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
        PathJoinSubstitution([
            FindPackageShare("ur_robot_driver"),
                "launch",
                "ur_control.launch.py"
            ])
        ]),
        launch_arguments={
            "ur_type": "ur7e",
            "robot_ip": robot_ip,
            "description_launchfile": os.path.join(pkg_dir, "custom_ur_rsp.launch.py"),
        }.items(),
      )      
    return LaunchDescription(declared_arguments + [ur_control_launch])