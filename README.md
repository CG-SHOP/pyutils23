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

This python package has a native core, which requires a plattform specific compilation.
Thanks to [conan](https://conan.io/) and [scikit-build](https://scikit-build.readthedocs.io/en/latest/),
it is relatively easy to build and install the package on nearly every system.

You need to have `gcc` and `cmake` installed on your system. This is probably already
the case. If you are using a `conda` environment, you may need to install `gcc` within
this environment, because, e.g., the `glibc` of `conda` can be incompatible with your system's
`glibc`.

If `gcc` and `cmake` are installed, just switch into your python environment (optional,
but recommended), check out this repository, and run

```shell
pip install .
```

Afterwards, you can delete the repository from your files because all files you need
have been copied to Python's package folder. We are working on making the
package installable directly from PyPI.

If anything goes wrong, please open an issue or write us a mail.

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

- _0.1.3_ Solution iterator, installable via pip.
- _0.1.2_ Support for large numbers. Some further simplification.
- _0.1.1_ Some code simplification.
- _0.1.0_ Initial version.
