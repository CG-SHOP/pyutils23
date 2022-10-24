#ifndef CGSHOP2023_ARRANGEMENT_UTIL_HPP_
#define CGSHOP2023_ARRANGEMENT_UTIL_HPP_

#include "cgshop2023_core/cpp_instance.hpp"
#include <CGAL/Arr_segment_traits_2.h>
#include <CGAL/Arr_trapezoid_ric_point_location.h>
#include <CGAL/Arrangement_2.h>
#include <CGAL/Arrangement_with_history_2.h>
#include <CGAL/Iso_rectangle_2.h>
#include <CGAL/Triangular_expansion_visibility_2.h>
namespace cgshop2023 {

using NumType = Kernel::FT;
using ArrTraits = CGAL::Arr_segment_traits_2<Kernel>;
using Segment = ArrTraits::X_monotone_curve_2;
using Arrangement = CGAL::Arrangement_with_history_2<ArrTraits>;
using SimpleArrangement = CGAL::Arrangement_2<ArrTraits>;
using VertexHandle = Arrangement::Vertex_handle;
using FaceHandle = Arrangement::Face_handle;
using Rect = CGAL::Iso_rectangle_2<Kernel>;
using HalfedgeCirc = Arrangement::Ccb_halfedge_circulator;
using Visibility = CGAL::Triangular_expansion_visibility_2<Arrangement>;
using Location = CGAL::Arr_trapezoid_ric_point_location<Arrangement>;
using LocationResult = CGAL::Arr_point_location_result<Arrangement>::Type;

} // namespace cgshop2023

#endif
