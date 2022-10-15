#!/usr/bin/python3
# Setup script to install this package.
# M.Blakeney, Mar 2018.

from pathlib import Path
from setuptools import setup

name = 'debugpy-run'
module = name.replace('-', '_')
here = Path(__file__).resolve().parent

setup(
    name=name,
    version='1.6',
    description='Finds and runs debugpy for VS Code "remote attach" '
            'command line debugging.',
    long_description=here.joinpath('README.md').read_text(),
    long_description_content_type='text/markdown',
    url=f'https://github.com/bulletmark/{name}',
    author='Mark Blakeney',
    author_email='mark.blakeney@bullet-systems.net',
    keywords='debugpy vscode code ptvsd',
    license='GPLv3',
    py_modules=[module],
    python_requires='>=3.6',
    install_requires=['packaging'],
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    data_files=[
        (f'share/{name}', ['README.md']),
    ],
    entry_points={
        'console_scripts': [f'{name}={module}:main'],
    },
)
