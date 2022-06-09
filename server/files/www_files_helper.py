from importlib.metadata import files
from io import BytesIO
import os
import sys
import server.files.filesystem_helper as fsh
from server.files.filesystem_errors import FileNotFoundError
from model.config import Configuration
from server.files.file_response import FileResponse
from server.files.filesystem_errors import PathOutOfScopeError


def get_file_descriptor_for_path(os_path: str, config: Configuration) -> FileResponse:
    os_path = fsh.concat_paths(config.web_directory, os_path)
    if fsh.is_below_directory(os_path, config.web_directory):
        if fsh.is_directory(os_path):
            for indexfile in config.index_files:
                if fsh.does_directory_contain(os_path, indexfile):
                    return get_file_response(os.path.join(os_path, indexfile))
            if config.list_files:
                return get_files_list_response(os_path, config)
        elif fsh.is_file(os_path):
            return get_file_response(os_path)
        raise FileNotFoundError()
    else:
        raise PathOutOfScopeError()

def get_file_response(os_path: str) -> FileResponse:
    contents, len = fsh.get_file_contents(os_path)
    mimetype = fsh.get_file_mimetype(os_path)
    if mimetype is None:
        mimetype = "text/html;charset=utf-8"
    return FileResponse(contents, mimetype, os_path, len)

def get_files_list_response(os_path: str, config: Configuration) -> FileResponse:
    files = fsh.list_directory_content(os_path)
    contents = '\n'.join(wrap_files_list_in_html(os_path, files, config)).encode(sys.getfilesystemencoding())
    return FileResponse(BytesIO(contents), "text/html;charset=utf-8", '', len(contents))

def wrap_files_list_in_html(os_path: str, files: list, config: Configuration) -> list:
    body = []
    body.append("<html><body><main><ul>")
    for filename in files:
        filepath = os.path.join(os_path, filename).removeprefix(config.web_directory)
        body.append("<li><a href='{0}'>{1}</a></li>".format( filepath, filename))
    body.append("</ul></main></body></html>")
    return body