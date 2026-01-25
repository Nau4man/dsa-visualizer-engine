from __future__ import annotations

from dsa_visualizer.data_structures.render.binary_tree import render_binary_tree


def render_binary_search_tree(root: object | None) -> str:
    if root is None:
        return "(empty)\n\nLeft < Node < Right"
    tree = render_binary_tree(root)
    return f"{tree}\n\nLeft < Node < Right"
