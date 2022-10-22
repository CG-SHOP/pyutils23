#include "../include/cgshop2023_core/cpp_instance.hpp"
#include "cgshop2023_core/verify_instance.hpp"
#include <fstream>

int main(int argc, char **argv) {
  using namespace cgshop2023;
  if (argc != 2) {
    std::cerr << "Required argument: Instance file path!\n";
    return 1;
  }
  std::ifstream input(argv[1], std::ios::in);
  std::string name;
  Instance instance = Instance::read(input, name);
  std::cout << "Read instance " << name << "..." << std::flush;
  InstanceVerifier verifier(&instance);
  bool vres = verifier.verify();
  std::cout << " done!" << std::endl;
  if (!vres) {
    std::cerr << "Invalid instance!\n";
  } else {
    std::cout << "Instance valid." << std::endl;
  }
  return !vres;
}
