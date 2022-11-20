# CG:SHOP 2023 Utilities

This project provides the utilities for parsing and verifying solutions for the
[CG:SHOP Challenge 2023](https://cgshop.ibr.cs.tu-bs.de/competition/cg-shop-2023/#problem-description).
The verification is exact and expecting most solutions to
be feasible, which is probably too slow for optimization purposes. For optimization,
you should probably implement a faster, inexact method and only use our implementation
for final verification.

This project shall also be an example on how one can build a Python package
with complex C++-code (especially, complex dependencies). The project is extensively
documented for this purpose and you can find further information in
[DEVELOPERS.md](./DEVELOPERS.md). The project may also be a good starting point to
implement an effizient optimizer with Python and C++.

> We are happy about any feedback. Please use the issue-function for suggestions, as they
> may be interesting for all participants.

## Installation

Installation is easy via

```shell
pip install csghop2023-pyutils
```

Note that this can take some minutes, because a native core based on CGAL will
automatically be compiled on your machine. We may provide precompiled versions for
some systems in the future.

If anything goes wrong, please open an issue or write us a mail. Automatically
compiling C++-code is not trivial on arbitrary setups, and we may not be
aware of some problems with special configurations (or environemnts that
do not have all developer tools installed by default).

### Requirements

Your system needs to be able to build C++-code, i.e., have gcc or clang available.
We expected most participants to already have such a setup, otherwise you should
get a proper error message explaining the problem (if not, please open an issue).
Mac OS X users may have to execute `xcode-select --install`.

> :warning: The installation takes some minutes and needs a stable internet connection!
> If it fails, simply try again. If it fails again, please open an issue to let us know
> about the problem.

If you are using conda, you may need to install the C++-compiler within the conda
environment first as otherwise glibc may be incompatible. You can do so by executing
`conda install -c conda-forge cxx-compiler` within the environment.

## Usage

### Reading instances

Instances and solution are parsed as simple dictionaries, as you may want to
use custom types for handling the numeric of the rational numbers.
While the C++-core actually exposes exact types for this, we disabled most
arithmetic functions on purpose, because this library is only supposed
to verify given data, not manipulate it. However, you can easily enable
the arithmetic operations if you want to work in Python.

```python
from cgshop2023_pyutils import InstanceDatabase

idb = InstanceDatabase("path/to/zip/or/folder/with/instances")
instance = idb["instance_name"]
print(instance["outer_boundary"])
```

### Verifying solutions

The verification will return a string with the error message if the
solution is invalid. Otherwise, it will return an empty string.

```python
from cgshop2023_pyutils import read_solution, verify

solution = read_solution("explicit/path/to/solution.json")
instance = idb[solution["instance"]]

err_msg = verify(instance, solution)
if err_msg:
    print("SOLUTION INVALID:", err_msg)
```

## Notes on CGAL version

We noticed troubles with inconsistent (wrong) results of the `CGAL::join` operation,
despite using the exact predicates and exact constructions kernel (`epeck`),
with CGAL 5.5.
Additionally, there seemed to be some unexplainable segmentation faults deep within CGAL::difference and CGAL::join.
We did not observe these problems with CGAL 5.3, so we are using that version.
We are still working on locating the problem: is there really a bug in CGAL or did
we do something wrong (despite this being very simple code)? Unfortunately, this
problem only happened for very complex instances and was hard to reproduce.

> If the verification gives you an error message you cannot explain, please
> inform us. It may be possible, that the issue still exists.

## Changes

- _0.2.9_ Throwing an error if no solutions where found.
- _0.2.8_ Fixing 0.2.7, as try-except was placed around the wrong block.
- _0.2.7_ Slightly changed handling of bad encodings. Files without correct type will automatically be skipped without error.
- _0.2.6_ Add `cmake_minimum_require_version` to hopefully expand support for older systems. Additionally, extended documentation for copying project structure.
- _0.2.5_ Lowered required CMake-version to support some more LTS-systems.
- _0.2.4_ Fixed problem with install via `pip` because it ships without tests.
- _0.2.3_ `--build=missing` for conan. Why didn't the CI complain before?
- _0.2.2_ Some improvements regarding large numbers.
- _0.2.1_ Conan is now called directly via `python -m`, in case python modules are not imported to PATH.
- _0.2.0_ Can now be installed with `pip install cgshop2023-pyutils` on most machines!
- _0.1.3_ Solution iterator, installable via pip.
- _0.1.2_ Support for large numbers. Some further simplification.
- _0.1.1_ Some code simplification.
- _0.1.0_ Initial version.
