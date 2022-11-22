"""
A Python module for parsing and verifying instances and solutions for the
CG:SHOP 2023 challenge.

Use `read_instance(path)->dict` to parse an instance.
Use `read_solution(path)->dict` to parse a solution.

The InstanceDatabase is for reading the instances directly from the ZIP file
by name/instance-id. It can also cache the instances.

Use `verify(Instance, Solution)->str` to verify a solution.
It will return an empty string if everything is ok, otherwise a message
describing the problem.

This library uses a compiled C++-core. If you get segmentation faults, you
may want remove and reinstall it, in order to trigger a recompilation.
See the readme for further information.
"""
# flake8: noqa F401
from .io import read_solution, read_instance
from .instance_database import InstanceDatabase
from .verifier import verify
