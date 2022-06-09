from io import BytesIO

class FileResponse():
    contents: BytesIO
    file_length: int
    file_path: str
    file_mimetype: str

    def __init__(self, contents: BytesIO, mimetype: str, file_path: str, file_length: int):
        self.contents = contents
        self.file_mimetype = mimetype
        self.file_path = file_path
        self.file_length = file_length