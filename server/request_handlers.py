import base64
import shutil
import server.url_path_helper as uph
import server.files.www_files_helper as wfh
from server.files.file_response import FileResponse
from server.files.filesystem_errors import FileReadError, PathOutOfScopeError, FileNotFoundError
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
        os_path = uph.translate_to_os_path(self.path)
        try:
            file = wfh.get_file_descriptor_for_path(os_path, self._config)
        except PathOutOfScopeError:
            return self.respond_with_not_found()
        except FileNotFoundError:
            return self.respond_with_not_found()
        except FileReadError:
            return self.respond_with_internal_error()
        self.respond_with_file(file)
        
    def respond_with_file(self, file: FileResponse):
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", file.file_mimetype)
        self.send_header("Content-Length", str(file.file_length))
        self.end_headers()
        shutil.copyfileobj(file.contents, self.wfile)

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

