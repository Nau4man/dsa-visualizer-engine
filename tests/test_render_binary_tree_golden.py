from dsa_visualizer.data_structures.implementations.structures import BinaryTree
from dsa_visualizer.data_structures.render.binary_tree import render_binary_tree


def test_render_binary_tree_sample() -> None:
    tree = BinaryTree(["A", "B", "C", "D", "E"])
    expected = (
        "           [A]\n"
        "            ▼\n"
        "      ┌─────────────┐\n"
        "      ▼             ▼\n"
        "     [B]           [C]\n"
        "      ▼\n"
        "   ┌───────┐\n"
        "   ▼       ▼\n"
        "  [D]     [E]"
    )
    assert render_binary_tree(tree.root) == expected


def test_render_binary_tree_empty() -> None:
    assert render_binary_tree(None) == "(empty)"
