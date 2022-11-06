//
// Python-bindings for the C++-part.
//
#include "cgshop2023_core/cpp_instance.hpp"
#include "cgshop2023_core/verify.hpp"
#include "cgshop2023_core/verify_instance.hpp"
#include <CGAL/number_utils.h>
#include <cmath>
#include <fmt/core.h>
#include <pybind11/operators.h> // to define operator overloading
#include <pybind11/pybind11.h>
#include <pybind11/stl.h> // automatic conversion of vectors
#include <string>

namespace py = pybind11;
using namespace cgshop2023;
using Polygon2 = CGAL::Polygon_2<Kernel>;
using Polygon2WithHoles = CGAL::Polygon_with_holes_2<Kernel>;

// Exact conversion of a long to FT.
auto to_exact(std::int64_t x) {
  using namespace cgshop2023;
  double lo32 = x & 0xffff'ffff;
  double hi32 = double(x >> 32) * 4294967296.0;
  return Kernel::FT(hi32) + Kernel::FT(lo32);
}

// Exact conversion of a string to FT.
Kernel::FT str_to_exact(std::string number) {
  number.erase(0, number.find_first_not_of('0'));
  if (number.empty())
    number += '0';
  if (std::count(number.begin(), number.end(), '/') == 1) { // rational numbers
    const auto point_pos = number.find('/');
    const auto numerator = str_to_exact(number.substr(0, point_pos));
    const auto denominator =
        str_to_exact(number.substr(point_pos + 1, number.length() - point_pos));
    return numerator / denominator;
  }
  constexpr size_t max_len = 14;
  if (number.length() <= max_len) {
    return to_exact(std::stol(number));
  }
  const Kernel::FT small_part =
      str_to_exact(number.substr(number.length() - max_len, max_len));
  const Kernel::FT large_part =
      std::pow(10, max_len) *
      str_to_exact(number.substr(0, number.length() - max_len));
  return large_part + small_part;
}

std::string verify(const Instance &instance, Solution &solution) {
  SolutionVerifier verifier(&instance, &solution);
  if (verifier.verify()) {
    return {""};
  } else {
    std::string msg = verifier.error_message().value();
    if (msg.empty()) {
      return "UNKNOWN ERROR WITHOUT MESSAGE!";
    }
    return msg;
  }
}

std::string verify(const Polygon2WithHoles &instance,
                   const std::vector<Polygon2> &solution) {
  Instance instance_{instance};
  Solution solution_{solution.cbegin(), solution.cend()};
  return verify(instance_, solution_);
}

bool verify_instance(const Instance &instance) {
  auto iv = InstanceVerifier(&instance);
  return iv.verify();
}

PYBIND11_MODULE(_cgshop2023_core, m) {
  // For copying: Note that the name _cgshop2023_core needs to fit the name in
  // the CMakeLists.txt.
  m.doc() =
      "Python bindings for the efficient verification core."; // optional module
                                                              // docstring

  // Exact numbers
  py::class_<Kernel::FT>(m, "FieldNumber",
                         "A container for exact numbers in CGAL.")
      .def(py::init(&to_exact))
      .def(py::init(&str_to_exact))
      .def(py::self / Kernel::FT())
      .def(py::self + Kernel::FT())
      .def(py::self * Kernel::FT())
      .def(py::self == Kernel::FT())
      .def("__float__", &CGAL::to_double<cgshop2023::Kernel::FT>)
      .def("__str__", [](const Kernel::FT &x) {
        return std::to_string(CGAL::to_double(x));
      });

  // Points
  py::class_<Point>(m, "Point", "A point in CGAL.")
      .def(py::init<Kernel::FT, Kernel::FT>())
      .def("x", [](const Point &p) { return p.x(); })
      .def("y", [](const Point &p) { return p.y(); })
      .def(py::self == Point())
      .def("__str__", [](const Point &p) {
        return fmt::format("({}, {})", CGAL::to_double(p.x()),
                           CGAL::to_double(p.y()));
      });

  // Polygons
  py::class_<Polygon2>(m, "Polygon", "A simple polygon in CGAL.")
      .def(py::init<>())
      .def(py::init([](const std::vector<Point> &vertices) {
        return std::make_unique<Polygon2>(vertices.begin(), vertices.end());
      }))
      .def("boundary",
           [](const Polygon2 &poly) {
             std::vector<Point> points;
             std::copy(poly.begin(), poly.end(), std::back_inserter(points));
             return points;
           })
      .def("is_simple", &Polygon2::is_simple)
      .def("area", [](const Polygon2 &poly) { return poly.area(); });
  py::class_<Polygon2WithHoles>(m, "PolygonWithHoles",
                                "A polygon with holes in CGAL.")
      .def(py::init(
          [](const Polygon2 &outer, const std::vector<Polygon2> &holes) {
            return new Polygon2WithHoles(outer, holes.begin(), holes.end());
          }))
      .def("outer_boundary",
           [](const Polygon2WithHoles &poly) { return poly.outer_boundary(); })
      .def("holes", [](const Polygon2WithHoles &poly) {
        std::vector<Polygon2> holes;
        std::copy(poly.holes_begin(), poly.holes_end(),
                  std::back_inserter(holes));
        return holes;
      });
  py::class_<Instance>(m, "NativeInstance",
                       "A native C++ container for an instance.")
      .def(py::init<Polygon2WithHoles>())
      .def("polygon", &Instance::polygon);
  py::class_<Solution>(m, "NativeSolution",
                       "A native C++ container for a solution.")
      .def(py::init<std::vector<SimplePolygon>>())
      .def("polygons", &Solution::polygons)
      .def("coverage", &Solution::coverage);
  m.def("area", &area);

  // verify
  m.def("verify", py::overload_cast<const Instance &, Solution &>(&verify),
        "Verify a solution.")
      .def("verify",
           py::overload_cast<const Polygon2WithHoles &,
                             const std::vector<Polygon2> &>(&verify),
           "Verify a solution.");
  m.def("verify_instance", &verify_instance, "Verify an instance.");
}
