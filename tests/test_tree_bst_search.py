"""Tests for BST search algorithm."""

from dsa_visualizer.algorithms.tree.bst_search import bst_search
from dsa_visualizer.data_structures.implementations.structures import BinarySearchTree


class TestBSTSearch:
    """Tests for bst_search function."""

    def test_empty_tree(self):
        """BST search on empty tree yields single complete step."""
        steps = list(bst_search(None, 10))
        assert len(steps) == 1
        assert steps[0].is_complete
        assert steps[0].result is None
        assert "empty" in steps[0].action.lower()

    def test_single_node_found(self):
        """BST search finds target in single-node tree."""
        tree = BinarySearchTree()
        tree.insert(10)

        steps = list(bst_search(tree.root, 10))
        # Only 1 step needed - compare and found
        assert len(steps) == 1
        assert steps[-1].is_complete
        assert steps[-1].result is tree.root
        assert "Found" in steps[-1].action

    def test_single_node_not_found_left(self):
        """BST search reports not found when target would be in left."""
        tree = BinarySearchTree()
        tree.insert(10)

        steps = list(bst_search(tree.root, 5))
        assert steps[-1].is_complete
        assert steps[-1].result is None
        assert "not found" in steps[-1].action.lower()
        assert "left" in steps[-2].action.lower()  # Went left

    def test_single_node_not_found_right(self):
        """BST search reports not found when target would be in right."""
        tree = BinarySearchTree()
        tree.insert(10)

        steps = list(bst_search(tree.root, 15))
        assert steps[-1].is_complete
        assert steps[-1].result is None
        assert "not found" in steps[-1].action.lower()
        assert "right" in steps[-2].action.lower()  # Went right

    def test_finds_root(self):
        """BST search finds target at root."""
        tree = BinarySearchTree()
        tree.insert(10)
        tree.insert(5)
        tree.insert(15)

        steps = list(bst_search(tree.root, 10))
        final_step = steps[-1]
        assert final_step.is_complete
        assert final_step.result is tree.root

    def test_finds_left_child(self):
        """BST search finds target in left subtree."""
        tree = BinarySearchTree()
        tree.insert(10)
        tree.insert(5)
        tree.insert(15)

        steps = list(bst_search(tree.root, 5))
        final_step = steps[-1]
        assert final_step.is_complete
        assert final_step.result is tree.root.left

    def test_finds_right_child(self):
        """BST search finds target in right subtree."""
        tree = BinarySearchTree()
        tree.insert(10)
        tree.insert(5)
        tree.insert(15)

        steps = list(bst_search(tree.root, 15))
        final_step = steps[-1]
        assert final_step.is_complete
        assert final_step.result is tree.root.right

    def test_efficient_search_goes_correct_direction(self):
        """BST search goes directly to target without visiting unnecessary nodes."""
        tree = BinarySearchTree()
        # Build:
        #       10
        #      /  \
        #     5    15
        #    / \   / \
        #   3   7 12  20
        tree.insert(10)
        tree.insert(5)
        tree.insert(15)
        tree.insert(3)
        tree.insert(7)
        tree.insert(12)
        tree.insert(20)

        # Search for 12 - should only visit 10 -> 15 -> 12
        steps = list(bst_search(tree.root, 12))
        final_step = steps[-1]
        assert final_step.is_complete
        assert final_step.result is tree.root.right.left

        # Should not have visited left subtree
        visited = final_step.highlights.visited_nodes
        assert id(tree.root.left) not in visited
        assert id(tree.root.left.left) not in visited
        assert id(tree.root.left.right) not in visited

    def test_action_shows_comparison(self):
        """BST search shows comparison in action string."""
        tree = BinarySearchTree()
        tree.insert(10)
        tree.insert(5)

        steps = list(bst_search(tree.root, 5))

        # First step compares 5 with 10
        first_step = steps[0]
        assert "5" in first_step.action
        assert "10" in first_step.action
        assert "<" in first_step.action  # 5 < 10

    def test_deep_tree(self):
        """BST search works on deeper trees."""
        tree = BinarySearchTree()
        tree.insert(50)
        tree.insert(25)
        tree.insert(75)
        tree.insert(10)
        tree.insert(30)
        tree.insert(60)
        tree.insert(90)
        tree.insert(5)

        steps = list(bst_search(tree.root, 5))
        final_step = steps[-1]
        assert final_step.is_complete
        assert final_step.result is tree.root.left.left.left

    def test_highlights_current_node(self):
        """BST search highlights current node being examined."""
        tree = BinarySearchTree()
        tree.insert(10)
        tree.insert(5)

        steps = list(bst_search(tree.root, 5))

        # First step should highlight root as current
        assert steps[0].highlights.current_node == id(tree.root)

    def test_highlights_path_nodes(self):
        """BST search tracks path to target in highlights."""
        tree = BinarySearchTree()
        tree.insert(10)
        tree.insert(5)
        tree.insert(15)
        tree.insert(3)

        steps = list(bst_search(tree.root, 3))
        final_step = steps[-1]

        # Path should be root -> left -> left-left
        path = final_step.highlights.path_nodes
        assert id(tree.root) in path
        assert id(tree.root.left) in path
        assert id(tree.root.left.left) in path

    def test_highlights_found_node(self):
        """BST search highlights found node when target is located."""
        tree = BinarySearchTree()
        tree.insert(10)
        tree.insert(5)

        steps = list(bst_search(tree.root, 5))

        final_step = steps[-1]
        assert final_step.highlights.found_node == id(tree.root.left)

    def test_step_numbers_are_sequential(self):
        """Step numbers are sequential starting from 1."""
        tree = BinarySearchTree()
        tree.insert(10)
        tree.insert(5)
        tree.insert(15)

        steps = list(bst_search(tree.root, 99))
        for i, step in enumerate(steps, 1):
            assert step.step_number == i

    def test_data_is_root(self):
        """Each step's data is the tree root."""
        tree = BinarySearchTree()
        tree.insert(10)
        tree.insert(5)

        steps = list(bst_search(tree.root, 5))
        for step in steps:
            if step.data is not None:
                assert step.data is tree.root

    def test_skewed_tree_left(self):
        """BST search works on left-skewed tree."""
        tree = BinarySearchTree()
        tree.insert(50)
        tree.insert(40)
        tree.insert(30)
        tree.insert(20)
        tree.insert(10)

        steps = list(bst_search(tree.root, 10))
        final_step = steps[-1]
        assert final_step.is_complete
        assert final_step.result.value == 10

    def test_skewed_tree_right(self):
        """BST search works on right-skewed tree."""
        tree = BinarySearchTree()
        tree.insert(10)
        tree.insert(20)
        tree.insert(30)
        tree.insert(40)
        tree.insert(50)

        steps = list(bst_search(tree.root, 50))
        final_step = steps[-1]
        assert final_step.is_complete
        assert final_step.result.value == 50

