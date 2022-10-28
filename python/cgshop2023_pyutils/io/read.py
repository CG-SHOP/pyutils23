import typing

from networkx.utils import open_file
import json


@open_file(0, mode="r")
def read_instance(path) -> typing.Dict:
    data = json.load(path)
    if data["type"] != "CGSHOP2023_Instance":
        raise ValueError("Not a CGSHOP2023 instance file")
    if not data["name"] or not isinstance(data["name"], str):
        raise ValueError("Missing instance name")
    if len(data["outer_boundary"]) < 3:
        raise ValueError("Outer boundary must have at least three points!")
    return data


@open_file(0, mode="r")
def read_solution(path) -> typing.Dict:
    data = json.load(path)
    return parse_solution(data)


def parse_solution(data):
    if data["type"] != "CGSHOP2023_Solution":
        raise ValueError("Not a CGSHOP2023 solution file")
    if "id" in data and "instance" not in data:
        data["instance"] = data["id"]
    if "name" in data and "instance" not in data:
        data["instance"] = data["name"]
    if not data["instance"] or not isinstance(data["instance"], str):
        raise ValueError("Missing instance name")
    data["instance"] = data["instance"].split("/")[-1].split(".")[0]
    polygons = data["polygons"]
    if not isinstance(polygons, list):
        raise ValueError("Solution is not a list.")
    data["polygons"] = [p for p in data["polygons"] if p]  # remove empty polygons
    if not polygons:
        raise ValueError("At least one polygon must be provided")
    if not all(isinstance(p, list) for p in polygons):
        raise ValueError("Badly encoded polygon. All polygons need to be lists.")
    if not all(len(p) >= 3 for p in polygons):
        raise ValueError(
            "All polygons need to consist of at least three distinct points."
        )
    return data
