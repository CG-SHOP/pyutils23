#ifndef CGSHOP2023_VERIFY_INSTANCE_HPP_INCLUDED_
#define CGSHOP2023_VERIFY_INSTANCE_HPP_INCLUDED_

#include "../../src/arrangement_util.hpp"
#include "cpp_instance.hpp"
#include <CGAL/Polygon_2_algorithms.h>

namespace cgshop2023 {
class InstanceVerifier {
public:
  explicit InstanceVerifier(const Instance *instance)
      : instance(instance), location(arrangement) {}

  bool verify() {
    if (!p_check_simplicity()) {
      return false;
    }
    if (!p_add_and_check(instance->polygon().outer_boundary(),
                         arrangement.unbounded_face())) {
      std::cerr << "Outer boundary invalid!\n";
      return false;
    }
    auto first_inner = *arrangement.unbounded_face()->holes_begin();
    auto interior = first_inner->twin()->face();
    for (const auto &h : instance->polygon().holes()) {
      if (!p_add_and_check(h, interior)) {
        return false;
      }
    }
    if (arrangement.unbounded_face()->number_of_holes() != 1) {
      std::cerr << "Unbounded face must have exactly 1 hole, but has "
                << arrangement.unbounded_face()->number_of_holes() << "!\n";
      return false;
    }
    return true;
  }

private:
  bool p_check_simplicity() {
    if (!p_check_simplicity(instance->polygon().outer_boundary())) {
      std::cerr << "Outer boundary is self-intersecting!\n";
      return false;
    }
    std::size_t i = 0;
    for (const auto &h : instance->polygon().holes()) {
      if (!p_check_simplicity(h)) {
        std::cerr << "Hole #" << i << " is self-intersecting!\n";
        return false;
      }
      ++i;
    }
    return true;
  }

  bool p_check_simplicity(const SimplePolygon &sp) {
    const auto &c = sp.container();
    return c.size() >= 3 && CGAL::is_simple_2(c.begin(), c.end(), Kernel{});
  }

  bool p_add_and_check(const SimplePolygon &sp, FaceHandle expected_face) {
    const auto &c = sp.container();
    const Point *prev = &c.back();
    std::vector<LocationResult> zones;
    for (const auto &curr : c) {
      Segment next_seg{*prev, curr};
      CGAL::zone(arrangement, next_seg, std::back_inserter(zones), location);
      if (zones.size() > 1) {
        for (const auto &lr : zones) {
          const Arrangement::Vertex_const_handle *vh;
          const Arrangement::Halfedge_const_handle *eh;
          if ((vh = boost::get<Arrangement::Vertex_const_handle>(&lr))) {
            std::cerr << "Segment (" << next_seg << ") contains vertex "
                      << (*vh)->point() << "!\n";
          } else if ((eh = boost::get<Arrangement::Halfedge_const_handle>(
                          &lr))) {
            std::cerr << "Segment (" << next_seg << ") intersects segment "
                      << (*eh)->curve() << "!\n";
          }
        }
        return false;
      } else {
        const Arrangement::Face_const_handle *fh;
        if (!(fh =
                  boost::get<Arrangement::Face_const_handle>(&zones.front()))) {
          std::cerr << "Segment (" << next_seg
                    << ") in unexpected arrangement feature!\n";
          return false;
        }
        if (*fh != expected_face) {
          std::cerr << "Segment (" << next_seg
                    << ") lies in unexpected face (either hole-in-hole or hole "
                       "outside of boundary)!\n";
          return false;
        }
      }
      zones.clear();
      prev = &curr;
    }
    for (const auto &curr : c) {
      Segment next_seg{*prev, curr};
      CGAL::insert(arrangement, next_seg, location);
      prev = &curr;
    }
    return true;
  }

  const Instance *instance;
  Arrangement arrangement;
  Location location;
};
} // namespace cgshop2023

#endif
