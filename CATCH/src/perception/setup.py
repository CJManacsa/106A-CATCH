from setuptools import find_packages, setup

package_name = 'perception'

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
    maintainer_email='samdreahsu@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'process_depth_image = perception.process_depth_image:main',
            'display_plane = perception.find_table_plane:main',
            'color_identifier = perception.color_identifier:main',
            'ball_trajectory_estimator = perception.ball_trajectory_estimator:main',
            'blob_detector = perception.blob_detector_ros2:main',
            'zxLS = perception.zxLS:main',    
        ],
    },
)
