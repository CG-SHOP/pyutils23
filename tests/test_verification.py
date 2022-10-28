import os.path
import random
import zipfile

from cgshop2023_pyutils.core import (
    FieldNumber,
    Point,
    Polygon,
    PolygonWithHoles,
    verify,
)
from cgshop2023_pyutils.io.read import read_solution
from cgshop2023_pyutils.verifier import verify as verify_
from cgshop2023_pyutils import InstanceDatabase
from cgshop2023_pyutils import verify as pyverify


def test_verify():
    points = [
        Point(FieldNumber(x), FieldNumber(y))
        for x, y in ((0, 0), (1, 0), (1, 1), (0, 1))
    ]
    polygon = Polygon(points)
    poly_with_holes = PolygonWithHoles(polygon, [])
    assert verify(poly_with_holes, [polygon]) == ""


def test_verify_fail():
    points = [
        Point(FieldNumber(x), FieldNumber(y))
        for x, y in ((0, 0), (1, 0), (1, 1), (0, 1))
    ]
    polygon = Polygon(points)
    poly_with_holes = PolygonWithHoles(polygon, [])
    assert verify(poly_with_holes, []) == "polygons have empty union"


def test_verify_fail2():
    points = [
        Point(FieldNumber(x), FieldNumber(y))
        for x, y in ((0, 0), (1, 0), (1, 1), (0, 1))
    ]
    polygon = Polygon(points)
    poly_with_holes = PolygonWithHoles(polygon, [])
    solution = [
        Polygon(
            [Point(FieldNumber(x), FieldNumber(y)) for x, y in ((0, 0), (1, 0), (1, 1))]
        )
    ]
    assert "the union of the polygons leaves uncovered" in verify(
        poly_with_holes, solution
    )


def test_pyverify():
    instance = {
        "outer_boundary": [
            {"x": 0, "y": {"num": 0}},
            {"x": "1/1", "y": 0},
            {"x": 1, "y": {"num": 1, "den": "1"}},
            {"x": 0, "y": 1},
        ],
        "holes": [],
    }
    solution = {
        "polygons": [
            [
                {"x": 0, "y": {"num": 0}},
                {"x": "1/1", "y": 0},
                {"x": 1, "y": {"num": 1, "den": "1"}},
                {"x": 0, "y": 1},
            ]
        ]
    }
    assert verify_(instance, solution) == ""


def test_examples():
    path = os.path.join(os.path.dirname(__file__), "./example_instances.zip")
    if not os.path.exists(path):
        return
    idb = InstanceDatabase(path)
    sol_zip = zipfile.ZipFile(
        os.path.join(os.path.dirname(__file__), "./correct_test_solutions.zip")
    )
    filelist = list(sol_zip.filelist)
    random.shuffle(filelist)
    for solution_path in filelist:
        try:
            if solution_path.is_dir():
                continue
            print(solution_path.filename)
            solution = read_solution(sol_zip.open(solution_path))
            if solution["instance"] == "testing":
                continue
            instance = idb[solution["instance"]]
            msg = pyverify(instance, solution)
            assert msg == ""
        except KeyError as ke:
            print(ke)


def test_example_edgecases():
    path = os.path.join(os.path.dirname(__file__), "./example_instances.zip")
    if not os.path.exists(path):
        return
    idb = InstanceDatabase(path)
    sol_zip = zipfile.ZipFile(os.path.join(os.path.dirname(__file__), "./edgecase.zip"))
    filelist = list(sol_zip.filelist)
    random.shuffle(filelist)
    for solution_path in filelist:
        try:
            if solution_path.is_dir():
                continue
            print(solution_path.filename)
            solution = read_solution(sol_zip.open(solution_path))
            if solution["instance"] == "testing":
                continue
            instance = idb[solution["instance"]]
            msg = pyverify(instance, solution)
            assert msg == "" or "zero size" in msg
        except KeyError as ke:
            print(ke)


def test_bad_examples():
    path = os.path.join(os.path.dirname(__file__), "./example_instances.zip")
    if not os.path.exists(path):
        return
    idb = InstanceDatabase(path)
    sol_zip = zipfile.ZipFile(
        os.path.join(os.path.dirname(__file__), "./bad_solutions.zip")
    )
    filelist = list(sol_zip.filelist)
    random.shuffle(filelist)
    for solution_path in filelist:
        try:
            if (
                str(solution_path.filename)
                == "bad_solutions/area_error_maze_001_sol.json"
            ):
                continue
            if solution_path.is_dir():
                continue
            print(solution_path.filename)
            solution = read_solution(sol_zip.open(solution_path))
            if solution["instance"] == "testing":
                continue
            instance = idb[solution["instance"]]
            msg = pyverify(instance, solution)
            print(msg)
            assert msg != ""
        except KeyError as ke:
            print(ke)


def test_bad_example():
    solution_path = "bad_solutions/area_error_maze_001_sol.json"
    path = os.path.join(os.path.dirname(__file__), "./example_instances.zip")
    if not os.path.exists(path):
        return
    idb = InstanceDatabase(path)
    sol_zip = zipfile.ZipFile(
        os.path.join(os.path.dirname(__file__), "./bad_solutions.zip")
    )
    filelist = list(sol_zip.filelist)
    random.shuffle(filelist)
    print(solution_path)
    solution = read_solution(sol_zip.open(solution_path))

    instance = idb[solution["instance"]]
    msg = pyverify(instance, solution)
    assert msg != ""
    print(msg)
