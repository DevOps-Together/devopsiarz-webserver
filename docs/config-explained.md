This is not correct JSON file because of comments
```json
{
    // port to listen on
    "port": 80,
    // address to listen on
    "address": "0.0.0.0",
    // file to which logs will be appended
    "log_file": "log/httpy.log"
    // format string for logs, see docs.python.org/3/library/logging.html#logging.basicConfig for list of format strings
    "log_format": ""
    // path to html documents catalog
    "web_directory": "./www",
    // names of files that will be treated as index. If file is not found, next pattern is checked.
    // patterns starting with regexp:: are interpreted as python regular expressions. 
    // I do not guarantee that regexp pattern will always result in server serving the same file if there are multiple files.
    "index_files": [
        "index.html",
        "index",
        "*.html"
    ],
    // none or http-basic
    "security": "none",
    // if http-basic is set
    // "username": "username",
    // "password": "password"
    // if index is not found, should server display list of files instead?
    "list_files": true
}
```