#!/usr/bin/env python

import sys
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if not hasattr(sys, "hexversion") or sys.hexversion < 0x02060000:
    raise Error("Python 2.6 or newer is required")

setup(
   name = "MyPy",
   author = "Nathan Li",
   description = "MySQL Connector in Pure Python"
)
