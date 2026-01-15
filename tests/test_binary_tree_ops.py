from dsa_visualizer.core.structures import BinaryTree


def test_binary_tree_search_finds_value() -> None:
    tree = BinaryTree(["A", "B", "C"])
    node = tree.search("B")
    assert node is not None
    assert node.value == "B"


def test_binary_tree_search_missing_value() -> None:
    tree = BinaryTree(["A", "B", "C"])
    assert tree.search("Z") is None


def test_binary_tree_delete_leaf() -> None:
    tree = BinaryTree(["A", "B", "C", "D"])
    assert tree.delete("D") is True
    assert tree.search("D") is None


def test_binary_tree_delete_root() -> None:
    tree = BinaryTree(["A", "B", "C"])
    assert tree.delete("A") is True
    assert tree.search("A") is None


def test_binary_tree_delete_missing() -> None:
    tree = BinaryTree(["A", "B", "C"])
    assert tree.delete("Z") is False
