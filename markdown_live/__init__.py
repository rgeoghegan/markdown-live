import argparse
from contextlib import closing
import mimetypes
import os
import shutil

try:
    from http.server import BaseHTTPRequestHandler, HTTPServer
except ImportError:
    # Compatible with python 2.7
    from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

import markdown

VERSION = "1.1.0"
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
    parser.add_argument('location', default='.', nargs='?',
                        help='Which directory or file to serve. If you pick '
                            'a file, / on the server will automatically '
                            'point to that file.')
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

        if not os.path.isdir(self.server.root_location):
            return self.markdown_file(self.server.root_location)

        full_path = os.path.join(self.server.root_location, path)

        if not os.path.exists(full_path):
            self.send_error(404, "File not found")

        if os.path.isdir(full_path):
            content = []
            for entry in os.listdir(full_path):
                content.append(
                    '<div><a href="{}">{}</a>'.format(
                        os.path.join(path, entry),
                        entry
                    )
                )
            return self.make_html(content)

        # Finally, try parsing the file as markdown
        return self.markdown_file(full_path)

    def make_html(self, content, last_modified=None):
        full_page = [
            "<!doctype html>",
            "<html><head>",
            self.header_content(),
            "</head>",
            "<body>",
        ]
        full_page.extend(content)
        full_page.append("</body></html>")

        text = "\n".join(full_page)
        self.send_response(200)
        self.send_header("Content-type", self.content_type)

        if last_modified is not None:
            self.send_header("Last-Modified",
                             self.date_time_string(last_modified))

        self.send_header("Content-Length", len(text))
        self.end_headers()
        self.wfile.write(text.encode(self.encoding))

    def markdown_file(self, path):
        with open(path) as f:
            fs = os.fstat(f.fileno())
            return self.make_html(
                [markdown.markdown(f.read())],
                last_modified=fs.st_mtime
            )

    def header_content(self):
        return '<link href="{}" rel="stylesheet"></link>'.format(
            '/' + self.stylesheet)

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
            self.send_header("Last-Modified",
                             self.date_time_string(fs.st_mtime))
            self.end_headers()

            shutil.copyfileobj(f, self.wfile)


class MarkdownHTTPServer(HTTPServer):
    """
    Hacky way to pass the location from run_server() to the Request Handler
    object.
    """
    handler_class = MarkdownHTTPRequestHandler

    def __init__(self, server_address, location):
        self.root_location = location

        try:
            super().__init__(
                server_address, self.handler_class
            )
        except TypeError:
            # Python 2.7 will cause a type error, and in addition
            # HTTPServer is an old-school class object, so use the old
            # inheritance way here.
            HTTPServer.__init__(self, server_address, self.handler_class)


def run_server(port, location):
    server_address = ('', port)
    httpd = MarkdownHTTPServer(server_address, location)
    print("Serving from http://localhost:{}/".format(port))
    httpd.serve_forever()

def run():
    args = parse_args()
    if args.version:
        print("Version {}".format(VERSION))
    else:
        run_server(args.port, args.location)
