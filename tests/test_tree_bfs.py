"""Tests for BFS tree search algorithm."""

from dsa_visualizer.algorithms.tree.bfs import bfs_search, bfs_traversal
from dsa_visualizer.data_structures.implementations.structures import BinaryTree


class TestBFSSearch:
    """Tests for bfs_search function."""

    def test_empty_tree(self):
        """BFS on empty tree yields single complete step."""
        steps = list(bfs_search(None, 10))
        assert len(steps) == 1
        assert steps[0].is_complete
        assert steps[0].result is None
        assert "empty" in steps[0].action.lower()

    def test_single_node_found(self):
        """BFS finds target in single-node tree."""
        tree = BinaryTree()
        tree.insert(10)

        steps = list(bfs_search(tree.root, 10))
        assert len(steps) == 2  # Visit + Found
        assert steps[-1].is_complete
        assert steps[-1].result is tree.root
        assert "Found" in steps[-1].action

    def test_single_node_not_found(self):
        """BFS reports not found in single-node tree."""
        tree = BinaryTree()
        tree.insert(10)

        steps = list(bfs_search(tree.root, 99))
        assert len(steps) == 2  # Visit + Not found
        assert steps[-1].is_complete
        assert steps[-1].result is None
        assert "not found" in steps[-1].action.lower()

    def test_finds_root(self):
        """BFS finds target at root."""
        tree = BinaryTree()
        tree.insert(10)
        tree.insert(5)
        tree.insert(15)

        steps = list(bfs_search(tree.root, 10))
        final_step = steps[-1]
        assert final_step.is_complete
        assert final_step.result is tree.root

    def test_finds_left_child(self):
        """BFS finds target in left child."""
        tree = BinaryTree()
        tree.insert(10)
        tree.insert(5)
        tree.insert(15)

        steps = list(bfs_search(tree.root, 5))
        final_step = steps[-1]
        assert final_step.is_complete
        assert final_step.result is tree.root.left

    def test_finds_right_child(self):
        """BFS finds target in right child."""
        tree = BinaryTree()
        tree.insert(10)
        tree.insert(5)
        tree.insert(15)

        steps = list(bfs_search(tree.root, 15))
        final_step = steps[-1]
        assert final_step.is_complete
        assert final_step.result is tree.root.right

    def test_levelorder_traversal_order(self):
        """BFS visits nodes level by level, left to right."""
        tree = BinaryTree()
        # Build a tree:
        #       10
        #      /  \
        #     5    15
        #    / \
        #   3   7
        tree.insert(10)
        tree.insert(5)
        tree.insert(15)
        tree.insert(3)
        tree.insert(7)

        # Search for non-existent value to force full traversal
        steps = list(bfs_search(tree.root, 99))

        # Extract visited values from actions
        visited_values = []
        for step in steps:
            if "Visit node" in step.action:
                action = step.action
                value_str = action.split("value ")[1].split(",")[0]
                visited_values.append(int(value_str))

        # Level-order: root (10), level 1 (5, 15), level 2 (3, 7)
        assert visited_values == [10, 5, 15, 3, 7]

    def test_deep_tree(self):
        """BFS works on deeper trees."""
        tree = BinaryTree()
        # BinaryTree does level-order insertion, so:
        # Level 0: 10
        # Level 1: 5 (left), 15 (right)
        # Level 2: 3 (5's left), 20 (5's right)
        tree.insert(10)
        tree.insert(5)
        tree.insert(15)
        tree.insert(3)
        tree.insert(20)

        steps = list(bfs_search(tree.root, 20))
        final_step = steps[-1]
        assert final_step.is_complete
        # 20 is at root.left.right (5's right child)
        assert final_step.result is tree.root.left.right

    def test_highlights_current_node(self):
        """BFS highlights current node being examined."""
        tree = BinaryTree()
        tree.insert(10)
        tree.insert(5)

        steps = list(bfs_search(tree.root, 5))

        # First step should highlight root as current
        assert steps[0].highlights.current_node == id(tree.root)

    def test_highlights_visited_nodes(self):
        """BFS tracks visited nodes in highlights."""
        tree = BinaryTree()
        tree.insert(10)
        tree.insert(5)
        tree.insert(15)

        steps = list(bfs_search(tree.root, 99))

        # Final step should have all nodes as visited
        final_highlights = steps[-1].highlights
        assert id(tree.root) in final_highlights.visited_nodes
        assert id(tree.root.left) in final_highlights.visited_nodes
        assert id(tree.root.right) in final_highlights.visited_nodes

    def test_highlights_found_node(self):
        """BFS highlights found node when target is located."""
        tree = BinaryTree()
        tree.insert(10)
        tree.insert(5)

        steps = list(bfs_search(tree.root, 5))

        final_step = steps[-1]
        assert final_step.highlights.found_node == id(tree.root.left)

    def test_step_numbers_are_sequential(self):
        """Step numbers are sequential starting from 1."""
        tree = BinaryTree()
        tree.insert(10)
        tree.insert(5)
        tree.insert(15)

        steps = list(bfs_search(tree.root, 99))
        for i, step in enumerate(steps, 1):
            assert step.step_number == i

    def test_data_is_root(self):
        """Each step's data is the tree root."""
        tree = BinaryTree()
        tree.insert(10)
        tree.insert(5)

        steps = list(bfs_search(tree.root, 5))
        for step in steps:
            if step.data is not None:
                assert step.data is tree.root


class TestBFSTraversal:
    """Tests for bfs_traversal function."""

    def test_empty_tree(self):
        """Traversal of empty tree yields single complete step."""
        steps = list(bfs_traversal(None))
        assert len(steps) == 1
        assert steps[0].is_complete
        assert steps[0].result == []

    def test_single_node(self):
        """Traversal of single node tree."""
        tree = BinaryTree()
        tree.insert(10)

        steps = list(bfs_traversal(tree.root))
        final_step = steps[-1]
        assert final_step.is_complete
        assert final_step.result == [10]

    def test_levelorder_result(self):
        """Traversal returns values in level-order."""
        tree = BinaryTree()
        tree.insert(10)
        tree.insert(5)
        tree.insert(15)
        tree.insert(3)
        tree.insert(7)

        steps = list(bfs_traversal(tree.root))
        final_step = steps[-1]
        assert final_step.is_complete
        # Level-order: 10, 5, 15, 3, 7
        assert final_step.result == [10, 5, 15, 3, 7]

    def test_all_nodes_visited(self):
        """Traversal visits all nodes."""
        tree = BinaryTree()
        tree.insert(10)
        tree.insert(5)
        tree.insert(15)

        steps = list(bfs_traversal(tree.root))
        final_step = steps[-1]

        assert id(tree.root) in final_step.highlights.visited_nodes
        assert id(tree.root.left) in final_step.highlights.visited_nodes
        assert id(tree.root.right) in final_step.highlights.visited_nodes

    def test_highlights_current_during_traversal(self):
        """Traversal highlights current node at each step."""
        tree = BinaryTree()
        tree.insert(10)
        tree.insert(5)

        steps = list(bfs_traversal(tree.root))

        # Non-final steps should have current_node set
        for step in steps[:-1]:
            assert step.highlights.current_node is not None

