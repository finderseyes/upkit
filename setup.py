import subprocess

import setuptools
from sys import platform
from setuptools.command.install import install

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='unity-tools',
    version='0.3.0',
    scripts=['unity-tools.py'],
    entry_points={
        'console_scripts': [
            'unity-tools = unity_tools.tools:execute_from_command_line',
        ],
    },
    author='Vu Le (findereyes)',
    author_email='tuongvu@gmail.com',
    description='Project and package manager for Unity3D',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/finderseyes/unity-tools',
    packages=setuptools.find_packages(),
    install_requires=['xmltodict', 'pyyaml', 'yamlordereddictloader', 'jinja2',],
    classifiers=[
        'Programming Language :: Python :: 2',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)

