import argparse
from contextlib import closing
from http.server import BaseHTTPRequestHandler, HTTPServer
import mimetypes
import os
import shutil

import markdown

VERSION = "0.0.2"
DEFAULT_PORT = 8000

def parse_args():
    parser = argparse.ArgumentParser(
        description="Render markdown files and serve them with an http server."
    )
    parser.add_argument(
        '-p', '--port', default=DEFAULT_PORT, type=int,
        help='Serve on this port instead of the default '
            '(port {})'.format(DEFAULT_PORT)
    )
    parser.add_argument('-v', '--version', action='store_true',
                        help='Just print out the version number')
    return parser.parse_args()

class MarkdownHTTPRequestHandler(BaseHTTPRequestHandler):
    content_type = 'text/html'
    stylesheet_content_type = 'text/css'
    encoding = 'utf8'
    stylesheet = 'markdown.css'
    favicon = 'favicon.ico'

    def do_GET(self):
        path = self.path[1:]

        if path == 'markdown.css':
            return self.stylesheet_response()
        elif path == 'favicon.ico':
            return self.favicon_response()

        try:
            f = open(path, 'r')
        except OSError as o:
            print(o)
            self.send_error(404, "File not found")
            return None

        with closing(f):
            content = [
                "<!doctype html>",
                "<html><head>",
                self.header_content(),
                "</head>",
                "<body>",
                markdown.markdown(f.read()),
                "</body></html>",
            ]
            content = "\n".join(content)

            self.send_response(200)
            self.send_header("Content-type", self.content_type)
            fs = os.fstat(f.fileno())
            self.send_header("Content-Length", len(content))
            self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
            self.end_headers()

            self.wfile.write(content.encode(self.encoding))

    def header_content(self):
        return '<link href="{}" rel="stylesheet"></link>'.format('/' + self.stylesheet)

    def stylesheet_response(self):
        return self.serve_file(self.stylesheet, mimetypes.types_map['.css'])

    def favicon_response(self):
        return self.serve_file(self.favicon, mimetypes.types_map['.ico'])

    def serve_file(self, filename, content_type):
        """
        Returns a 200 response with the content of the filename (which is
        relative to this file), and the given content type.
        """
        rel_path = os.path.join(os.path.dirname(__file__), filename)

        with open(rel_path, 'rb') as f:
            self.send_response(200)
            self.send_header("Content-type", content_type)
            fs = os.fstat(f.fileno())
            self.send_header("Content-Length", str(fs[6]))
            self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
            self.end_headers()

            shutil.copyfileobj(f, self.wfile)

def run_server(port):
    server_address = ('', port)
    httpd = HTTPServer(server_address, MarkdownHTTPRequestHandler)
    print("Serving from http://localhost:{}/".format(port))
    httpd.serve_forever()

def run():
    args = parse_args()
    if args.version:
        print("Version {}".format(VERSION))
    else:
        run_server(args.port)
