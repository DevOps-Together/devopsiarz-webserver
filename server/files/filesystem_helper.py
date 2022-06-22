import mimetypes
import os
import pathlib
import re

REGEX_FLAG="regexp::"

def is_below_directory(path: str, directory_path: str):
    try:
        return pathlib.Path(path).is_relative_to(directory_path)
    except ValueError:
        return False

def concat_paths(path1: str, path2: str):
    return os.path.join(path1, path2)

def list_directory_content(directory_path: str):
    return os.listdir(directory_path)

def any_match(directory_path: str, filename_regex: str):
    filenames_list = list_directory_content(directory_path)
    for filename in filenames_list:
        if re.fullmatch(filename_regex, filename) != None:
            path = os.path.join(directory_path, filename)
            if os.path.isfile(path):
                return path
    return False

def does_directory_contain(directory_path: str, filename: str):
    path = os.path.join(directory_path, filename)
    if filename.startswith(REGEX_FLAG):
        return any_match(directory_path, filename.removeprefix(REGEX_FLAG))
    elif os.path.isfile(path) or os.path.isdir(path):
            return path
    return False

def is_file(path: str):
    return os.path.isfile(path)

def is_directory(path: str):
    return os.path.isdir(path)

def get_file_contents(path):
    return open(path, 'rb'), os.stat(path)[6]

def get_file_mimetype(path):
    return mimetypes.guess_type(path)[0]
