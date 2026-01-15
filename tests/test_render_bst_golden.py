from dsa_visualizer.core.structures import BinarySearchTree
from dsa_visualizer.render.binary_search_tree import render_binary_search_tree


def test_render_bst_sample() -> None:
    tree = BinarySearchTree([8, 3, 10, 1, 6])
    expected = (
        "           [8]\n"
        "            ▼\n"
        "      ┌─────────────┐\n"
        "      ▼             ▼\n"
        "     [3]           [10]\n"
        "      ▼\n"
        "   ┌───────┐\n"
        "   ▼       ▼\n"
        "  [1]     [6]\n"
        "\n"
        "Left < Node < Right"
    )
    assert render_binary_search_tree(tree.root) == expected


def test_render_bst_empty() -> None:
    expected = "(empty)\n\nLeft < Node < Right"
    assert render_binary_search_tree(None) == expected
