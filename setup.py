#!/usr/bin/env python

from distutils.core import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(name='FallkapselServer',
      version='0.1',
      description='Server and GUI to connect to a microcontroller and display its acceleration.',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='Leon Brenig',
      author_email='Leon.Brenig@dlr.de',
      url='https://github.com/DLRSchoolLabBremen/Fallkapsel-Schwerelosigkeit',
      packages=['Fallkapsel_Server'],
      install_requires=[
        'pybluez2',
        'matplotlib',
        'customtkinter',
      ],
      entry_points={
        'console_scripts': [
            'fallkapsel_server = Fallkapsel_Server.__main__:main',
        ],
      },
      license='MIT',    
     )