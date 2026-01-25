"""Tests for tree rendering with highlights."""

from dsa_visualizer.algorithms.types import TreeHighlightContext
from dsa_visualizer.data_structures.implementations.structures import BinaryTree
from dsa_visualizer.data_structures.render.binary_tree import render_binary_tree


class TestRenderTreeHighlights:
    """Tests for render_binary_tree with TreeHighlightContext."""

    def test_render_without_highlights(self):
        """Tree renders normally without highlights."""
        tree = BinaryTree()
        tree.insert(10)
        tree.insert(5)
        tree.insert(15)

        output = render_binary_tree(tree.root)
        assert "[10]" in output
        assert "[5]" in output
        assert "[15]" in output

    def test_render_with_empty_highlights(self):
        """Tree renders normally with empty highlight context."""
        tree = BinaryTree()
        tree.insert(10)
        tree.insert(5)
        tree.insert(15)

        highlights = TreeHighlightContext()
        output = render_binary_tree(tree.root, highlights)
        assert "[10]" in output
        assert "[5]" in output
        assert "[15]" in output

    def test_current_node_marker(self):
        """Current node shows arrow marker."""
        tree = BinaryTree()
        tree.insert(10)
        tree.insert(5)
        tree.insert(15)

        highlights = TreeHighlightContext(current_node=id(tree.root))
        output = render_binary_tree(tree.root, highlights)
        # Root should have current marker
        assert "[→10]" in output
        # Others should not
        assert "[5]" in output
        assert "[15]" in output

    def test_found_node_marker(self):
        """Found node shows checkmark marker."""
        tree = BinaryTree()
        tree.insert(10)
        tree.insert(5)
        tree.insert(15)

        # Find the left child node (value 5)
        left_node = tree.root.left
        highlights = TreeHighlightContext(found_node=id(left_node))
        output = render_binary_tree(tree.root, highlights)
        # Left child should have found marker
        assert "[✓5]" in output
        # Others should not
        assert "[10]" in output
        assert "[15]" in output

    def test_visited_nodes_marker(self):
        """Visited nodes show dot marker."""
        tree = BinaryTree()
        tree.insert(10)
        tree.insert(5)
        tree.insert(15)

        # Mark root as visited
        highlights = TreeHighlightContext(
            visited_nodes=frozenset({id(tree.root)})
        )
        output = render_binary_tree(tree.root, highlights)
        # Root should have visited marker
        assert "[·10]" in output
        # Others should not
        assert "[5]" in output
        assert "[15]" in output

    def test_path_nodes_marker(self):
        """Path nodes show dot marker."""
        tree = BinaryTree()
        tree.insert(10)
        tree.insert(5)
        tree.insert(15)

        highlights = TreeHighlightContext(
            path_nodes=(id(tree.root), id(tree.root.left))
        )
        output = render_binary_tree(tree.root, highlights)
        # Both root and left child should have path marker
        assert "[·10]" in output
        assert "[·5]" in output
        # Right child should not
        assert "[15]" in output

    def test_comparing_node_marker(self):
        """Comparing node shows question mark marker."""
        tree = BinaryTree()
        tree.insert(10)
        tree.insert(5)
        tree.insert(15)

        highlights = TreeHighlightContext(comparing_node=id(tree.root.right))
        output = render_binary_tree(tree.root, highlights)
        # Right child should have comparing marker
        assert "[?15]" in output
        # Others should not
        assert "[10]" in output
        assert "[5]" in output

    def test_marker_priority_found_over_current(self):
        """Found marker takes priority over current marker."""
        tree = BinaryTree()
        tree.insert(10)

        # Same node is both found and current - found should win
        highlights = TreeHighlightContext(
            current_node=id(tree.root),
            found_node=id(tree.root),
        )
        output = render_binary_tree(tree.root, highlights)
        assert "[✓10]" in output
        assert "[→10]" not in output

    def test_marker_priority_current_over_visited(self):
        """Current marker takes priority over visited marker."""
        tree = BinaryTree()
        tree.insert(10)

        # Same node is both current and visited - current should win
        highlights = TreeHighlightContext(
            current_node=id(tree.root),
            visited_nodes=frozenset({id(tree.root)}),
        )
        output = render_binary_tree(tree.root, highlights)
        assert "[→10]" in output
        assert "[·10]" not in output

    def test_multiple_highlights(self):
        """Multiple nodes can have different highlights simultaneously."""
        tree = BinaryTree()
        tree.insert(10)
        tree.insert(5)
        tree.insert(15)

        highlights = TreeHighlightContext(
            current_node=id(tree.root.left),  # 5 is current
            visited_nodes=frozenset({id(tree.root)}),  # 10 is visited
            comparing_node=id(tree.root.right),  # 15 is comparing
        )
        output = render_binary_tree(tree.root, highlights)
        assert "[·10]" in output
        assert "[→5]" in output
        assert "[?15]" in output

    def test_highlight_wider_label_width(self):
        """Label width accounts for markers when computing layout."""
        tree = BinaryTree()
        tree.insert(999)  # 3 digit value
        tree.insert(1)
        tree.insert(9999)  # 4 digit value

        # Without highlights
        output_no_hl = render_binary_tree(tree.root)

        # With highlights on the widest node
        highlights = TreeHighlightContext(current_node=id(tree.root.right))
        output_hl = render_binary_tree(tree.root, highlights)

        # Both should render without issues
        assert "[999]" in output_no_hl
        assert "[9999]" in output_no_hl
        assert "[999]" in output_hl
        assert "[→9999]" in output_hl

