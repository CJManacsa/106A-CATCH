from setuptools import find_packages
from setuptools import setup

setup(
    name='catch_custom_msgs',
    version='0.0.0',
    packages=find_packages(
        include=('catch_custom_msgs', 'catch_custom_msgs.*')),
)
