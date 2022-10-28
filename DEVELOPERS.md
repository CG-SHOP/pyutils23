# Developer's Notes

This package is a Python-module with native C++-code for efficiently using CGAL.
There are actually already Python-bindings for CGAL (scitkit-geometry may be
the easiest option), but this way we have some more control.

The structure of this project contains some thoughts in order to allow to build
simple Python-packages, pure C++-libraries, C++-libraries with a Python-binding,
and Python-packages with native C++-elements. Using this structure, you can start
with a Python-package and add a native part later to speed things up, or
you can start with a C++-library and later decide to also add Python-bindings.

> If you have any suggestions for improving this, please let us know.

## C++-Library

The C++-code is to be structured classically using `include` for the public
interface and `src` for implementation details. Repeat the library-name in
`include` to simplify the `#include` statements (i.e., prevent naming
collisions).

The project is configured using CMake. We define the C++-library in
the root file `./CMakeLists.txt` but the other targets (tests and
python-binding) will be defined in subdirectories. There are two
extensions in the `cmake`-folder: CPM (a simple package manager) and
CCache for caching.
CPM will automatically install some simple dependencies.

For complex dependencies we use _conan_ on top. conan is much more powerful
and faster than CPM, but requires manual intervention, making it annoying
to use for some quick coding projects. We use it for CGAL and nlohmann_json.
CGAL has very complex dependencies which would be difficult to handle with CPM
and nlohmann_json is slow to compile with CPM (conan seems to have precompiled
binaries available).

conan offers a number of generators for integrating the dependencies into
your project. Even for CMake-projects, there are various options with pros
and cons. In this project, we went for the maybe controversial decision to
use the `cmake_find_package`-generator, which creates individual `FindXXX.cmake`
files for each dependency that can be used by cmake. We generate these into
the `cmake`-folder. This may be ugly (having generated code among sources)
and be problematic when you want to build the dependencies with varying conan
configurations (few use cases), but it makes the project independent of conan
(if you want to install the dependencies differently) and it works nicely
with scikit-build (for building Python-bindings). The decision for using
a `conanfile.txt` instead of the more modern `py` is purely for simplicity.

The CMakeLists.txt is extensively documented and should give you further
insights.

The C++-related projected structure is shown below.

```text
Project without Python-API
├── cmake                   <- cmake extensions. conan will also generate files in here.
│   ├── CCache.cmake
│   └── CPM.cmake
├── CMakeLists.txt          <- root file of CMake-project
├── conanfile.txt           <- define conan dependencies
├── include                 <- public api (headers)
│   └── libname             <- repeat library name for easier import
│       └── libapi.h        <- A header defining a public interface
├── src                     <- implementation details
│   └── ... (*.cpp)
└── tests                   <- add some unit tests
    ├── CMakeLists.txt      <- keep the root CMakeLists simple
    └── main.cpp
```

To build this project, do

```shell
# conan
cd cmake
conan install .. --build=missing
cd ..
# cmake (maybe simply use your IDE)
mkdir bin-release
cmake -S . -B bin-release -DCMAKE_BUILD_TYPE=Release
```

## Python-Package

Python luckily is much easier to build than C++, primarily because it simply
has to be packed and this can easily be done using setuptools.

The Python-sources are to be put into the `python`-folder. Unittests
can be added to `tests` (which is also used by C++). Python dependencies should
be added to `requirements.txt`. The package is to be defined in `setup.py`.

To learn more about packing pure python packages, look [here](https://setuptools.pypa.io/en/latest/).

```text
Python structure without C++
├── python                          <- contains your python sources
│   ├── cgshop2023_pyutils          <- your python package (repeat name)
│   │   ├── __init__.py             <- your code
│   │   └── ...
│   │       └── ...
├── requirements.txt                <- python dependencies for pip
├── setup.py                        <- define package
└── tests                           <- add some tests
    ├── __init__.py
    ├── ...
    └── test_x.py
```

One important thing to note here is, that the tests in `tests` will
test the package, not the sources in `python`. So before running the
tests, you have to do `python3 setup.py install` to build and install
your package. For some quick, in-development-testing, just add the
unittests to the sources and move them later to `tests` when they
become more stable.

> You could actually skip the `python` folder as there is the package folder too. However, this helps me to separate things clearly. Maybe the name `python` is not so good, because pycharm will automatically do some bad magic.

## Using the C++-library in Python

Alright, so you have some code in Python and some in C++ and want to make
the C++-code accessible in Python.
For this, we add a CMakeLists.txt in the `python`-folder and a
C++-file containing the bindings at the corresponding location.
It is recommendable to wrap this file in a submodule and an `__init__.py`.
The native part should be protected.

```text
Example project with Python-API
├── cmake
│   ├── CCache.cmake
│   └── CPM.cmake
├── CMakeLists.txt
├── conanfile.txt
├── include
│   └── fastcode
│       └── fastcode.h
├── MANIFEST.in              <- Defines source files (copy and paste thanks to regex)
├── pyproject.toml           <- Tells pip how to init the build process before setup.py
├── python
│   ├── CMakeLists.txt
│   └── pyfastcode
│       ├── binding.cpp      <- Bindings
│       └── __init__.py
├── README.md
├── requirements.txt
├── setup.py
├── src
│   └── fastcode.cpp
└── tests
    ├── CMakeLists.txt
    ├── test_x.py
    └── main.cpp
```

The build will be driven by scikit-build. The setup will happen in `setup.py`.
However, you also have to make sure that the cmake project will copy the binaries
to the right positions in the python module. Check out the `setup.py` and `python/CMakeLists.txt`.

You can build the package with

```shell
pip install .
```

or

```shell
python3 setup.py development
```

if you want to create the binaries in-source for development.

## Coding Style

We roughly follow [scikit-hep](https://scikit-hep.org/developer/style).

## Tools

Run the following command to get some basic feedback and automatic clean up.

```shell
pre-commit run --all-files
```

`pre-commit` can be installed via pip and can be setup to run automatically before any `git commit`.
The first run takes some time because it automatically installs all dependencies in some virtual environment.

The config `.pre-commit-config.yaml` is set up for Python and C++ and can simply be copied for any Python/C++-project.
It currently uses `black` for Python linting and `llvm`-style for C++. Simply search and replace if you want
something else (for `black` it can be more difficult). The config is not very sensitive in favour of generality, so
you should use additional static code analyzers.
