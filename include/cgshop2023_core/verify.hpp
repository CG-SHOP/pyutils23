#ifndef CGSHOP2023_VERIFIER_VERIFY_HPP_INCLUDED_
#define CGSHOP2023_VERIFIER_VERIFY_HPP_INCLUDED_

#include "cpp_instance.hpp"
#include <optional>
#include <string>

namespace cgshop2023 {

class SolutionVerifier {
public:
  SolutionVerifier(const Instance *instance, const Solution *solution) noexcept
      : m_error(std::nullopt), m_instance(instance), m_solution(solution) {}

  const Solution &solution() const noexcept { return *m_solution; }
  const Instance &instance() const noexcept { return *m_instance; }
  const std::optional<std::string> &error_message() const noexcept {
    return m_error;
  }

  bool verify();

private:
  bool p_verify_convexity();
  bool p_verify_coverage(const Polygon &coverage);
  std::optional<Polygon> compute_coverage();
  bool check_coverage_area_size(const Polygon &coverage);

  std::optional<std::string> m_error;
  const Instance *m_instance;
  const Solution *m_solution;
};

} // namespace cgshop2023

#endif
