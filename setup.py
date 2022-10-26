"""
This file instructs scitkit-build how to build the module. This is very close
to the classical setuptools, but wraps some things for us to build the native
modules easier and more reliable.
"""

from setuptools import find_packages
from skbuild import setup

# automatically running conan. Ugly workaround, but does its job.
import subprocess

subprocess.run(["conan", "install", ".", "-if", "cmake"], check=True)

setup(
    name="cgshop2023_pyutils",
    version="0.1.3",
    description="Official utilities for the CG:SHOP Challenge 2023.",
    packages=find_packages("python"),  # Include all packages in `./python`.
    package_dir={"": "python"},  # The root for out python package is in `./python`.
    python_requires=">=3.7",
)
