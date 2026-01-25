"""Algorithm visualization module for DSA Visualizer.

This module provides step-by-step algorithm visualization with highlighting
support for educational purposes.
"""

from dsa_visualizer.algorithms.types import (
    AlgorithmStep,
    HighlightContext,
    TreeHighlightContext,
)
from dsa_visualizer.algorithms.runner import AlgorithmRunner

__all__ = [
    "AlgorithmStep",
    "HighlightContext",
    "TreeHighlightContext",
    "AlgorithmRunner",
]
