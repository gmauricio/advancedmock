#! /usr/bin/env python
import os
from setuptools import setup

# Copyright (C) 2013 German Mauricio Munoz
# E-mail: mauricio AT mapalesoftware DOT com

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = 'advancedmock',
    version = '0.0.1',
    py_modules=['advancedmock'],

    #TODO metadata for upload to PyPI
    author = 'German Mauricio Munoz',
    author_email = 'mauricio@mapalesoftware.com',
    description = 'An extension for the mock library',
    long_description = read('README'),
)
