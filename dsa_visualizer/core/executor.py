from __future__ import annotations

from collections.abc import Callable, Iterator
from dataclasses import dataclass
from typing import Any

from dsa_visualizer.algorithms.runner import AlgorithmRunner
from dsa_visualizer.algorithms.search.binary import binary_search
from dsa_visualizer.algorithms.search.exponential import exponential_search
from dsa_visualizer.algorithms.search.interpolation import interpolation_search
from dsa_visualizer.algorithms.search.jump import jump_search
from dsa_visualizer.algorithms.search.linear import linear_search
from dsa_visualizer.algorithms.tree.bfs import bfs_search, bfs_traversal
from dsa_visualizer.algorithms.tree.bst_search import bst_search
from dsa_visualizer.algorithms.tree.dfs import dfs_search, dfs_traversal
from dsa_visualizer.algorithms.types import AlgorithmStep
from dsa_visualizer.data_structures.implementations.structures import (
    BinarySearchTree,
    BinaryTree,
    DoublyLinkedList,
    Graph,
    LinkedList,
    MinHeap,
    Queue,
    Stack,
)


# Registry of available search algorithms
SEARCH_ALGORITHMS: dict[str, Callable[[list, Any], Iterator[AlgorithmStep]]] = {
    "linear": linear_search,
    "binary": binary_search,
    "jump": jump_search,
    "interpolation": interpolation_search,
    "exponential": exponential_search,
}

# Algorithm display names
ALGORITHM_NAMES: dict[str, str] = {
    "linear": "Linear Search",
    "binary": "Binary Search",
    "jump": "Jump Search",
    "interpolation": "Interpolation Search",
    "exponential": "Exponential Search",
}

# Registry of available tree search algorithms
TREE_SEARCH_ALGORITHMS: dict[str, Callable[[object, Any], Iterator[AlgorithmStep]]] = {
    "dfs": dfs_search,
    "bfs": bfs_search,
    "bst": bst_search,
}

# Tree traversal algorithms (no target needed)
TREE_TRAVERSAL_ALGORITHMS: dict[str, Callable[[object], Iterator[AlgorithmStep]]] = {
    "dfs": dfs_traversal,
    "bfs": bfs_traversal,
}

# Tree algorithm display names
TREE_ALGORITHM_NAMES: dict[str, str] = {
    "dfs": "Depth-First Search",
    "bfs": "Breadth-First Search",
    "bst": "BST Search",
}


@dataclass(frozen=True)
class ExecutionResult:
    ok: bool
    error: str | None = None


@dataclass
class PendingAlgorithm:
    """Stores info about an algorithm ready to run."""

    runner: AlgorithmRunner
    data: object  # Can be list (array) or tree root node


# Built-in example datasets
EXAMPLE_ARRAYS: dict[str, list] = {
    "small": [1, 3, 5, 7, 9],
    "medium": [2, 4, 8, 16, 32, 64, 128, 256],
    "large": [1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80],
    "unsorted": [42, 17, 8, 91, 33, 56, 24],
    "duplicates": [1, 2, 2, 3, 3, 3, 4, 4, 4, 4],
}

EXAMPLE_TREES: dict[str, list] = {
    "balanced": [50, 25, 75, 12, 37, 62, 87],
    "small": [10, 5, 15],
    "left_heavy": [50, 40, 30, 20, 10],
    "right_heavy": [10, 20, 30, 40, 50],
}


class Executor:
    def __init__(self) -> None:
        self.globals: dict[str, object] = {
            "LinkedList": LinkedList,
            "DoublyLinkedList": DoublyLinkedList,
            "Stack": Stack,
            "Queue": Queue,
            "BinaryTree": BinaryTree,
            "BinarySearchTree": BinarySearchTree,
            "MinHeap": MinHeap,
            "Graph": Graph,
        }
        self.pending_algorithm: PendingAlgorithm | None = None

        # Add search functions to globals
        self.globals["search"] = self._create_search_function()
        self.globals["tree_search"] = self._create_tree_search_function()
        self.globals["tree_traverse"] = self._create_tree_traverse_function()

        # Add example datasets
        self.globals["EXAMPLES"] = {
            "arrays": {k: list(v) for k, v in EXAMPLE_ARRAYS.items()},
            "trees": {k: list(v) for k, v in EXAMPLE_TREES.items()},
        }

    def _create_search_function(self) -> Callable:
        """Create the search function that users call."""

        def search(algorithm: str, data: list, target: object) -> str:
            """Start a search algorithm visualization.

            Args:
                algorithm: Algorithm name ("linear", "binary", etc.)
                data: The array to search in.
                target: The value to find.

            Returns:
                Status message.
            """
            algorithm_lower = algorithm.lower()
            if algorithm_lower not in SEARCH_ALGORITHMS:
                available = ", ".join(sorted(SEARCH_ALGORITHMS.keys()))
                raise ValueError(
                    f"Unknown algorithm: {algorithm!r}. "
                    f"Available: {available}"
                )

            # Get algorithm generator
            algo_func = SEARCH_ALGORITHMS[algorithm_lower]
            generator = algo_func(list(data), target)

            # Create runner
            name = ALGORITHM_NAMES.get(algorithm_lower, algorithm)
            runner = AlgorithmRunner.from_generator(name, generator)

            # Store for app to pick up
            self.pending_algorithm = PendingAlgorithm(runner=runner, data=list(data))

            return f"Starting {name} for target {target!r}..."

        return search

    def _create_tree_search_function(self) -> Callable:
        """Create the tree_search function that users call."""

        def tree_search(algorithm: str, tree: object, target: object) -> str:
            """Start a tree search algorithm visualization.

            Args:
                algorithm: Algorithm name ("dfs", "bfs", "bst")
                tree: The tree to search in (BinaryTree or BinarySearchTree).
                target: The value to find.

            Returns:
                Status message.
            """
            algorithm_lower = algorithm.lower()
            if algorithm_lower not in TREE_SEARCH_ALGORITHMS:
                available = ", ".join(sorted(TREE_SEARCH_ALGORITHMS.keys()))
                raise ValueError(
                    f"Unknown algorithm: {algorithm!r}. "
                    f"Available: {available}"
                )

            # Get the root node from the tree object
            root = getattr(tree, "root", tree)

            # Get algorithm generator
            algo_func = TREE_SEARCH_ALGORITHMS[algorithm_lower]
            generator = algo_func(root, target)

            # Create runner
            name = TREE_ALGORITHM_NAMES.get(algorithm_lower, algorithm)
            runner = AlgorithmRunner.from_generator(name, generator)

            # Store for app to pick up
            self.pending_algorithm = PendingAlgorithm(runner=runner, data=root)

            return f"Starting {name} for target {target!r}..."

        return tree_search

    def _create_tree_traverse_function(self) -> Callable:
        """Create the tree_traverse function that users call."""

        def tree_traverse(algorithm: str, tree: object) -> str:
            """Start a tree traversal algorithm visualization.

            Args:
                algorithm: Algorithm name ("dfs", "bfs")
                tree: The tree to traverse (BinaryTree or BinarySearchTree).

            Returns:
                Status message.
            """
            algorithm_lower = algorithm.lower()
            if algorithm_lower not in TREE_TRAVERSAL_ALGORITHMS:
                available = ", ".join(sorted(TREE_TRAVERSAL_ALGORITHMS.keys()))
                raise ValueError(
                    f"Unknown algorithm: {algorithm!r}. "
                    f"Available: {available}"
                )

            # Get the root node from the tree object
            root = getattr(tree, "root", tree)

            # Get algorithm generator
            algo_func = TREE_TRAVERSAL_ALGORITHMS[algorithm_lower]
            generator = algo_func(root)

            # Create runner
            name = f"{TREE_ALGORITHM_NAMES.get(algorithm_lower, algorithm)} Traversal"
            runner = AlgorithmRunner.from_generator(name, generator)

            # Store for app to pick up
            self.pending_algorithm = PendingAlgorithm(runner=runner, data=root)

            return f"Starting {name}..."

        return tree_traverse

    def execute(self, source: str) -> ExecutionResult:
        # Clear any pending algorithm before execution
        self.pending_algorithm = None

        try:
            compiled = compile(source, "<input>", "exec")
            exec(compiled, self.globals)
        except Exception as exc:  # noqa: BLE001 - surface error message to user
            return ExecutionResult(False, str(exc))
        return ExecutionResult(True, None)

    def pop_pending_algorithm(self) -> PendingAlgorithm | None:
        """Get and clear any pending algorithm."""
        pending = self.pending_algorithm
        self.pending_algorithm = None
        return pending
