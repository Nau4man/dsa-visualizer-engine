"""Depth-First Search for binary trees.

DFS explores as far as possible along each branch before backtracking.
This implementation uses pre-order traversal (root, left, right).

Time Complexity: O(n) where n is the number of nodes
Space Complexity: O(h) where h is the height of the tree (recursion stack)
"""

from __future__ import annotations

from collections.abc import Iterator

from dsa_visualizer.algorithms.types import AlgorithmStep, TreeHighlightContext


def dfs_search(root: object | None, target: object) -> Iterator[AlgorithmStep]:
    """Search for a target value in a binary tree using DFS.

    Uses pre-order traversal: visits root, then left subtree, then right subtree.

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
    path: list[int] = []

    # Use iterative DFS with explicit stack
    stack: list[object] = [root]

    while stack:
        node = stack.pop()
        node_id = id(node)
        node_value = _get_value(node)

        step_number += 1
        path.append(node_id)

        # Yield step for examining this node
        yield AlgorithmStep(
            step_number=step_number,
            action=f"Visit node with value {node_value}, compare with target {target}",
            highlights=TreeHighlightContext(
                current_node=node_id,
                visited_nodes=frozenset(visited),
                path_nodes=tuple(path),
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
                    path_nodes=tuple(path),
                ),
                data=root,
                is_complete=True,
                result=node,
            )
            return

        visited.add(node_id)

        # Add children to stack (right first so left is processed first)
        right = getattr(node, "right", None)
        left = getattr(node, "left", None)

        if right is not None:
            stack.append(right)
        if left is not None:
            stack.append(left)

        # When backtracking (no more children or dead end), update path
        if left is None and right is None:
            # Backtrack: find the last node in path that still has unvisited children
            while path:
                # Check if we need to keep this node in path
                if _has_unvisited_children_in_stack(stack, path):
                    break
                path.pop()

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


def dfs_traversal(root: object | None) -> Iterator[AlgorithmStep]:
    """Traverse all nodes in a binary tree using DFS (pre-order).

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

    # Use iterative DFS with explicit stack
    stack: list[object] = [root]

    while stack:
        node = stack.pop()
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

        # Add children to stack (right first so left is processed first)
        right = getattr(node, "right", None)
        left = getattr(node, "left", None)

        if right is not None:
            stack.append(right)
        if left is not None:
            stack.append(left)

    # Traversal complete
    step_number += 1
    yield AlgorithmStep(
        step_number=step_number,
        action=f"DFS traversal complete. Order: {traversal_order}",
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


def _has_unvisited_children_in_stack(stack: list[object], path: list[int]) -> bool:
    """Check if any node in the stack is a descendant of a path node."""
    path_set = set(path)
    for node in stack:
        if id(node) in path_set:
            return True
    return False
