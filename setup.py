"""
This file instructs scitkit-build how to build the module. This is very close
to the classical setuptools, but wraps some things for us to build the native
modules easier and more reliable.

For a proper installation with `pip install .`, you additionally need a
`pyproject.toml` to specify the dependencies to load this `setup.py`.

You can use `python3 setup.py install` to build and install the package
locally, with verbose output. To build this package in place, which may be
useful for debugging, use `python3 setup.py develop`. This will build
the native modules and move them into your source folder.

The setup options are documented here:
https://scikit-build.readthedocs.io/en/latest/usage.html#setup-options
"""
import os

from setuptools import find_packages
from skbuild import setup
import sys
import subprocess
import json

def conan_to_json(args):
    """
    Runs conan with the args and parses the output as json.
    """
    args = [sys.executable, "-m", "conans.conan"] + args
    return json.loads(subprocess.check_output(args).decode())
def create_conan_profile():
    # check if profile exists or create a default one automatically.
    if "default" in conan_to_json(["profile", "list", "-f", "json"]):
        return  # Profile already exists
    cmd = f"-m conans.conan profile detect"
    subprocess.run([sys.executable, *cmd.split(" ")], check=False, stderr=None)

def run_conan():
    """
    Running conan to get C++ dependencies
    """
    create_conan_profile()
    settings = {
        # "compiler.libcxx": "libstdc++11"  # maybe necessary to make sure the ABI fits
    }
    cmd = f"-m conans.conan install ."
    for key, val in settings.items():
        cmd += f" -s {key}={val}"
    cmd += " --build=missing"
    subprocess.run([sys.executable, *cmd.split(" ")], check=True)


def readme():
    # Simply return the README.md as string
    with open("README.md") as file:
        return file.read()


run_conan()  # automatically running conan. Ugly workaround, but does its job.
setup(  # https://scikit-build.readthedocs.io/en/latest/usage.html#setup-options
    # ~~~~~~~~~ BASIC INFORMATION ~~~~~~~~~~~
    name="cgshop2023_pyutils",
    version="0.2.11",  # TODO: Use better approach for managing version number.
    description="Official utilities for the CG:SHOP Challenge 2023.",
    long_description=readme(),
    url="https://github.com/CG-SHOP/pyutils23",
    long_description_content_type="text/markdown",
    author="TU Braunschweig, IBR, Algorithms Group (Phillip Keldenich and Dominik Krupke)",
    author_email="keldenich@ibr.cs.tu-bs.de, krupke@ibr.cs.tu-bs.de",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    # ~~~~~~~~~~~~ CRITICAL PYTHON SETUP ~~~~~~~~~~~~~~~~~~~
    # This project structures defines the python packages in a subfolder.
    # Thus, we have to collect this subfolder and define it as root.
    packages=find_packages("python"),  # Include all packages in `./python`.
    package_dir={"": "python"},  # The root for our python package is in `./python`.
    python_requires=">=3.7",  # lowest python version supported.
    install_requires=[
        # requirements necessary for basic usage (subset of requirements.txt)
        "chardet>=4.0.0",
        "networkx>=2.5.1",
        "requests>=2.25.1",
    ],
    # ~~~~~~~~~~~ CRITICAL CMAKE SETUP ~~~~~~~~~~~~~~~~~~~~~
    # Especially LTS systems often have very old CMake version (or none at all).
    # Defining this will automatically install locally a working version.
    cmake_minimum_required_version="3.17",
    #
    # By default, the `install` target is built (automatically provided).
    # To compile a specific target, use the following line.
    # Alternatively, you can use `if(NOT SKBUILD) ... endif()` in CMake, to
    # remove unneeded parts for packaging (like tests).
    # cmake_install_target = "install"
    #
    # In the cmake you defined by install(...) where to move the built target.
    # This is critical als only targets with install will be used by skbuild.
    # This should be relative paths to the project root, as you don't know
    # where the package will be packaged. You can change the root for the
    # install-paths with the following line. Note that you can also access
    # the installation root (including this modification) in cmake via
    # `CMAKE_INSTALL_PREFIX`. If your package misses some binaries, you
    # probably messed something up here or in the `install(...)` path.
    # cmake_install_dir = ".",
    # |-----------------------------------------------------------------------|
    # | If you are packing foreign code/bindings, look out if they do install |
    # | targets in global paths, like /usr/libs/. This could be a problem.    |
    # |-----------------------------------------------------------------------|
    #
    # Some CMake-projects allow you to configure it using parameters. You
    # can specify them for this Python-package using the following line.
    cmake_args=[
        # -----------------------------------------------------------
        # CUSTOM CMAKE ARGUMENTS:
        # "-DCGALPY_KERNEL_BINDINGS=epec",
        #             "-DCGALPY_ARRANGEMENT_ON_SURFACE_2_BINDINGS=ON",
        # ------------------------------------------------------------
        # MANDATORY CMAKE ARGUMENTS FOR CONAN:
        # The following cmake-argument is necessary to load the toolchain
        # of conan. The absolute path is necessary as otherwise the
        # probing of scikit-build does not work.
        f"-DCMAKE_TOOLCHAIN_FILE={os.path.abspath('./conan_toolchain.cmake')}",
    ]
    #
    # There are further options, but you should be fine with these above.
)
