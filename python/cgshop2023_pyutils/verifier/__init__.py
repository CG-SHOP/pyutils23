"""
This file provides functions to verify instances and solutions.
The primary logic is convering the data to a native format
with exact data types and wrapping the C++-code.
"""
# flake8: noqa F401
import typing

from ..core import (
    NativeInstance,
    NativeSolution,
    verify as verify_,
    verify_instance as _verify_instance,
)

from ._convert_to_native_format import _to_polygon, _to_polygon_with_holes


def verify(instance: typing.Dict, solution: typing.Dict):
    """
    Verify a solution for an instance. This function uses C++ code, CGAL, and exact arithmetics
    to obtain exact results within a few seconds.
    :param instance: The data of the instance as parsed from the json.
    :param solution: The data of the solution as parsed from the json. Use our parser
            to verify the correctness of the format.
    :return: An empty string if the solution is valid. Otherwise, an error message.
    """
    instance_poly = _to_polygon_with_holes(
        instance["outer_boundary"], instance["holes"]
    )
    n_instance = NativeInstance(instance_poly)
    solution_polys = [_to_polygon(poly) for poly in solution["polygons"]]

    n_solution = NativeSolution(solution_polys)
    if not all(float(p.area()) > 0 for p in solution_polys):
        return "Solution contains polygons of zero size."
    error_msg = verify_(n_instance, n_solution)
    return error_msg


def verify_instance(instance: typing.Dict):
    """
    Verify an instance to be valid.
    :param instance: The data of the instance as parsed from the json.
    :return: True if it is valid, otherwise false.
    """
    instance_poly = _to_polygon_with_holes(
        instance["outer_boundary"], instance["holes"]
    )
    n_instance = NativeInstance(instance_poly)
    return _verify_instance(n_instance)
