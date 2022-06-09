import mimetypes
import os
import pathlib

def is_below_directory(path: str, directory_path: str):
    try:
        return pathlib.Path(path).is_relative_to(directory_path)
    except ValueError:
        return False

def concat_paths(path1: str, path2: str):
    return os.path.join(path1, path2)

def list_directory_content(directory_path: str):
    return os.listdir(directory_path)

def does_directory_contain(directory_path: str, filename: str):
    path = os.path.join(directory_path, filename)
    return os.path.isfile(path) or os.path.isdir(path)

def is_file(path: str):
    return os.path.isfile(path)

def is_directory(path: str):
    return os.path.isdir(path)

def get_file_contents(path):
    return open(path, 'rb'), os.stat(path)[6]

def get_file_mimetype(path):
    return mimetypes.guess_type(path)[1]
