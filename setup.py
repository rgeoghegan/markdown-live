import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "markdown-live",
    version = "0.0.1",
    author = "Rory Geoghegan",
    author_email = "r.geoghegan@gmail.com",
    description = ("Serve your markdown files from an http server to see "
        "them render as you edit."),
    license = "BSD",
    keywords = "markdown",
    #url = "http://packages.python.org/an_example_pypi_project",
    packages=['markdown_live'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
