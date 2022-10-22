from cgshop2023_pyutils.core import (
    FieldNumber,
    Point,
    Polygon,
    PolygonWithHoles,
    verify,
)
from cgshop2023_pyutils.io.read import read_instance, read_solution
from cgshop2023_pyutils.verifier import verify as verify_
from cgshop2023_pyutils import InstanceDatabase
from cgshop2023_pyutils import verify as pyverify
import zipfile

idb = InstanceDatabase("./example_instances.zip")
sol_zip = zipfile.ZipFile("./correct_test_solutions.zip")
filelist = list(sol_zip.filelist)
solution_path = (
    "convex-cover-main-solutions/solutions/prio dfs_cheese10008.instance_sol.json"
)
solution_path = (
    "convex-cover-main-solutions/solutions/multitry_cheese4023.instance_sol.json"
)
solution = read_solution(sol_zip.open(solution_path))
instance = idb[solution["instance"]]
msg = pyverify(instance, solution)
assert msg == ""
