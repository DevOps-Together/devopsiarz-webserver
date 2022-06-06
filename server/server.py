from enum import Enum
from http.server import ThreadingHTTPServer
from logging import error, info
from model.config import Configuration
from server.request_handlers import HttpBasicRequestHandler, InsecureRequestHandler

class Security(Enum):
    HTTP_BASIC = 'http-basic'
    NONE = 'none'

class Server:
    _config: Configuration

    def __init__(self, config: Configuration):
        self._config = config
    
    def start(self):
        server_address = (self._config.address, self._config.port)
        server = None
        if self._config.security == Security.NONE:
            info("Starting server with no security.")
            server = ThreadingHTTPServer(server_address, lambda a, b, webserver: InsecureRequestHandler(a, b, webserver, self._config))
        elif self._config.security == Security.HTTP_BASIC:
            info("Starting server with http basic auth security.")
            server = ThreadingHTTPServer(server_address, lambda a, b, webserver: HttpBasicRequestHandler(a, b, webserver, self._config))
        else:
            error("Unknown security mode: %s. Server is shutting down.".format(self._config.security))
            return
        server.serve_forever()
        info("Server stopped.")
        return