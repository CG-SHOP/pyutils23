# This is the root file for CMake, which is used to define the native part
# of the project. It is completely independent of the Python-part and can
# actually be used just to build a C++-library.
cmake_minimum_required(VERSION 3.17)  # 3.17 has been released March 2020

project(cgshop2023 CXX)  # Feel free to add more project information
set(CMAKE_CXX_STANDARD 17)  # Using C++-17 (most features with good support at 2022)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)  # The code needs to be compiled as PIC to build the shared lib for python.
include(./cmake/CCache.cmake)  # Magic to speed up compiling by caching.

#~~~~~~~~~~~~~~~~~~~ CPM Dependencies ~~~~~~~~~~~~~~~~
# CPM allows us to include some simple dependencies without much fuss.
# Great default, for everything more complicated, uses conan.
# Why not always use conan? CPM works without any interaction (conan needs
# to be called externally). CPM also has no problems with install PyBind11
# (which conan has at the time).
# If the dependency has complicated dependencies on its own or is slow to
# compile, better use conan.
include(./cmake/CPM.cmake)  # Package manager for simple requirements.

CPMAddPackage("gh:fmtlib/fmt#9.1.0")  # fmt for nice strings
# further CPM-dependencies are defined in the subdirectories

#~~~~~~~~~~~~~~~~~ Conan dependencies ~~~~~~~~~~~~~~~~~~~~~
# We are using the `cmake_find_package` generator to create `FindXXX`-files
# in the `cmake`-folder. This is only necessary, if the packages are not
# already installed. This approach is not without its problems:
# PRO: Simple option that is compatible with scikit-build. Can work without conan.
# CON: Difficult if you want to use changing conan settings.

# run `conan install .. --build=missing` in `./cmake`.
list(APPEND CMAKE_MODULE_PATH ${CMAKE_SOURCE_DIR}/cmake)
list(APPEND CMAKE_PREFIX_PATH ${CMAKE_SOURCE_DIR}/cmake)
list(APPEND CMAKE_MODULE_PATH ${CMAKE_BINARY_DIR})


# Also need to be defined in `./conanfile.txt`.
find_package(CGAL REQUIRED)
find_package(nlohmann_json REQUIRED)

#~~~~~~~~~~~~~~~~~~~ C++-Library ~~~~~~~~~~~~~~~~~~~~~~~~~
# This part defines the actual C++-library that may be used as a simple
# C++-library. The Python-interface to this library is defined separately.
add_library(cgshop2023_core)  # define library target
# provide the public header files to users.
target_include_directories(cgshop2023_core PUBLIC ./include)
# Add the files needed for compilation
target_sources(cgshop2023_core
        PUBLIC  # public headers of the API
        include/cgshop2023_core/cpp_instance.hpp
        include/cgshop2023_core/verify.hpp
        PRIVATE  # implementation details
        src/cpp_instance.cpp
        src/verify.cpp
        src/arrangement_util.hpp)
# enable warnings
target_compile_options(cgshop2023_core PRIVATE
        "$<$<CXX_COMPILER_ID:GNU,Clang,AppleClang>:-Wall>")
# link dependencies. Using PUBLIC allows us to use them also when defining the
# python-bindings.
target_link_libraries(cgshop2023_core
        PUBLIC CGAL::CGAL nlohmann_json::nlohmann_json fmt::fmt)

#~~~~~~~~~~~ TESTS OF THE PUBLIC INTERFACE ~~~~~~~~~~~~~~
# A good programmer will add at least some unit tests.
# The tests-folder can also be used for Python-tests, without interference.
if (NOT SKBUILD)
    # only import if exists. The production code may be shipped without.
    add_subdirectory(tests)  # defined in a separate CMakeLists.txt
endif ()

#~~~~~~~~~~~~~~~~~~ Python Interface ~~~~~~~~~~~~~~~~~~~~
# The Python-bindings are compiled as separate target to allow the independent
# usage of the C++-library.
add_subdirectory(python)  # defined in a separate CMakeLists.txt

#~~~~~~~~~~~~~~~~ Apps ~~~~~~~~~~~~~~~~~~~~~~~~~~~
if (NOT SKBUILD)  # only make available if not using SKBUILD.
    add_executable(bad_cgal
            apps/cgal_problem.cpp)
    target_link_libraries(bad_cgal CGAL::CGAL)

    add_executable(verify_instance
            apps/cpp_verify_instance.cpp
            include/cgshop2023_core/cpp_instance.hpp
            include/cgshop2023_core/verify.hpp
            src/cpp_instance.cpp
            src/verify.cpp
            src/arrangement_util.hpp
            )
    target_include_directories(verify_instance PUBLIC ./include)
    target_link_libraries(verify_instance
            CGAL::CGAL nlohmann_json::nlohmann_json fmt::fmt)
endif ()
