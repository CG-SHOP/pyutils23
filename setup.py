"""
This file instructs scitkit-build how to build the module. This is very close
to the classical setuptools, but wraps some things for us to build the native
modules easier and more reliable.
"""

from setuptools import find_packages
from skbuild import setup

# automatically running conan. Ugly workaround, but does its job.
import subprocess

subprocess.run(
    ["python3", "-m", "conans.conan", "install", ".", "-if", "cmake"], check=True
)


def readme():
    """
    :return: Content of README.md
    """
    with open("README.md") as file:
        return file.read()


setup(
    name="cgshop2023_pyutils",
    version="0.2.1",
    description="Official utilities for the CG:SHOP Challenge 2023.",
    long_description=readme(),
    url="https://github.com/CG-SHOP/pyutils23",
    long_description_content_type="text/markdown",
    author="TU Braunschweig, IBR, Algorithms Group (Phillip Keldenich and Dominik Krupke)",
    author_email="keldenich@ibr.cs.tu-bs.de, krupke@ibr.cs.tu-bs.de",
    packages=find_packages("python"),  # Include all packages in `./python`.
    package_dir={"": "python"},  # The root for out python package is in `./python`.
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    install_requires=[
        # requirements necessary for basic usage (subset of requirements.txt)
        "chardet>=4.0.0",
        "networkx>=2.5.1",
        "requests>=2.25.1",
    ],
)
