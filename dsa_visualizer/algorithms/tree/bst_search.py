"""Binary Search Tree lookup algorithm.

BST search exploits the BST property: for every node, all values in the
left subtree are less than the node's value, and all values in the right
subtree are greater.

Time Complexity: O(h) where h is the height of the tree
  - O(log n) for balanced trees
  - O(n) for skewed trees
Space Complexity: O(1) for iterative, O(h) for recursive
"""

from __future__ import annotations

from collections.abc import Iterator

from dsa_visualizer.algorithms.types import AlgorithmStep, TreeHighlightContext


def bst_search(root: object | None, target: object) -> Iterator[AlgorithmStep]:
    """Search for a target value in a Binary Search Tree.

    Uses the BST property to eliminate half the remaining tree at each step.
    Requires values to be comparable (support < and > operators).

    Args:
        root: Root node of the BST (must have .value or .data, .left, .right attributes).
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
    node = root

    while node is not None:
        node_id = id(node)
        node_value = _get_value(node)
        path.append(node_id)

        step_number += 1

        # Determine comparison result and next direction
        if node_value == target:
            # Found the target
            yield AlgorithmStep(
                step_number=step_number,
                action=f"Compare {target} with {node_value}: Equal - Found target!",
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

        if target < node_value:
            # Go left
            direction = "left"
            next_node = getattr(node, "left", None)
            action = f"Compare {target} with {node_value}: {target} < {node_value}, go left"
        else:
            # Go right
            direction = "right"
            next_node = getattr(node, "right", None)
            action = f"Compare {target} with {node_value}: {target} > {node_value}, go right"

        yield AlgorithmStep(
            step_number=step_number,
            action=action,
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

        if next_node is None:
            # Dead end - target not in tree
            step_number += 1
            yield AlgorithmStep(
                step_number=step_number,
                action=f"No {direction} child - target {target} not found in tree",
                highlights=TreeHighlightContext(
                    visited_nodes=frozenset(visited),
                    path_nodes=tuple(path),
                ),
                data=root,
                is_complete=True,
                result=None,
            )
            return

        node = next_node

    # Should not reach here, but handle edge case
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


def _get_value(node: object) -> object:
    """Get the value from a tree node."""
    if hasattr(node, "value"):
        return getattr(node, "value")
    return getattr(node, "data")
