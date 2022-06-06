import base64
from distutils.log import info
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from model.config import Configuration


class InsecureRequestHandler(BaseHTTPRequestHandler):
    _config: Configuration

    def __init__(self, request: bytes, client_address: tuple[str, int], server: ThreadingHTTPServer, config: Configuration) -> None:
        super().__init__(request, client_address, server)
        self._config = config

    def do_GET():
        # TODO: File listing
        # TODO: if any file from index list is present, respond with it
        # TODO: otherwise respond with list of files and subfolders
        return


class HttpBasicRequestHandler(BaseHTTPRequestHandler):
    _config: Configuration
    _insecureHandler : InsecureRequestHandler

    def __init__(self, request: bytes, client_address: tuple[str, int], server: ThreadingHTTPServer, config: Configuration) -> None:
        super().__init__(request, client_address, server)
        self._insecureHandler = InsecureRequestHandler(request, client_address, server, config)
        self._config = config

    def do_GET(self):
        info(format("Handling GET request from %s.", self.client_address[1]))
        authorization = self.headers.get('Authorization',  '')
        if(authorization == '' or not authorization.startswith('Basic')):
            info("Authentication type not recognized.")
            self.send_auth_challange_response()
            return
        username, password = base64.b64decode(authorization.replace('Basic','').strip()).decode('utf-8').split(':')
        # TODO random wait between checking username and password to defeat response time-based bruteforcers
        if(self._config.username == username and self._config.password == password):
            info(format("Authentication for user %s correct.", username))
            self._insecureHandler.do_GET()
        else:
            info(format("Authentication for user %s incorrect.", username))
            self.send_auth_challange_response()
        
    def send_auth_challange_response(self):
        info("Sending authentication challange.")
        self.send_response(HTTPStatus.UNAUTHORIZED)
        self.send_header('WWW-Authenticate', 'Basic realm="Access to web directory protected by authorization."')

