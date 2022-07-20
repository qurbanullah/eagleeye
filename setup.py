#!/usr/bin/env python

"""
setup.py file for eagleeye
"""

import os
from setuptools import setup, find_packages

prefix = os.environ.get("prefix", "/usr")
name = 'eagleeye'
version = '0.3.0'


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name=name,
    version=version,
    author="Qurban Ullah",
    author_email="qurbanullah@avouch.org>",
    description="Avouch Linux package installer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="<https://github.com/avouchlinux/eagleeye>",
    packages=find_packages(exclude=('test')),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPL License",
        "Operating System :: OS Independent",
    ],
    command_options={
        'build_sphinx': {
            'project': ('setup.py', name),
            'version': ('setup.py', version),
            'release': ('setup.py', version),
        }
    },
    entry_points={
        # Install a script
        'console_scripts': [
            'ee = eagleeye.eagleeye:main',
        ],
    },
    python_requires='>=3.10',
    install_requires=[
        'zstandard',
        'pathlib',
        'tqdm',
        'shutil',
        'tempfile',
        'tarfile',
        'argparse',
        'xml.etree.ElementTree',
    ],
)