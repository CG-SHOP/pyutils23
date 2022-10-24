"""lossless conversion to native format"""
from ..core import (
    FieldNumber,
    Point,
    Polygon,
    PolygonWithHoles,
)


def _to_number(number_data):
    if isinstance(number_data, float):
        if int(number_data) == number_data:
            return _to_number(int(number_data))
        try:
            num, fp = str(number_data).split(".")
            len_fp = len(str(number_data).split(".")[1])
            print("WARNING: Automatic float translation.")
            x = FieldNumber(num) + (FieldNumber(fp) / FieldNumber(10**len_fp))
            return x
        except Exception:
            pass
        raise ValueError("Floating point not supported.")
    if isinstance(number_data, int):
        return FieldNumber(number_data)
    if isinstance(number_data, str):
        number_data = number_data.strip()
        if "/" in number_data:
            elements = number_data.split("/")
            if len(elements) != 2:
                raise ValueError("Cannot convert number with multiple '/'")
            return _to_number(elements[0]) / _to_number(elements[1])
        if "." in number_data:
            elements = number_data.split(".")
            if len(elements) != 2:
                raise ValueError(f"Cannot parse {number_data}.")
            x = FieldNumber(elements[0]) + (
                FieldNumber(elements[1]) / FieldNumber(10 ** len(elements[1]))
            )
            return x
        if len(number_data) > 18:
            print("WARNING: Very large number.")
            return (
                FieldNumber(number_data[18:]) * FieldNumber(10**18)
            ) + FieldNumber(number_data[:18])
        return FieldNumber(number_data)
    if isinstance(number_data, dict):
        return _to_number(number_data["num"]) / _to_number(number_data.get("den", 1))
    raise ValueError(f"Don't know how to convert '{number_data}'.")


def _to_coordinate(point_data):
    if "x" not in point_data or "y" not in point_data:
        raise ValueError(f"Cannot parse point data '{point_data}'")
    x = _to_number(point_data["x"])
    y = _to_number(point_data["y"])
    return Point(x, y)


def _to_polygon(points_data):
    return Polygon([_to_coordinate(p) for p in points_data])


def _to_polygon_with_holes(boundary, holes):
    boundary = _to_polygon(boundary)
    if not float(boundary.area()) > 0:
        raise ValueError("Polygon with negative boundary volume.")
    holes = [_to_polygon(hole) for hole in holes]
    if not all(float(hole.area()) < 0 for hole in holes):
        raise ValueError("Polygon has clockwise holes.")
    return PolygonWithHoles(boundary, holes)
