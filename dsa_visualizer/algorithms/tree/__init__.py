"""Tree search and traversal algorithms.

Includes:
- dfs_search - Depth-First Search (find value)
- dfs_traversal - Depth-First Traversal (visit all nodes)
- bfs_search - Breadth-First Search (find value)
- bfs_traversal - Breadth-First Traversal (visit all nodes)
- bst_search - Binary Search Tree lookup
"""

from dsa_visualizer.algorithms.tree.dfs import dfs_search, dfs_traversal
from dsa_visualizer.algorithms.tree.bfs import bfs_search, bfs_traversal
from dsa_visualizer.algorithms.tree.bst_search import bst_search

__all__ = [
    "dfs_search",
    "dfs_traversal",
    "bfs_search",
    "bfs_traversal",
    "bst_search",
]
