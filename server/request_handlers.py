import base64
import io
import os
import pathlib
import shutil
import sys
import urllib
from distutils.log import info
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from model.config import Configuration


class InsecureRequestHandler(BaseHTTPRequestHandler):
    _config: Configuration

    def __init__(self, request: bytes, client_address: tuple[str, int], server: ThreadingHTTPServer, config: Configuration) -> None:
        self._config = config
        super().__init__(request, client_address, server)

    def do_GET(self):
        path = self.translate_path(self.path)
        if path != '' and not pathlib.Path(path).is_relative_to(self._config.web_directory):
            self.respond_with_not_found()
            return None
        for index in self._config.index_files:
                index = os.path.join(path, index)
                if os.path.exists(index):
                    path = index
                    break
        else:
            return self.list_files(path)
        return self.respond_with_file(path)

    def respond_with_file(self, path):
        try:
            file = open(path, 'rb')
        except OSError:
            self.respond_with_internal_error()
            return None
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type","text/html;charset=utf-8")
        self.send_header("Content-Length", str(os.stat(path)[6]))
        self.end_headers()
        shutil.copyfileobj(file, self.wfile)

    def list_files(self, path):
        try:
            files_in_directory = os.listdir(path)
        except OSError:
            self.respond_with_not_found()
            return None
        response_body = []
        response_body.append("<html><body><main><ul>")
        for filename in files_in_directory:
            if filename in (os.curdir, os.pardir):
                continue
            response_body.append("<li><a href='{1}'>{2}</a></li>".format(os.path.join(self.path, filename), filename))
        response_body.append("</ul></main></body></html>")
        encoded = '\n'.join(response_body).encode(sys.getfilesystemencoding())
        f = io.BytesIO()
        f.write(encoded)
        f.seek(0)
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-type", "text/html; charset=%s".format(sys.getfilesystemencoding()))
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        return f

    def translate_path(self, path: str):
        path = self.remove_path_parameters(path)
        path = path.rstrip(" /")
        try:
            path = urllib.parse.unquote(path, errors='surrogatepass')
        except UnicodeDecodeError:
            path = urllib.parse.unquote(path)
        path = os.path.normpath(path)
        words = path.split('/')
        words = filter(None, words)
        path = self._config.web_directory
        for word in words:
            if os.path.dirname(word) or word in (os.curdir, os.pardir):
                continue
            path = os.path.join(path, word)
        return path

    def remove_path_parameters(self,path: str):
        path = path.split('?',1)[0]
        path = path.split('#',1)[0]
        return path

    def respond_with_not_found(self):
        self.send_error(HTTPStatus.NOT_FOUND)
        return None

    def respond_with_internal_error(self):
        self.send_error(HTTPStatus.INTERNAL_SERVER_ERROR)
        return None


class HttpBasicRequestHandler(BaseHTTPRequestHandler):
    _config: Configuration
    _insecureHandler : InsecureRequestHandler

    def __init__(self, request: bytes, client_address: tuple[str, int], server: ThreadingHTTPServer, config: Configuration) -> None:
        self._insecureHandler = InsecureRequestHandler(request, client_address, server, config)
        self._config = config
        super().__init__(request, client_address, server)

    def do_GET(self):
        info(format("Handling GET request from %s.", self.client_address[1]))
        authorization = self.headers.get('Authorization',  '')
        if authorization == '' or not authorization.startswith('Basic'):
            info("Authentication type not recognized.")
            self.send_auth_challange_response()
            return None
        username, password = base64.b64decode(authorization.replace('Basic','').strip()).decode('utf-8').split(':')
        # TODO random wait between checking username and password to defeat response time-based bruteforcers
        if self._config.username == username and self._config.password == password:
            info(format("Authentication for user %s correct.", username))
            self._insecureHandler.do_GET()
        else:
            info(format("Authentication for user %s incorrect.", username))
            self.send_auth_challange_response()
        return None
        
    def send_auth_challange_response(self):
        info("Sending authentication challange.")
        self.send_response(HTTPStatus.UNAUTHORIZED)
        self.send_header('WWW-Authenticate', 'Basic realm="Access to web directory protected by authorization."')
        return None

