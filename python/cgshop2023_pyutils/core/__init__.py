"""
This file imports from the native code. This helps with coding, as the native part
is not available during coding but only after compilation.
"""
# flake8: noqa F401
from ._cgshop2023_core import (
    FieldNumber,
    Point,
    Polygon,
    PolygonWithHoles,
    NativeInstance,
    NativeSolution,
    area,
    verify,
    verify_instance,
)  # will only be available after building.
