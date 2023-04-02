// This code should help reproducing errors with CGAL.
#include <CGAL/Boolean_set_operations_2.h>
#include <CGAL/Exact_predicates_exact_constructions_kernel.h>
#include <CGAL/Point_2.h>
#include <CGAL/Polygon_2.h>
#include <CGAL/Polygon_with_holes_2.h>
#include <fstream>
#include <iostream>
#include <iterator>
#include <nlohmann/json.hpp>
#include <vector>
using json = nlohmann::json;

using Kernel = CGAL::Epeck;
using FT = Kernel::FT;
using Pt = CGAL::Point_2<Kernel>;
using Polygon2 = CGAL::Polygon_2<Kernel>;
using Polygon2WithHoles = CGAL::Polygon_with_holes_2<Kernel>;

auto to_exact(std::int64_t x) {
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
    return to_exact(std::int64_t(std::stoll(number)));
  }
  const Kernel::FT small_part =
      str_to_exact(number.substr(number.length() - max_len, max_len));
  const Kernel::FT large_part =
      std::pow(10, max_len) *
      str_to_exact(number.substr(0, number.length() - max_len));
  return large_part + small_part;
}

FT get_number(const json &data) {
  if(data.is_string()) {
    return str_to_exact(data);
  }
  std::string num = data["num"].get<std::string>();
  std::string den = data["den"].get<std::string>();
  return str_to_exact(num) / str_to_exact(den);
}
Kernel::FT area(const Polygon2WithHoles &polygon) {
  // Compute area of non-simple polygon
  auto area = polygon.outer_boundary().area();
  // hole areas are negative, so we can simply sum them up.
  return std::transform_reduce(polygon.holes_begin(), polygon.holes_end(), area,
                               std::plus<>(),
                               [](const auto &p) { return p.area(); });
}
int main(int argc, char **argv) {
  if(argc<=1) {
    std::cerr << "Specify a path to a json-encoded solution" <<std::endl;
  }
  std::string path{argv[1]};
  std::ifstream f(path);
  json data = json::parse(f);
  std::vector<Polygon2> polys;
  for (const auto &poly : data["polygons"]) {
    std::vector<Pt> boundary;
    for (const auto &point : poly) {
      boundary.emplace_back(get_number(point["x"]), get_number(point["y"]));
    }
    polys.push_back(Polygon2(boundary.begin(), boundary.end()));
  }
  std::vector<Polygon2WithHoles> coverage;
  CGAL::join(polys.begin(), polys.end(), std::back_inserter(coverage));
  std::cout << "Cov: " << coverage.size() << std::endl;
  std::cout << (area(coverage.at(0))> FT(4.25268e+17))<<std::endl;
}
