from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class HighlightContext:
    """Describes what elements should be highlighted in visualization.

    All index sets use array indices. For tree-based algorithms,
    use TreeHighlightContext instead.
    """

    current: frozenset[int] = field(default_factory=frozenset)
    """Indices currently being examined."""

    comparing: frozenset[int] = field(default_factory=frozenset)
    """Indices being compared."""

    visited: frozenset[int] = field(default_factory=frozenset)
    """Indices already visited/processed."""

    found: frozenset[int] = field(default_factory=frozenset)
    """Indices where a match was found."""

    eliminated: frozenset[int] = field(default_factory=frozenset)
    """Indices ruled out (e.g., binary search elimination)."""

    boundaries: tuple[int, int] | None = None
    """Search range boundaries (low, high) if applicable."""


@dataclass(frozen=True)
class TreeHighlightContext:
    """Describes what nodes should be highlighted in tree visualization.

    Uses Python object IDs to identify nodes rather than indices.
    """

    current_node: int | None = None
    """Python id() of the node currently being examined."""

    visited_nodes: frozenset[int] = field(default_factory=frozenset)
    """Python id() values of nodes already visited."""

    found_node: int | None = None
    """Python id() of the node where target was found."""

    path_nodes: tuple[int, ...] = ()
    """Python id() values of nodes in the current path (for traversal visualization)."""

    comparing_node: int | None = None
    """Python id() of node being compared."""


@dataclass(frozen=True)
class AlgorithmStep:
    """A single step in algorithm execution.

    Each step represents a meaningful operation that helps understand
    how the algorithm works (e.g., "Compare arr[3] with target").
    """

    step_number: int
    """1-indexed step count."""

    action: str
    """Human-readable description of this step."""

    highlights: HighlightContext
    """What to highlight in the visualization."""

    data: list | object
    """Current state of the data being operated on."""

    is_complete: bool = False
    """True if the algorithm has finished."""

    result: object | None = None
    """Final result (only meaningful when is_complete=True)."""
