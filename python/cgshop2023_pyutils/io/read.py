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
    if data["type"] != "CGSHOP2023_Solution":
        raise ValueError("Not a CGSHOP2023 solution file")
    if "id" in data and "instance" not in data:
        data["instance"] = data["id"]
    if "name" in data and "instance" not in data:
        data["instance"] = data["name"]
    if not data["instance"] or not isinstance(data["instance"], str):
        raise ValueError("Missing instance name")
    polygons = data["polygons"]
    if not isinstance(polygons, list) or not polygons:
        raise ValueError("At least one polygon must be provided")
    return data
