"""Search algorithms for arrays and sequences.

Algorithms are ordered from least efficient to most efficient:
1. linear_search - O(n)
2. binary_search - O(log n)
3. jump_search - O(sqrt(n))
4. interpolation_search - O(log log n) average
5. exponential_search - O(log n)
"""

from dsa_visualizer.algorithms.search.linear import linear_search
from dsa_visualizer.algorithms.search.binary import binary_search
from dsa_visualizer.algorithms.search.jump import jump_search
from dsa_visualizer.algorithms.search.interpolation import interpolation_search
from dsa_visualizer.algorithms.search.exponential import exponential_search

__all__ = [
    "linear_search",
    "binary_search",
    "jump_search",
    "interpolation_search",
    "exponential_search",
]
