#~~~~~~~~~~~~~~~ TEST LIBRARY SETUP ~~~~~~~~~~~~~~~~
CPMAddPackage("gh:onqtam/doctest@2.4.8")  # download/install/import doctest using CPM.
include(${doctest_SOURCE_DIR}/scripts/cmake/doctest.cmake)  # include doctest
enable_testing()

# ~~~~~~~~~~~~~~~ CREATE COMPILABLE TEST TARGET ~~~~~~~~~~~~~~~~~~~~
add_executable(cgshop2023_test)  # test target
target_sources(cgshop2023_test PRIVATE main.cpp)  # add the test files
# linking for using doctest and the public interface of the implementation
target_link_libraries(cgshop2023_test PRIVATE doctest::doctest)
target_link_libraries(cgshop2023_test PRIVATE cgshop2023_core)

# enable compilation warnings
target_compile_options(cgshop2023_test PRIVATE
        "$<$<CXX_COMPILER_ID:GNU,Clang,AppleClang>:-Wall>")
