from dsa_visualizer.core.snapshotter import Snapshotter
from dsa_visualizer.render.memory_view import render_memory


class Node:
    def __init__(self, value: object) -> None:
        self.value = value
        self.left = None
        self.right = None


class Tree:
    def __init__(self) -> None:
        self.root = None

    def set_root(self, value: object) -> None:
        self.root = Node(value)


def test_structural_binary_tree_rendering() -> None:
    tree = Tree()
    tree.set_root("A")
    tree.root.left = Node("B")
    snapshotter = Snapshotter()
    snapshot = snapshotter.snapshot({"tree": tree})
    rendered = render_memory(snapshot)

    assert "tree ──▶ Binary Tree" in rendered
    assert "[A]" in rendered


def test_bst_rendering() -> None:
    from dsa_visualizer.data_structures.implementations.structures import BinarySearchTree

    tree = BinarySearchTree([8, 3, 10, 1, 6])
    snapshotter = Snapshotter()
    snapshot = snapshotter.snapshot({"bst": tree})
    rendered = render_memory(snapshot)

    assert "bst ──▶ Binary Search Tree" in rendered
    assert "Left < Node < Right" in rendered


def test_min_heap_rendering() -> None:
    from dsa_visualizer.data_structures.implementations.structures import MinHeap

    heap = MinHeap([1, 3, 5])
    snapshotter = Snapshotter()
    snapshot = snapshotter.snapshot({"heap": heap})
    rendered = render_memory(snapshot)

    assert "heap ──▶ Min Heap" in rendered
    assert "[1]" in rendered


class CustomMinHeap:
    def __init__(self) -> None:
        self._data: list[object] = []

    def insert(self, value: object) -> None:
        self._data.append(value)
        self._data.sort()

    def pop_min(self) -> object | None:
        if not self._data:
            return None
        return self._data.pop(0)

    def peek(self) -> object | None:
        if not self._data:
            return None
        return self._data[0]


def test_structural_min_heap_rendering() -> None:
    heap = CustomMinHeap()
    heap.insert(1)
    heap.insert(3)
    snapshotter = Snapshotter()
    snapshot = snapshotter.snapshot({"heap": heap})
    rendered = render_memory(snapshot)

    assert "heap ──▶ Min Heap" in rendered
    assert "[1]" in rendered


def test_graph_rendering() -> None:
    from dsa_visualizer.data_structures.implementations.structures import Graph

    graph = Graph()
    graph.add_edge("A", "B")
    graph.add_edge("A", "C")
    snapshotter = Snapshotter()
    snapshot = snapshotter.snapshot({"graph": graph})
    rendered = render_memory(snapshot)

    assert "graph ──▶ Undirected Graph" in rendered
    assert "Adjacency list" in rendered


class CustomGraph:
    def __init__(self) -> None:
        self.directed = True
        self.adj: dict[str, list[str]] = {}

    def add_edge(self, source: str, target: str) -> None:
        self.adj.setdefault(source, []).append(target)


def test_structural_graph_rendering() -> None:
    graph = CustomGraph()
    graph.add_edge("A", "B")
    snapshotter = Snapshotter()
    snapshot = snapshotter.snapshot({"graph": graph})
    rendered = render_memory(snapshot)

    assert "graph ──▶ Directed Graph" in rendered
    assert "Directed Edges" in rendered
