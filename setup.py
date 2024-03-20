from os import getenv
from setuptools import setup

setup(
    name='publish_tools',
    version=f'{getenv("LIB_VERSION")}.0.0',
    author="Igor Bari",
    package_dir={"publish_tools": "src"}
)