#!/bin/sh
# This script is meant to build and install the module manually.
# All dependencies are automatically installed using pip and conan.
# If all dependencies are already installed, you can also just run `python3 setup.py install`.
pip install -r requirements.txt || exit  # python dependencies
cd cmake || exit
conan install .. --build=missing || exit  # c++ dependencies
cd ..
python3 setup.py install  # triggers building and installing the python module
