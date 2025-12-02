from setuptools import find_packages
from setuptools import setup

setup(
    name='mover_services',
    version='0.0.0',
    packages=find_packages(
        include=('mover_services', 'mover_services.*')),
)
