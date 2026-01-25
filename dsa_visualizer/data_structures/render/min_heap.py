from __future__ import annotations

from dsa_visualizer.data_structures.render.binary_tree import render_binary_tree


class _HeapNode:
    def __init__(self, value: object) -> None:
        self.value = value
        self.left: _HeapNode | None = None
        self.right: _HeapNode | None = None


def render_min_heap(values: list[object]) -> str:
    if not values:
        return "(empty)"
    nodes = [_HeapNode(value) for value in values]
    for index, node in enumerate(nodes):
        left_index = index * 2 + 1
        right_index = left_index + 1
        if left_index < len(nodes):
            node.left = nodes[left_index]
        if right_index < len(nodes):
            node.right = nodes[right_index]
    return render_binary_tree(nodes[0])
