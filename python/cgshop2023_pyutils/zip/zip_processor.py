"""
This file contains the ZipSolutionIterator which can read a zip and return all solutions
in it. It should be reasonably robust and have some basic security features.
"""
import json
import typing
from typing import BinaryIO, Union, Iterator
from os import PathLike
from zipfile import ZipFile, BadZipFile
from json import JSONDecodeError

import chardet

from ..io import parse_solution, NoSolution, BadSolutionFile
from .zip_reader_errors import (
    BadZipChecker,
    NoSolutionsError,
    InvalidEncodingError,
    InvalidJSONError,
    InvalidZipError,
)


class ZipSolutionIterator:
    """
    Iterates over all solutions in a zip file.
    First initialize the class, then use call.
    e.g.,
    ```
    zsi = ZipSolutionIterator()
    for solution in zsi("./myzip.zip"):
        print(solution.instance_name)
    ```
    """

    def __init__(
        self,
        file_size_limit: int = 250 * 1_000_000,
        zip_size_limit: int = 2000 * 1_000_000,
        solution_extensions=("json", "solution"),
    ):
        """
        Set the parameters in the constructor. Use the __call__ to actually iterate
        a zip file.
        :param file_size_limit: Limit the size of a single file within the zip.
        :param zip_size_limit: Limit the overall decompressed size of the zip.
        :param solution_extensions: What file extensions should be checked?
        """
        self._checker = BadZipChecker(
            file_size_limit=file_size_limit, zip_size_limit=zip_size_limit
        )
        self._solution_extensions = solution_extensions

    def _check_if_bad_zip(self, zipfile):
        self._checker(zipfile)

    def _is_hidden_folder_name(self, name):
        if len(name) > 1 and name[0] == ".":  # classic hidden unix files.
            return True
        if len(name) > 1 and name[:2] == "__":  # OS X does that.
            return True
        return False

    def _is_solution_filename(self, name):
        extension = name.split(".")[-1].lower()
        # check extension
        if extension not in self._solution_extensions:
            return False
        # check for hidden file/directory
        if any(self._is_hidden_folder_name(s) for s in name.split("/")):
            return False
        # any more checks?
        return True

    def _iterate_solution_filenames(self, zip_file):
        had_filename = False
        for filename in zip_file.namelist():
            if self._is_solution_filename(filename):
                had_filename = True
                yield filename
        if not had_filename:
            raise NoSolutionsError()

    def _robust_parse_json_from_bytes(self, bytes):
        """
        First tries to encode via 'UTF-8', otherwise it uses chardet.
        :param bytes: bytes of solution file
        :return: json
        """
        try:
            return json.loads(str(bytes, encoding="utf-8", errors="strict"))
        except UnicodeDecodeError:
            encoding = chardet.detect(bytes)
            return json.loads(
                str(bytes, encoding=encoding["encoding"], errors="strict")
            )

    def _parse_file(self, solution_file, file_name, info):
        # read no more than the claimed file_size bytes (which we checked for limit violations)
        b = solution_file.read(info.file_size)
        try:
            return self._robust_parse_json_from_bytes(b)
        except UnicodeDecodeError as ude:
            raise InvalidEncodingError(file_name) from ude
        except JSONDecodeError as e:
            raise InvalidJSONError(file_name, f"{e}") from e
        except RecursionError as re:
            raise InvalidJSONError(file_name, "Nesting level is too deep") from re

    def _iterate_solution_jsons(self, zip_file):
        for file_name in self._iterate_solution_filenames(zip_file):
            with zip_file.open(file_name, "r") as sol_file:
                info = zip_file.getinfo(file_name)
                yield file_name, self._parse_file(sol_file, file_name, info)

    def __call__(
        self, path_or_file: Union[BinaryIO, str, PathLike]
    ) -> Iterator[typing.Dict]:
        """
        Iterates over all solutions in the zip.
        :param path_or_file: Zip or file
        :return:
        """
        found_an_instance =False
        try:
            with ZipFile(path_or_file) as zip_file:
                self._check_if_bad_zip(zip_file)
                for file_name, solution_json in self._iterate_solution_jsons(zip_file):
                    meta = {
                        "zip_info": {
                            "zip_file": zip_file.filename,
                            "file_in_zip": file_name,
                        }
                    }
                    try:
                        solution = parse_solution(solution_json)
                        solution["meta"] = meta
                        yield solution
                        found_an_instance = True
                    except NoSolution:
                        print(f"Skipping {file_name}, as it is not a solution file.")
        except BadZipFile as e:
            raise InvalidZipError(f"{e}") from e
        except BadSolutionFile as e:
            raise InvalidZipError(f"Aborted parsing zip due to bad file: {e}") from e
        if not found_an_instance:
            raise NoSolutionsError()
