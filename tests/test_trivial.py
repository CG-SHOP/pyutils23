import pytest
import os

from cgshop2023_pyutils import InstanceDatabase
from cgshop2023_pyutils import verify as pyverify

from cgshop2023_pyutils.zip import ZipSolutionIterator

def test_iterator():
    path = os.path.join(os.path.dirname(__file__), "./instances.zip")
    if not os.path.exists(path):
        return
    idb = InstanceDatabase(path)
    path = os.path.join(os.path.dirname(__file__), "./trivial.zip")
    if not os.path.exists(path):
        return
    isi = ZipSolutionIterator()
    for solution in isi(path):
        instance = idb[solution["instance"]]
        print(solution["instance"])
        assert pyverify(instance=instance, solution=solution) == ""
    