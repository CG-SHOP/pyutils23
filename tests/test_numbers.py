from cgshop2023_pyutils.core import (
    FieldNumber,
    Point,
    Polygon,
    PolygonWithHoles,
)
import pytest


def test_basic():
    assert float(FieldNumber("1")) == 1.0
    for i in range(32):
        assert float(FieldNumber(f"{2 ** i}")) == 2**i
    for i in range(32):
        assert float(FieldNumber(f"{2 ** (i + 1)}") / FieldNumber("2")) == 2**i
    for i in range(32):
        x = 2**i
        assert float(FieldNumber(f"{x}") / FieldNumber(3)) == pytest.approx(x / 3)


def test_point():
    p = Point(FieldNumber("1"), FieldNumber("2"))
    assert str(p) == "(1, 2)"
    assert float(p.x()) == 1
    assert float(p.y()) == 2


def test_polygon():
    points = [
        Point(FieldNumber(x), FieldNumber(y))
        for x, y in ((0, 0), (1, 0), (1, 1), (0, 1))
    ]
    polygon = Polygon(points)
    assert len(polygon.boundary()) == 4
    assert float(polygon.area()) == 1
    for p in polygon.boundary():
        print(p)


def test_reversed_polygon():
    points = [
        Point(FieldNumber(x), FieldNumber(y))
        for x, y in ((0, 0), (1, 0), (1, 1), (0, 1))
    ][::-1]
    polygon = Polygon(points)
    assert len(polygon.boundary()) == 4
    assert float(polygon.area()) == -1
    for p in polygon.boundary():
        print(p)


def test_bad_polygon():
    points = [Point(FieldNumber(x), FieldNumber(y)) for x, y in ((0, 0),)]
    polygon = Polygon(points)
    assert len(polygon.boundary()) == 1
    assert float(polygon.area()) == 0
    for p in polygon.boundary():
        print(p)


def test_polygon_with_holes():
    points = [
        Point(FieldNumber(x), FieldNumber(y))
        for x, y in ((0, 0), (1, 0), (1, 1), (0, 1))
    ]
    polygon = Polygon(points)
    poly_with_holes = PolygonWithHoles(polygon, [])
    assert len(poly_with_holes.holes()) == 0
