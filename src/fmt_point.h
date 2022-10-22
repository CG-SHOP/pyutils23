//
// Adding support for formatting points with fmt.
//

#ifndef CGSHOP2023_FMT_POINT_H
#define CGSHOP2023_FMT_POINT_H

#include "cgshop2023_core/cpp_instance.hpp"
#include <fmt/core.h>
#include <fmt/format.h>

template <> struct fmt::formatter<cgshop2023::Point> {
  // Formats a point for fmt.
  constexpr auto parse(format_parse_context &ctx) -> decltype(ctx.begin()) {
    return ctx.begin();
  }

  template <typename FormatContext>
  auto format(const cgshop2023::Point &p, FormatContext &ctx) const
      -> decltype(ctx.out()) {
    // ctx.out() is an output iterator to write to.
    const auto x = CGAL::to_double(p.x());
    const auto y = CGAL::to_double(p.y());
    return fmt::format_to(ctx.out(), "({:.1f}, {:.1f})", x, y);
  }
};

#endif // CGSHOP2023_FMT_POINT_H
