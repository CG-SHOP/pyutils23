import os
import abc
import typing

from ..io import read_instance


class InstanceBaseDatabase(abc.ABC):
    """
    This class is only an ABC for lower level access classes.
    """

    def __init__(self, path: str, enable_cache: bool = False):
        """
        Create an InstanceDatabase that searches in a specified folder for instances.
        :param path: Path to the folder that contains the instance files (e.g. the folder
                        that contains the extracted zips). The instance files can be
                        in subfolders but have the names have to be NAME.instance.json.
        :param enable_cache: Should the loaded instances be cached? This can take quite
                        a lot of memory
        """
        self._path = path
        self._is_cache_enabled = enable_cache
        self._cache = {}
        if not os.path.exists(path):
            raise ValueError(f"The folder {os.path.abspath(path)} does not exist")

    def _filename_fits_name(self, filename, name):
        if not self._filename_fits_instance_convention(filename):
            return False
        split = filename.split(".")
        return split[0] == name

    def _filename_fits_instance_convention(self, filename):
        split = filename.split(".")
        if len(split) != 3:
            return False
        return split[1] == "instance" and split[2] == "json"

    def read(self, f):
        return read_instance(f)

    def _cache_and_return(self, instance):
        if self._is_cache_enabled:
            self._cache[instance.name] = instance
        return instance

    def _is_hidden_folder_name(self, name):
        if name.replace(".", "") and name[0] == ".":  # classic hidden unix files.
            return True
        if len(name) > 1 and name[:2] == "__":  # OS X does that.
            return True
        return False

    def _is_hidden_folder(self, path):
        return any(self._is_hidden_folder_name(folder) for folder in path.split("/"))

    def _extract_instance_name_from_path(self, path):
        filename = os.path.split(path)[1]
        return filename.split(".")[0]

    @abc.abstractmethod
    def __iter__(self) -> typing.Dict:
        """
        Iterate over all instances in database.
        :return: Instance objects
        """
        pass

    @abc.abstractmethod
    def __getitem__(self, name: str) -> typing.Dict:
        """
        Returns the instance of a specific name or throws an KeyError.
        :param name: Name of the instance.
        :return: Instance object
        """
        pass
