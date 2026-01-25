"""Highlight markers for algorithm visualization.

These ASCII markers are embedded in rendered output to indicate
the state of each element during algorithm execution. The UI layer
converts these markers to styled Rich text.
"""

from __future__ import annotations

from dsa_visualizer.algorithms.types import HighlightContext, TreeHighlightContext


# Marker characters for different highlight states
MARKER_CURRENT = "→"
"""Points to the element currently being examined."""

MARKER_VISITED = "·"
"""Indicates an element that has already been visited."""

MARKER_FOUND = "✓"
"""Indicates the element where a match was found."""

MARKER_COMPARING = "?"
"""Indicates an element being compared."""

MARKER_ELIMINATED = "×"
"""Indicates an element that has been ruled out."""

MARKER_BOUNDARY_L = "["
"""Left boundary marker for search range."""

MARKER_BOUNDARY_R = "]"
"""Right boundary marker for search range."""


def get_index_marker(index: int, highlights: HighlightContext) -> str:
    """Get the appropriate marker for an index based on highlight context.

    Priority (highest to lowest):
    1. Found (✓) - most important, search is complete
    2. Current (→) - currently being examined
    3. Comparing (?) - being compared
    4. Visited (·) - already processed
    5. Eliminated (×) - ruled out
    6. None ("") - no special state

    Args:
        index: The array index to get marker for.
        highlights: The current highlight context.

    Returns:
        The marker string for this index, or empty string if none.
    """
    if index in highlights.found:
        return MARKER_FOUND
    if index in highlights.current:
        return MARKER_CURRENT
    if index in highlights.comparing:
        return MARKER_COMPARING
    if index in highlights.visited:
        return MARKER_VISITED
    if index in highlights.eliminated:
        return MARKER_ELIMINATED
    return ""


def is_at_left_boundary(index: int, highlights: HighlightContext) -> bool:
    """Check if index is at the left search boundary."""
    if highlights.boundaries is None:
        return False
    return index == highlights.boundaries[0]


def is_at_right_boundary(index: int, highlights: HighlightContext) -> bool:
    """Check if index is at the right search boundary."""
    if highlights.boundaries is None:
        return False
    return index == highlights.boundaries[1]


def is_in_search_range(index: int, highlights: HighlightContext) -> bool:
    """Check if index is within the current search range."""
    if highlights.boundaries is None:
        return True  # No boundaries means all indices are valid
    low, high = highlights.boundaries
    return low <= index <= high


def get_node_marker(node: object, highlights: TreeHighlightContext) -> str:
    """Get the appropriate marker for a tree node based on highlight context.

    Priority (highest to lowest):
    1. Found (✓) - search is complete, target found
    2. Current (→) - currently being examined
    3. Comparing (?) - being compared
    4. In path (·) - part of the traversal path
    5. Visited (·) - already processed
    6. None ("") - no special state

    Args:
        node: The tree node to get marker for.
        highlights: The current tree highlight context.

    Returns:
        The marker string for this node, or empty string if none.
    """
    node_id = id(node)

    if highlights.found_node == node_id:
        return MARKER_FOUND
    if highlights.current_node == node_id:
        return MARKER_CURRENT
    if highlights.comparing_node == node_id:
        return MARKER_COMPARING
    if node_id in highlights.path_nodes:
        return MARKER_VISITED
    if node_id in highlights.visited_nodes:
        return MARKER_VISITED
    return ""
