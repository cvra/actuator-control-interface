#!/usr/bin/env python

from setuptools import setup, find_packages

args = dict(
    name='cvra_actuatorpub',
    version='0.1',
    description='Publish Actuator Trajectories Via CVRA SimpleRPC',
    packages=['cvra_actuatorpub'],
    install_requires=['cvra_rpc'],
    author='Antoine Albertelli',
    author_email='a.albertelli@cvra.ch',
    url='https://github.com/cvra',
    license='BSD'
)

setup(**args)
