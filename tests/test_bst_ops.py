from dsa_visualizer.core.structures import BinarySearchTree


def test_bst_search_finds_value() -> None:
    tree = BinarySearchTree([8, 3, 10, 1, 6])
    node = tree.search(6)
    assert node is not None
    assert node.value == 6


def test_bst_search_missing_value() -> None:
    tree = BinarySearchTree([8, 3, 10])
    assert tree.search(42) is None


def test_bst_delete_leaf() -> None:
    tree = BinarySearchTree([8, 3, 10, 1, 6])
    assert tree.delete(1) is True
    assert tree.search(1) is None


def test_bst_delete_root() -> None:
    tree = BinarySearchTree([8, 3, 10])
    assert tree.delete(8) is True
    assert tree.search(8) is None


def test_bst_delete_missing() -> None:
    tree = BinarySearchTree([8, 3, 10])
    assert tree.delete(99) is False
