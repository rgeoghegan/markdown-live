Markdown-live
=============

Simply run a web server from the command line that will render your
markdown files as html live.

Installation
------------

`pip install markdown-live` should work. It's compatible with python 2.7, and python 3.4+.

Usage
-----

Installing markdown-live will install the `markdown_live` executable, which can be used as such:

    usage: markdown_live [-h] [-p PORT] [-v] [LOCATION]

    Render markdown files and serve them with an http server.

    optional arguments:
      -h, --help            show this help message and exit
      -p PORT, --port PORT  Serve on this port instead of the default (port 8000)
      -v, --version         Just print out the version number
      LOCATION              either a markdown file to just render that
                            file, or a directory to server files from that
                            directory

Pypi
----

The package is currenly available on pypi [here](https://pypi.python.org/pypi/markdown-live).

