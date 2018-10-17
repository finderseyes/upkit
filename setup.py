import subprocess

import setuptools
from sys import platform
from setuptools.command.install import install


class InstallOSXTools(install):
    def run(self):
        if platform == 'osx':
            command = 'brew install hardlink-osx'
            process = subprocess.Popen(command, shell=True)
            process.wait()
            install.run(self)


with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='unity-tools',
    version='0.1',
    scripts=['unity-tools'],
    author='Vu Le',
    author_email='tuongvu@gmail.com',
    description='Unity3D project utilities',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/finderseyes/unity-tools',
    packages=setuptools.find_packages(),
    install_requires=['xmltodict', 'pyyaml', 'jinja2', 'ntpath'],
    cmdclass={
        'install-osx-tools': InstallOSXTools
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)

