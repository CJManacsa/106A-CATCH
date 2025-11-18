from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package="perception",
            executable="track_ball",
            name="track_ball",
            output="screen",
            parameters=[
                {"camera_topic": "/camera/camera/color/image_raw"},
                {"resize_width": 320},
                {"resize_height": 240},
                {"h_low": 5},
                {"s_low": 120},
                {"v_low": 100},
                {"h_high": 10},
                {"s_high": 255},
                {"v_high": 255},
                {"min_area_px": 150},
                {"publish_debug_image": True},
            ],
        ),
    ])
