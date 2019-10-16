class LibreOfficeError(Exception):
    def __init__(self, output):
        self.output = output
