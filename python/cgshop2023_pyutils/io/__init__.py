"""
Just simple parsing of json files, including some checking and cleaning.
"""
# flake8: noqa F401
from .read import read_instance, read_solution, parse_solution, BadSolutionFile, NoSolution
