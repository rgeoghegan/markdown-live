#!/usr/bin/env bash

set -e

# Simple shell script to remember the right order of commands to use with
# setup.py to build the wheel/src dist.
python setup.py sdist bdist_wheel
# twine to upload to pypi
twine upload dist/*
