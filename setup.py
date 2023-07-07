#!/usr/bin/env python

from distutils.core import setup

setup(name='FallkapselServer',
      version='0.1',
      description='Server and GUI to connect to a microcontroller and display its acceleration.',
      author='Leon Brenig',
      author_email='Leon.Brenig@dlr.de',
      url='https://github.com/DLRSchoolLabBremen/Fallkapsel-Schwerelosigkeit',
      packages=['distutils', 'distutils.command'],
      license='MIT',    
     )