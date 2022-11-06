#include "cgshop2023_core/verify.hpp"
#include "./fmt_point.h"
#include <CGAL/Boolean_set_operations_2.h>
#include <fmt/core.h>
#include <fmt/format.h>
#include <functional>
#include <numeric>
#include <type_traits>

namespace cgshop2023 {

// check that all polygons of the solution are convex
bool SolutionVerifier::p_verify_convexity() {
  std::size_t idx = 0;
  for (const SimplePolygon &poly : solution().polygons()) {
    if (!poly.is_simple()) {
      m_error = fmt::format("polygon {} is not simple", idx);
      return false;
    }
    auto has_zero_length = [](const auto &edge) {
      return edge.squared_length() == 0;
    };
    if (std::any_of(poly.edges_begin(), poly.edges_end(), has_zero_length)) {
      m_error = fmt::format("polygon {} has a zero length edge", idx);
      return false;
    }
    if (!poly.is_convex()) {
      m_error = fmt::format("polygon {} is not convex", idx);
      return false;
    }
    ++idx;
  }
  return true;
}

std::optional<Polygon> SolutionVerifier::compute_coverage() {
  auto union_results = solution().coverage();
  if (union_results.empty()) {
    m_error = fmt::format("polygons have empty union");
    return {};
  }
  if (union_results.size() > 1) {
    m_error = fmt::format("polygons have disconnected union");
    return {};
  }
  return union_results.at(0);
}

Kernel::FT area(const Polygon &polygon) {
  // Compute area of non-simple polygon
  auto area = polygon.outer_boundary().area();
  // hole areas are negative, so we can simply sum them up.
  return std::transform_reduce(polygon.holes_begin(), polygon.holes_end(), area,
                               std::plus<>(),
                               [](const auto &p) { return p.area(); });
}

// check that the entire instance is covered
bool SolutionVerifier::p_verify_coverage(const Polygon &coverage) {
  const Polygon &ipoly = instance().polygon();
  std::vector<Polygon> diff_results;
  CGAL::difference(ipoly, coverage, std::back_inserter(diff_results));
  return std::all_of(
      diff_results.begin(), diff_results.end(), [&](const auto &poly) {
        const auto &ob = poly.outer_boundary();
        if (area(poly) > 0) {
          m_error =
              fmt::format("the union of the polygons leaves uncovered some "
                          "area of volume {} at or near point {}",
                          CGAL::to_double(area(poly)), *ob.vertices_begin());
          return false;
        }
        return true;
      });
}

bool SolutionVerifier::verify() {
  if (!p_verify_convexity())
    return false;
  auto coverage = compute_coverage();
  if (coverage) {
    if (!check_coverage_area_size(*coverage))
      return false;
    if (!p_verify_coverage(*coverage))
      return false;
    if (area(*coverage) != area(instance().polygon())) {
      m_error = "The area doesn't fit, but somehow no rule has been triggered";
      return false;
    }
    return true;
  }
  return false;
}

bool SolutionVerifier::check_coverage_area_size(const Polygon &coverage) {
  const Polygon &ipoly = instance().polygon();
  if (area(coverage) > area(ipoly)) {
    m_error = fmt::format("the solution covers more area than the instance.");
    return false;
  }
  return true;
}

} // namespace cgshop2023
