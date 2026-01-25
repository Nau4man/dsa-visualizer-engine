"""Tests for DFS tree search algorithm."""

from dsa_visualizer.algorithms.tree.dfs import dfs_search, dfs_traversal
from dsa_visualizer.data_structures.implementations.structures import BinaryTree


class TestDFSSearch:
    """Tests for dfs_search function."""

    def test_empty_tree(self):
        """DFS on empty tree yields single complete step."""
        steps = list(dfs_search(None, 10))
        assert len(steps) == 1
        assert steps[0].is_complete
        assert steps[0].result is None
        assert "empty" in steps[0].action.lower()

    def test_single_node_found(self):
        """DFS finds target in single-node tree."""
        tree = BinaryTree()
        tree.insert(10)

        steps = list(dfs_search(tree.root, 10))
        assert len(steps) == 2  # Visit + Found
        assert steps[-1].is_complete
        assert steps[-1].result is tree.root
        assert "Found" in steps[-1].action

    def test_single_node_not_found(self):
        """DFS reports not found in single-node tree."""
        tree = BinaryTree()
        tree.insert(10)

        steps = list(dfs_search(tree.root, 99))
        assert len(steps) == 2  # Visit + Not found
        assert steps[-1].is_complete
        assert steps[-1].result is None
        assert "not found" in steps[-1].action.lower()

    def test_finds_root(self):
        """DFS finds target at root."""
        tree = BinaryTree()
        tree.insert(10)
        tree.insert(5)
        tree.insert(15)

        steps = list(dfs_search(tree.root, 10))
        final_step = steps[-1]
        assert final_step.is_complete
        assert final_step.result is tree.root

    def test_finds_left_child(self):
        """DFS finds target in left subtree."""
        tree = BinaryTree()
        tree.insert(10)
        tree.insert(5)
        tree.insert(15)

        steps = list(dfs_search(tree.root, 5))
        final_step = steps[-1]
        assert final_step.is_complete
        assert final_step.result is tree.root.left

    def test_finds_right_child(self):
        """DFS finds target in right subtree."""
        tree = BinaryTree()
        tree.insert(10)
        tree.insert(5)
        tree.insert(15)

        steps = list(dfs_search(tree.root, 15))
        final_step = steps[-1]
        assert final_step.is_complete
        assert final_step.result is tree.root.right

    def test_preorder_traversal_order(self):
        """DFS visits nodes in pre-order (root, left, right)."""
        tree = BinaryTree()
        # Build a tree:
        #       10
        #      /  \
        #     5    15
        tree.insert(10)
        tree.insert(5)
        tree.insert(15)

        # Search for non-existent value to force full traversal
        steps = list(dfs_search(tree.root, 99))

        # Extract visited values from actions
        visited_values = []
        for step in steps:
            if "Visit node" in step.action:
                # Extract value from action like "Visit node with value 10, ..."
                action = step.action
                value_str = action.split("value ")[1].split(",")[0]
                visited_values.append(int(value_str))

        # Pre-order: root (10), left (5), right (15)
        assert visited_values == [10, 5, 15]

    def test_deep_tree(self):
        """DFS works on deeper trees."""
        tree = BinaryTree()
        # Build:
        #       10
        #      /  \
        #     5    15
        #    /      \
        #   3       20
        tree.insert(10)
        tree.insert(5)
        tree.insert(15)
        tree.insert(3)
        tree.insert(20)

        steps = list(dfs_search(tree.root, 3))
        final_step = steps[-1]
        assert final_step.is_complete
        assert final_step.result is tree.root.left.left

    def test_highlights_current_node(self):
        """DFS highlights current node being examined."""
        tree = BinaryTree()
        tree.insert(10)
        tree.insert(5)

        steps = list(dfs_search(tree.root, 5))

        # First step should highlight root as current
        assert steps[0].highlights.current_node == id(tree.root)

    def test_highlights_visited_nodes(self):
        """DFS tracks visited nodes in highlights."""
        tree = BinaryTree()
        tree.insert(10)
        tree.insert(5)
        tree.insert(15)

        steps = list(dfs_search(tree.root, 99))

        # Final step should have all nodes as visited
        final_highlights = steps[-1].highlights
        assert id(tree.root) in final_highlights.visited_nodes
        assert id(tree.root.left) in final_highlights.visited_nodes
        assert id(tree.root.right) in final_highlights.visited_nodes

    def test_highlights_found_node(self):
        """DFS highlights found node when target is located."""
        tree = BinaryTree()
        tree.insert(10)
        tree.insert(5)

        steps = list(dfs_search(tree.root, 5))

        final_step = steps[-1]
        assert final_step.highlights.found_node == id(tree.root.left)

    def test_step_numbers_are_sequential(self):
        """Step numbers are sequential starting from 1."""
        tree = BinaryTree()
        tree.insert(10)
        tree.insert(5)
        tree.insert(15)

        steps = list(dfs_search(tree.root, 99))
        for i, step in enumerate(steps, 1):
            assert step.step_number == i

    def test_data_is_root(self):
        """Each step's data is the tree root."""
        tree = BinaryTree()
        tree.insert(10)
        tree.insert(5)

        steps = list(dfs_search(tree.root, 5))
        for step in steps:
            if step.data is not None:
                assert step.data is tree.root


class TestDFSTraversal:
    """Tests for dfs_traversal function."""

    def test_empty_tree(self):
        """Traversal of empty tree yields single complete step."""
        steps = list(dfs_traversal(None))
        assert len(steps) == 1
        assert steps[0].is_complete
        assert steps[0].result == []

    def test_single_node(self):
        """Traversal of single node tree."""
        tree = BinaryTree()
        tree.insert(10)

        steps = list(dfs_traversal(tree.root))
        final_step = steps[-1]
        assert final_step.is_complete
        assert final_step.result == [10]

    def test_preorder_result(self):
        """Traversal returns values in pre-order."""
        tree = BinaryTree()
        tree.insert(10)
        tree.insert(5)
        tree.insert(15)
        tree.insert(3)
        tree.insert(7)

        steps = list(dfs_traversal(tree.root))
        final_step = steps[-1]
        assert final_step.is_complete
        # Pre-order: 10, 5, 3, 7, 15
        assert final_step.result == [10, 5, 3, 7, 15]

    def test_all_nodes_visited(self):
        """Traversal visits all nodes."""
        tree = BinaryTree()
        tree.insert(10)
        tree.insert(5)
        tree.insert(15)

        steps = list(dfs_traversal(tree.root))
        final_step = steps[-1]

        assert id(tree.root) in final_step.highlights.visited_nodes
        assert id(tree.root.left) in final_step.highlights.visited_nodes
        assert id(tree.root.right) in final_step.highlights.visited_nodes

    def test_highlights_current_during_traversal(self):
        """Traversal highlights current node at each step."""
        tree = BinaryTree()
        tree.insert(10)
        tree.insert(5)

        steps = list(dfs_traversal(tree.root))

        # Non-final steps should have current_node set
        for step in steps[:-1]:
            assert step.highlights.current_node is not None

