class FileNotFoundError(Exception):
    path: str

class PathOutOfScopeError(Exception):
    path: str

class FileReadError(Exception):
    path: str