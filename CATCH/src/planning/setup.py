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
            'debug_catcher = planning.debug_ball_catcher:main',
            'current_pos = planning.current_pos:main',
            'publish_ball = planning.ball_hitpoint_publisher:main',
            'tf = planning.static_tf_transform:main',
            'pyroki_moveit = planning.pyroki_with_moveit:main'
        ],
    },
)
