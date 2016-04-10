#!/usr/bin/env bash

# Simple shell script to remember the right order of commands to use with
# setup.py to update the package on pypi.
python setup.py sdist register upload
