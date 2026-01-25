"""Breadth-First Search for binary trees.

BFS explores nodes level by level, visiting all nodes at the current depth
before moving to nodes at the next depth level.

Time Complexity: O(n) where n is the number of nodes
Space Complexity: O(w) where w is the maximum width of the tree
"""

from __future__ import annotations

from collections import deque
from collections.abc import Iterator

from dsa_visualizer.algorithms.types import AlgorithmStep, TreeHighlightContext


def bfs_search(root: object | None, target: object) -> Iterator[AlgorithmStep]:
    """Search for a target value in a binary tree using BFS.

    Visits nodes level by level from top to bottom, left to right.

    Args:
        root: Root node of the tree (must have .value or .data, .left, .right attributes).
        target: Value to search for.

    Yields:
        AlgorithmStep objects showing the search progress.
    """
    if root is None:
        yield AlgorithmStep(
            step_number=1,
            action="Tree is empty - nothing to search",
            highlights=TreeHighlightContext(),
            data=None,
            is_complete=True,
            result=None,
        )
        return

    step_number = 0
    visited: set[int] = set()

    # Use queue for BFS
    queue: deque[object] = deque([root])

    while queue:
        node = queue.popleft()
        node_id = id(node)
        node_value = _get_value(node)

        step_number += 1

        # Yield step for examining this node
        yield AlgorithmStep(
            step_number=step_number,
            action=f"Visit node with value {node_value}, compare with target {target}",
            highlights=TreeHighlightContext(
                current_node=node_id,
                visited_nodes=frozenset(visited),
                comparing_node=node_id,
            ),
            data=root,
            is_complete=False,
            result=None,
        )

        # Check if we found the target
        if node_value == target:
            step_number += 1
            yield AlgorithmStep(
                step_number=step_number,
                action=f"Found target {target}!",
                highlights=TreeHighlightContext(
                    found_node=node_id,
                    visited_nodes=frozenset(visited),
                ),
                data=root,
                is_complete=True,
                result=node,
            )
            return

        visited.add(node_id)

        # Add children to queue (left first, then right)
        left = getattr(node, "left", None)
        right = getattr(node, "right", None)

        if left is not None:
            queue.append(left)
        if right is not None:
            queue.append(right)

    # Target not found
    step_number += 1
    yield AlgorithmStep(
        step_number=step_number,
        action=f"Target {target} not found in tree",
        highlights=TreeHighlightContext(
            visited_nodes=frozenset(visited),
        ),
        data=root,
        is_complete=True,
        result=None,
    )


def bfs_traversal(root: object | None) -> Iterator[AlgorithmStep]:
    """Traverse all nodes in a binary tree using BFS (level-order).

    Args:
        root: Root node of the tree.

    Yields:
        AlgorithmStep objects showing the traversal progress.
    """
    if root is None:
        yield AlgorithmStep(
            step_number=1,
            action="Tree is empty - nothing to traverse",
            highlights=TreeHighlightContext(),
            data=None,
            is_complete=True,
            result=[],
        )
        return

    step_number = 0
    visited: set[int] = set()
    traversal_order: list[object] = []

    # Use queue for BFS
    queue: deque[object] = deque([root])

    while queue:
        node = queue.popleft()
        node_id = id(node)
        node_value = _get_value(node)

        step_number += 1
        visited.add(node_id)
        traversal_order.append(node_value)

        # Yield step for visiting this node
        yield AlgorithmStep(
            step_number=step_number,
            action=f"Visit node with value {node_value}",
            highlights=TreeHighlightContext(
                current_node=node_id,
                visited_nodes=frozenset(visited),
            ),
            data=root,
            is_complete=False,
            result=None,
        )

        # Add children to queue (left first, then right)
        left = getattr(node, "left", None)
        right = getattr(node, "right", None)

        if left is not None:
            queue.append(left)
        if right is not None:
            queue.append(right)

    # Traversal complete
    step_number += 1
    yield AlgorithmStep(
        step_number=step_number,
        action=f"BFS traversal complete. Order: {traversal_order}",
        highlights=TreeHighlightContext(
            visited_nodes=frozenset(visited),
        ),
        data=root,
        is_complete=True,
        result=traversal_order,
    )


def _get_value(node: object) -> object:
    """Get the value from a tree node."""
    if hasattr(node, "value"):
        return getattr(node, "value")
    return getattr(node, "data")
