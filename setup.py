import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

requirements = [
    n.strip() for n in read('requirements.txt').split('\n') if n.strip()
]
print(requirements)

setup(
    name = "markdown-live",
    version = "0.0.2",
    author = "Rory Geoghegan",
    author_email = "r.geoghegan@gmail.com",
    description = ("Serve your markdown files from an http server to see "
        "them render as you edit."),

    packages=['markdown_live'],
    install_requires = requirements,
    package_data = {'': ['*.css', '*.ico']},
    include_package_data = True,
    entry_points={
        'console_scripts': [
            'markdown_live = markdown_live:run',
        ],
    },
    
    license = "BSD",
    keywords = "markdown",
    url = "https://github.com/rgeoghegan/markdown-live",
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
