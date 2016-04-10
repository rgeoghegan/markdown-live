import argparse
from contextlib import closing
from http.server import BaseHTTPRequestHandler, HTTPServer
import markdown
import os
import shutil

def parse_args():
    parser = argparse.ArgumentParser(
        description="Render markdown files and serve them with an http server."
    )
    parser.add_argument('-p', '--port', default=8000, type=int)
    return parser.parse_args()

class MarkdownHTTPRequestHandler(BaseHTTPRequestHandler):
    content_type = 'text/html'
    stylesheet_content_type = 'text/css'
    encoding = 'utf8'
    stylesheet = 'markdown.css'

    def do_GET(self):
        path = self.path[1:]

        if path == 'markdown.css':
            return self.stylesheet_response()

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
        rel_path = os.path.join(
            os.path.dirname(__file__),
            self.stylesheet
        )
        with open(rel_path, 'rb') as f:
            self.send_response(200)
            self.send_header("Content-type", self.stylesheet_content_type)
            fs = os.fstat(f.fileno())
            self.send_header("Content-Length", str(fs[6]))
            self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
            shutil.copyfileobj(f, self.wfile)

    def serve_file(self, filename):
        rel_path = os.path.join(
            os.path.dirname(__file__),
            filename
        )
        with open(rel_path, 'rb') as f:
            self.send_response(200)
            self.send_header("Content-type", self.stylesheet_content_type)
            fs = os.fstat(f.fileno())
            self.send_header("Content-Length", str(fs[6]))
            self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
            shutil.copyfileobj(f, self.wfile)


def run(port):
    server_address = ('', port)
    httpd = HTTPServer(server_address, MarkdownHTTPRequestHandler)
    print("Serving from http://localhost:{}/".format(port))
    httpd.serve_forever()

if __name__ == '__main__':
    args = parse_args()
    run(args.port)
