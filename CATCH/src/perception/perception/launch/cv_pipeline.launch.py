from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='perception',
            executable='blob_detector',
            name='blob_detector',
            output='screen'
        ),
        Node(
            package='perception',
            executable='process_depth_image',
            name='process_depth_image',
            output='screen'
        ),
        Node(
            package='perception',
            executable='ball_trajectory_estimator',
            name='ball_trajectory_estimator',
            output='screen'
        ),
        # Node(
        #     package='perception',
        #     executable='closest_predicted_point',
        #     name='closest_predicted_point',
        #     output='screen'
        # ),
    ])
