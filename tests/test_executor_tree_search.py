"""Tests for tree search functionality in Executor."""

from dsa_visualizer.core.executor import Executor


class TestTreeSearch:
    """Tests for tree_search function."""

    def test_dfs_search_creates_pending_algorithm(self):
        """tree_search with dfs creates pending algorithm."""
        executor = Executor()
        executor.execute("tree = BinaryTree([10, 5, 15])")
        executor.execute("tree_search('dfs', tree, 5)")

        pending = executor.pop_pending_algorithm()
        assert pending is not None
        assert pending.runner.name == "Depth-First Search"

    def test_bfs_search_creates_pending_algorithm(self):
        """tree_search with bfs creates pending algorithm."""
        executor = Executor()
        executor.execute("tree = BinaryTree([10, 5, 15])")
        executor.execute("tree_search('bfs', tree, 5)")

        pending = executor.pop_pending_algorithm()
        assert pending is not None
        assert pending.runner.name == "Breadth-First Search"

    def test_bst_search_creates_pending_algorithm(self):
        """tree_search with bst creates pending algorithm."""
        executor = Executor()
        executor.execute("tree = BinarySearchTree([10, 5, 15])")
        executor.execute("tree_search('bst', tree, 5)")

        pending = executor.pop_pending_algorithm()
        assert pending is not None
        assert pending.runner.name == "BST Search"

    def test_tree_search_case_insensitive(self):
        """tree_search algorithm name is case insensitive."""
        executor = Executor()
        executor.execute("tree = BinaryTree([10, 5, 15])")
        executor.execute("tree_search('DFS', tree, 5)")

        pending = executor.pop_pending_algorithm()
        assert pending is not None

    def test_tree_search_unknown_algorithm(self):
        """tree_search raises error for unknown algorithm."""
        executor = Executor()
        executor.execute("tree = BinaryTree([10, 5, 15])")
        result = executor.execute("tree_search('unknown', tree, 5)")

        assert not result.ok
        assert "Unknown algorithm" in result.error

    def test_tree_search_returns_status_message(self):
        """tree_search returns a status message."""
        executor = Executor()
        executor.execute("tree = BinaryTree([10, 5, 15])")
        executor.execute("msg = tree_search('dfs', tree, 5)")

        assert "Starting" in executor.globals.get("msg", "")


class TestTreeTraverse:
    """Tests for tree_traverse function."""

    def test_dfs_traversal_creates_pending_algorithm(self):
        """tree_traverse with dfs creates pending algorithm."""
        executor = Executor()
        executor.execute("tree = BinaryTree([10, 5, 15])")
        executor.execute("tree_traverse('dfs', tree)")

        pending = executor.pop_pending_algorithm()
        assert pending is not None
        assert "Depth-First Search" in pending.runner.name
        assert "Traversal" in pending.runner.name

    def test_bfs_traversal_creates_pending_algorithm(self):
        """tree_traverse with bfs creates pending algorithm."""
        executor = Executor()
        executor.execute("tree = BinaryTree([10, 5, 15])")
        executor.execute("tree_traverse('bfs', tree)")

        pending = executor.pop_pending_algorithm()
        assert pending is not None
        assert "Breadth-First Search" in pending.runner.name
        assert "Traversal" in pending.runner.name

    def test_tree_traverse_case_insensitive(self):
        """tree_traverse algorithm name is case insensitive."""
        executor = Executor()
        executor.execute("tree = BinaryTree([10, 5, 15])")
        executor.execute("tree_traverse('BFS', tree)")

        pending = executor.pop_pending_algorithm()
        assert pending is not None

    def test_tree_traverse_unknown_algorithm(self):
        """tree_traverse raises error for unknown algorithm."""
        executor = Executor()
        executor.execute("tree = BinaryTree([10, 5, 15])")
        result = executor.execute("tree_traverse('unknown', tree)")

        assert not result.ok
        assert "Unknown algorithm" in result.error

    def test_tree_traverse_returns_status_message(self):
        """tree_traverse returns a status message."""
        executor = Executor()
        executor.execute("tree = BinaryTree([10, 5, 15])")
        executor.execute("msg = tree_traverse('dfs', tree)")

        assert "Starting" in executor.globals.get("msg", "")

