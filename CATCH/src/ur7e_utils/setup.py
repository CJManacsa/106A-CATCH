from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'ur7e_utils'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/urdf', ['urdf/ur7e_with_pedestal.urdf.xacro']),
        (os.path.join('share', package_name, 'calibration'), glob('calibration/*')),
        (os.path.join('share', package_name, 'launch'), glob('launch/*')),
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
            'tuck_robot = ur7e_utils.tuck:main',
            'keyboard_controller = ur7e_utils.keyboard_controller:main',
            'enable_gripper = ur7e_utils.gripper:main',
        ],
    },
    scripts=[
        'scripts/freedrive',
        'scripts/enable_comms',
        'scripts/tuck',
        'scripts/reset_state',
    ]
)

