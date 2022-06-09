import urllib
import os

def translate_to_os_path(url_path: str):
    url_path = remove_request_parameters(url_path)
    url_path = remove_trailing_slash_and_whitespaces(url_path)
    try:
        url_path = urllib.parse.unquote(url_path, errors='surrogatepass')
    except UnicodeDecodeError:
        url_path = urllib.parse.unquote(url_path)
    os_path = os.path.normpath(url_path)
    return remove_leading_separator(os_path)
    
def remove_leading_separator(os_path: str):
    return os_path.lstrip("{} .".format(os.path.sep))

def remove_trailing_slash_and_whitespaces(url_path: str):
    return url_path.rstrip(" /")

def remove_request_parameters(url_path: str):
    url_path = url_path.split('?',1)[0]
    url_path = url_path.split('#',1)[0]
    return url_path