import os

from cgshop2023_pyutils.zip import ZipSolutionIterator


def test_iterator():
    path = os.path.join(os.path.dirname(__file__), "./correct_test_solutions.zip")
    if not os.path.exists(path):
        return
    isi = ZipSolutionIterator()
    for solution in isi(path):
        assert "." not in solution["instance"]
        print(solution["instance"])
