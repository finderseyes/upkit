import setuptools

from upkit import __version__

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='upkit',
    version=__version__,
    # scripts=['upkit.py'],
    entry_points={
        'console_scripts': [
            'upkit = upkit.tools:execute_from_command_line',
        ],
    },
    author='Vu Le (findereyes)',
    author_email='tuongvu@gmail.com',
    description='Project and package manager for Unity3D',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/finderseyes/upkit',
    packages=setuptools.find_packages(),
    install_requires=['xmltodict', 'pyyaml', 'yamlordereddictloader', 'jinja2',],
    classifiers=[
        'Programming Language :: Python :: 2',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)

