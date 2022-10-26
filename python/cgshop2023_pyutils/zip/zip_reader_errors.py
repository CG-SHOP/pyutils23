from os import path
from zipfile import ZipFile


class ZipReaderError(Exception):
    pass


class InvalidFileName(ZipReaderError):
    def __init__(self, file_name):
        self.file_name = file_name
        super().__init__(
            f"The ZIP archive contains the invalid file name: '{file_name}'!"
        )


class FileTooLargeError(ZipReaderError):
    def __init__(self, file_name, file_size, file_size_limit):
        self.file_name = file_name
        self.file_size = file_size
        self.file_size_limit = file_size_limit
        super().__init__(
            f"The ZIP archive contains the file '{self.file_name}' with a size "
            f"of {self.file_size / 1_000_000} MB (only {self.file_size_limit / 1_000_000} MB allowed)!"
        )


class ZipTooLargeError(ZipReaderError):
    def __init__(self, decompressed_size, decompressed_size_limit):
        self.decompressed_size = decompressed_size
        self.decompressed_size_limit = decompressed_size_limit
        super().__init__(
            f"The ZIP archive has a total decompressed size of {self.decompressed_size/1_000_000} MB "
            f"(only {self.decompressed_size_limit / 1_000_000} MB allowed)!"
        )


class NoSolutionsError(ZipReaderError):
    def __init__(self):
        super().__init__("The ZIP archive does not appear to contain any solution!")


class InvalidJSONError(ZipReaderError):
    def __init__(self, file_name, message):
        self.file_name = file_name
        super().__init__(
            f"The ZIP archive contains the file '{file_name}'"
            f" which is not a valid JSON-encoded file: {message}!"
        )


class InvalidEncodingError(ZipReaderError):
    def __init__(self, file_name):
        self.file_name = file_name
        super().__init__(
            f"File '{file_name}' in the ZIP uses an unrecognized character encoding; "
            f"please use UTF-8 instead."
        )


class InvalidZipError(ZipReaderError):
    def __init__(self, message):
        super().__init__(
            f"The ZIP archive is corrupted and could not be decompressed: {message}!"
        )


class BadZipChecker:
    """
    Check if zip is bad/malicious/corrupted.
    """

    def __init__(self, file_size_limit: int, zip_size_limit: int):
        self.file_size_limit = file_size_limit
        self.zip_size_limit = zip_size_limit

    def _check_zip_size(self, zip_file):
        zip_decompressed_size = sum(zi.file_size for zi in zip_file.infolist())
        if zip_decompressed_size > self.zip_size_limit:
            raise ZipTooLargeError(zip_decompressed_size, self.zip_size_limit)

    def _is_file_name_okay(self, name):
        return name[0] != "/" and not path.isabs(name) and ".." not in name

    def _check_file_names(self, f: ZipFile):
        for n in f.namelist():
            if not self._is_file_name_okay(n):
                raise InvalidFileName(n)

    def _check_decompressed_sizes(self, f: ZipFile):
        for info in f.filelist:
            if info.file_size > self.file_size_limit:
                raise FileTooLargeError(
                    info.filename, info.file_size, self.file_size_limit
                )

    def _check_crc(self, zip_file):
        bad_filename = zip_file.testzip()
        if bad_filename is not None:
            raise InvalidZipError(f"{bad_filename} is corrupted (CRC checksum error)!")

    def __call__(self, zip_file):
        self._check_file_names(zip_file)
        self._check_decompressed_sizes(zip_file)
        self._check_zip_size(zip_file)
        self._check_crc(zip_file)
