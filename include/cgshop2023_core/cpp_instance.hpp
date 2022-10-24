#ifndef CGSHOP2023_VERIFIER_CPP_INSTANCE_HPP_INCLUDED_
#define CGSHOP2023_VERIFIER_CPP_INSTANCE_HPP_INCLUDED_

#include <CGAL/Boolean_set_operations_2.h>
#include <CGAL/Exact_predicates_exact_constructions_kernel.h>
#include <CGAL/Point_2.h>
#include <CGAL/Polygon_2.h>
#include <CGAL/Polygon_with_holes_2.h>
#include <algorithm>
#include <initializer_list>
#include <iostream>
#include <string>
#include <utility>
#include <vector>

namespace cgshop2023 {

using Kernel = CGAL::Epeck;
using Point = CGAL::Point_2<Kernel>;
using Polygon = CGAL::Polygon_with_holes_2<Kernel>;
using SimplePolygon = CGAL::Polygon_2<Kernel>;

Kernel::FT area(const Polygon &polygon);

class Instance {
public:
  explicit Instance(const Polygon &poly) : m_polygon(poly) {}
  explicit Instance(Polygon &&poly) : m_polygon(std::move(poly)) {}
  [[nodiscard]] const Polygon &polygon() const noexcept { return m_polygon; }

  void write(std::ostream &output, const std::string &name);
  static Instance read(std::istream &input, std::string &out_name);

  [[nodiscard]] std::size_t num_vertices() const noexcept {
    return std::transform_reduce(
        m_polygon.holes_begin(), m_polygon.holes_end(),
        m_polygon.outer_boundary().container().size(), std::plus<>(),
        [](const auto &hole) { return hole.container().size(); });
  }

private:
  Polygon m_polygon;
};

class Solution {
public:
  Solution() = default;

  template <typename InputIterator>
  Solution(InputIterator polys_begin, InputIterator polys_end)
      : m_polygons(polys_begin, polys_end) {}

  Solution(std::initializer_list<SimplePolygon> init)
      : Solution(std::begin(init), std::end(init)) {}

  explicit Solution(std::vector<SimplePolygon> &polygons)
      : m_polygons(polygons) {}
  explicit Solution(std::vector<SimplePolygon> &&polygons)
      : m_polygons{std::move(polygons)} {}

  [[nodiscard]] const std::vector<SimplePolygon> &polygons() const noexcept {
    return m_polygons;
  }

  [[nodiscard]] size_t size() const { return m_polygons.size(); }

  [[nodiscard]] const std::vector<Polygon> &coverage() const {
    if (!m_polygons.empty() && m_coverage.empty()) {
      CGAL::join(polygons().begin(), polygons().end(),
                 std::back_inserter(m_coverage));
    }
    return m_coverage;
  }

private:
  std::vector<SimplePolygon> m_polygons;
  mutable std::vector<Polygon> m_coverage = {};
};

} // namespace cgshop2023

#endif
