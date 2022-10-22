#include "../include/cgshop2023_core/cpp_instance.hpp"
#include <exception>
#include <nlohmann/json.hpp>
#include <stdexcept>
#include <string>
#include <type_traits>

namespace cgshop2023 {

template <typename K, typename V>
static void write_kv(std::ostream &output, const K &key, const V &value) {
  output << '\"' << key << "\": ";
  if constexpr (std::is_integral_v<V> || std::is_floating_point_v<V>) {
    output << value;
  } else {
    output << '\"' << value << '\"';
  }
}

template <typename P>
static void write_point(std::ostream &output, const P &p) {
  output << "{\"x\": " << int(std::round(CGAL::to_double(p.x())))
         << ", \"y\": " << int(std::round(CGAL::to_double(p.y()))) << "}";
}

template <typename PC>
static void write_point_container(std::ostream &out, const PC &c) {
  out << '[';
  auto beg = c.begin();
  auto last = c.end();
  --last;
  for (; beg != last; ++beg) {
    write_point(out, *beg);
    out << ", ";
  }
  write_point(out, *last);
  out << ']';
}

void Instance::write(std::ostream &output, const std::string &name) {
  output << '{';
  write_kv(output, "type", "CGSHOP2023_Instance");
  output << ", ";
  write_kv(output, "name", name);
  output << ", ";
  write_kv(output, "n", num_vertices());
  output << ", \"outer_boundary\": ";
  write_point_container(output, m_polygon.outer_boundary().container());
  output << ", ";
  const auto &hc = m_polygon.holes();
  if (!hc.empty()) {
    output << "\"holes\": [";
    auto hlast = hc.end();
    --hlast;
    for (auto hi = hc.begin(); hi != hlast; ++hi) {
      write_point_container(output, hi->container());
      output << ", ";
    }
    write_point_container(output, hlast->container());
    output << ']';
  } else {
    output << "\"holes\": []";
  }
  output << "}\n";
}

static Kernel::FT int64_to_cgal_exact(std::int64_t v) {
  double lo32 = v & 0xffffffff;
  double hi32 = double(v >> 32) * 4294967296.0;
  return Kernel::FT(lo32) + Kernel::FT(hi32);
}

static SimplePolygon json_to_points(const nlohmann::json &plist) {
  std::vector<Point> points;
  for (const auto &p : plist) {
    std::int64_t x = p.at("x").get<std::int64_t>();
    std::int64_t y = p.at("y").get<std::int64_t>();
    points.emplace_back(int64_to_cgal_exact(x), int64_to_cgal_exact(y));
  }
  return SimplePolygon(points.begin(), points.end());
}

Instance Instance::read(std::istream &input, std::string &out_name) {
  nlohmann::json jsdata;
  input >> jsdata;
  if (jsdata.at("type") != "CGSHOP2023_Instance") {
    throw std::runtime_error("Not a CGSHOP 2023 instance file!");
  }
  out_name = jsdata.at("name").get<std::string>();
  const auto &ob = jsdata.at("outer_boundary");
  const auto &holes = jsdata.at("holes");
  std::vector<SimplePolygon> out_holes;
  SimplePolygon boundary = json_to_points(ob);
  for (const auto &h : holes) {
    out_holes.emplace_back(json_to_points(h));
  }
  return Instance(
      Polygon(std::move(boundary), out_holes.begin(), out_holes.end()));
}

} // namespace cgshop2023
