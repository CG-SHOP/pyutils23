import os
import zipfile
import typing

from .instance_file_database import InstanceFileDatabase
from .instance_zip_database import InstanceZipDatabase


class InstanceDatabase:
    """
    This class allows to easily read instances from a folder/zipfile if the instance files
    follow the naming convention 'instance-name.instance.json'. It allows subfolder
    but no symbolic links.
    """

    def __init__(self, path: str, enable_cache: bool = False):
        """
        Create an InstanceDatabase that searches in a specified folder/zipfile for instances.
        :param path: Path to the folder/zipfile that contains the instance files (e.g. the folder
                        that contains the extracted zips). The instance files can be
                        in subfolders but have the names have to be NAME.instance.json.
        :param enable_cache: Should the loaded instances be cached? This can take quite
                        a lot of memory
        """
        self._inner_database = self._guess_database_class(path, enable_cache)

    def _guess_database_class(self, path: str, enable_cache):
        """
        Guess if the path contains a zipfile or a folder that could contain the database
        :param path: Path to the folder/zipfile
        :param enable_cache: Cache instances or read from file/zip
        :return: Guessed database object
        """
        if os.path.isdir(path):
            return InstanceFileDatabase(path, enable_cache=enable_cache)
        elif os.path.isfile(path):
            if zipfile.is_zipfile(path):
                return InstanceZipDatabase(path, enable_cache=enable_cache)
            else:
                raise FileNotFoundError(f"{path} is neither a directory or a zipfile.")
        raise FileNotFoundError(f"{path} not found")

    def __iter__(self) -> typing.Dict:
        """
        Iterate over all instances in database.
        :return: Instance objects
        """
        yield from self._inner_database

    def __getitem__(self, name: str) -> typing.Dict:
        """
        Returns the instance of a specific name or throws an KeyError.
        :param name: Name of the instance.
        :return: Instance object
        """
        if "/" in name:
            name = name.split("/")[-1]
        extension = ".instance"
        if len(name) > len(extension) and name[-len(extension) :] == extension:
            name = name[: -len(extension)]
        return self._inner_database[name]
