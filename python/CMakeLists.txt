# This file defines the structure of the python-binding.

# ~~~~~~~~~~~~~ Dependencies via CPM ~~~~~~~~~~~~~~~~~
CPMAddPackage("gh:pybind/pybind11@2.10.0")  # pybind11, essential


# Repeat the following part for every binding-module you want to build.
# If the different bindings need to interact with each other/share data, it
# may be easier (and cheaper) to have just a single binding. A single binding define
# as many classes and functions as you want.
# ~~~~~~~~~~ Create a new Python-module ~~~~~~~~~~~~~~~~~~~~~
pybind11_add_module(_cgshop2023_core  # target name with leading `_` as this will be a protected module.
        cgshop2023_pyutils/core/binding.cpp)  # the file with the API.
# link your C++-library to the API.
target_link_libraries(_cgshop2023_core PRIVATE cgshop2023_core)
# link other dependencies
target_link_libraries(_cgshop2023_core PRIVATE fmt::fmt CGAL::CGAL)
# enable compilation warnings
target_compile_options(_cgshop2023_core PRIVATE
        "$<$<CXX_COMPILER_ID:GNU,Clang,AppleClang>:-Wall>")
# This definition is important for skbuild to copy the binary to the right
# position in the package.
# !!! This part is critical and a wrong configuration leads to bad packages
# !!! without an error. Use a path relative to the project root (or
# !!! `cmake_install_dir`[setup.py], if used).
install(TARGETS _cgshop2023_core DESTINATION ./python/cgshop2023_pyutils/core)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
