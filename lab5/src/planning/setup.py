from setuptools import find_packages, setup

package_name = 'planning'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ee106a-tah',
    maintainer_email='danielmunicio360@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'main = planning.main:main',
            'tf = planning.static_tf_transform:main',
            'pyroki_test = planning.pyroki_test:main',
            'robot_control = planning.robot_control:main',
            'debug_catcher = planning.debug_ball_catcher:main',
            'topic_catcher = planning.topic_ball_catcher:main',
            'single_pos = planning.single_pos:main',
            'current_pos = planning.current_pos:main',
            'publish_ball = planning.ball_hitpoint_publisher:main',
            'ball_catcher_node = planning.ball_catcher_node:main',
            'pyroki_moveit = planning.pyroki_with_moveit:main'
        ],
    },
)
