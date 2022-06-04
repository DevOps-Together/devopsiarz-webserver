import http
from model.config import Configuration

class Server:
    _config: Configuration

    def __init__(self, config: Configuration):
        self._config = config
    
    def start():
        # TODO: loop listening on port from configuration, starting a new thread for each incoming connection (use some kind of thread pool with limit on maximal number of threads)
        # TODO: threads that establish connection, retrive and return resource or appropriate error
        # TODO: handle http basic auth for incoming connections
        # TODO: cleanup of all threads and resources on exit
        return