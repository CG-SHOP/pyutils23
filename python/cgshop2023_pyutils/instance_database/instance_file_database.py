import os
import typing

from .instance_base_database import InstanceBaseDatabase


class InstanceFileDatabase(InstanceBaseDatabase):
    """
    This class allows to easily read instances from a folder if the instance files
    follow the naming convention 'instance-name.instance.json'. It allows subfolder
    but no symbolic links.
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
        super().__init__(path, enable_cache)

    def _iterate_paths(self):
        for root, dirs, files in os.walk(self._path, topdown=True):
            dirs[:] = [d for d in dirs if not self._is_hidden_folder(d)]
            for file in files:
                if self._filename_fits_instance_convention(
                    file
                ) and not self._is_hidden_folder_name(file):
                    path = os.path.join(root, file)
                    yield path

    def _find_path(self, name):
        for instance_path in self._iterate_paths():
            if self._filename_fits_name(os.path.split(instance_path)[-1], name):
                return instance_path
        raise KeyError(f"Did not find a suitable file for {name} in {self._path}")

    def _extract_instance_name_from_path(self, path):
        filename = os.path.split(path)[1]
        return filename.split(".")[0]

    def __iter__(self) -> typing.Dict:
        """
        Iterate over all instance files.
        :return: Instance objects
        """
        for instance_path in self._iterate_paths():
            instance_name = self._extract_instance_name_from_path(instance_path)
            if instance_name in self._cache:
                yield self._cache[instance_name]
            else:
                yield self._cache_and_return(self.read(instance_path))

    def __getitem__(self, name: str) -> typing.Dict:
        """
        Returns the instance of a specific name or throws an KeyError.
        :param name: Name of the instance.
        :return:
        """
        if name is self._cache:
            return self._cache[name]
        path = self._find_path(name)
        return self._cache_and_return(self.read(path))
