from config.config import ConfigServer
from http.server import BaseHTTPRequestHandler, HTTPServer
from logging import info
import logging


class Server(BaseHTTPRequestHandler):

    def do_GET(self):
        config = ConfigServer()
        self.web_directory = config.web_directory
        self.html_files = config.start_html
        try:
            content = open(self.web_directory + self.html_files[0]).read()
            self.send_response(200)
        except FileNotFoundError:
            content = "<h1>404</h1>"
            self.send_response(404)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(content, 'utf-8'))


def run_server():
    config = ConfigServer()
    webServer = HTTPServer((config.hostname, config.port), Server)
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
    info("Server started http://%s:%s" % (config.hostname, config.port))
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass
    webServer.server_close()
    info("Server stopped http://%s:%s " % (config.hostname, config.port))
