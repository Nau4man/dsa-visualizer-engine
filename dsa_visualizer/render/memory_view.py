from __future__ import annotations

from dsa_visualizer.core.snapshotter import ObjectRecord, Snapshot
from dsa_visualizer.render.array import render_array
from dsa_visualizer.render.binary_search_tree import render_binary_search_tree
from dsa_visualizer.render.binary_tree import render_binary_tree
from dsa_visualizer.render.doubly_linked_list import render_doubly_linked_list
from dsa_visualizer.render.graph import render_graph
from dsa_visualizer.render.hashmap import render_hashmap
from dsa_visualizer.render.linked_list import render_linked_list
from dsa_visualizer.render.min_heap import render_min_heap
from dsa_visualizer.render.primitive import render_primitive
from dsa_visualizer.render.queue import render_queue
from dsa_visualizer.render.stack import render_stack


def render_memory(snapshot: Snapshot) -> str:
    lines: list[str] = []
    object_names: dict[str, list[str]] = {}
    for name, target in snapshot.names.items():
        if isinstance(target, str) and target.startswith("obj#"):
            object_names.setdefault(target, []).append(name)
        else:
            lines.append(render_primitive(name, target))
            lines.append("")

    for obj_id, names in object_names.items():
        record = snapshot.objects.get(obj_id)
        if record is None:
            continue
        lines.extend(_render_object_block(record, names))
        lines.append("")

    if lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines)


def _render_object_block(record: ObjectRecord, names: list[str]) -> list[str]:
    header = _render_names_header(sorted(names), record.dsa_type)
    if record.dsa_type == "Array" and isinstance(record.payload, list):
        return header + [render_array(record.payload)]
    if record.dsa_type == "Hash Table" and isinstance(record.payload, dict):
        return header + [render_hashmap(record.payload)]
    if record.dsa_type == "Doubly Linked List":
        return header + [render_doubly_linked_list(record.payload)]
    if record.dsa_type == "Linked List":
        return header + [render_linked_list(record.payload)]
    if record.dsa_type == "Stack" and isinstance(record.payload, list):
        return header + [render_stack(record.payload)]
    if record.dsa_type == "Queue" and isinstance(record.payload, list):
        return header + [render_queue(record.payload)]
    if record.dsa_type == "Binary Search Tree":
        return header + [render_binary_search_tree(record.payload)]
    if record.dsa_type == "Binary Tree":
        return header + [render_binary_tree(record.payload)]
    if record.dsa_type == "Min Heap" and isinstance(record.payload, list):
        return header + [render_min_heap(record.payload)]
    if record.dsa_type == "Undirected Graph" and isinstance(record.payload, dict):
        return header + [render_graph(record.payload, directed=False)]
    if record.dsa_type == "Directed Graph" and isinstance(record.payload, dict):
        return header + [render_graph(record.payload, directed=True)]
    summary = f"{record.dsa_type} {record.summary}".strip()
    return header + [summary]


def _render_names_header(names: list[str], dsa_type: str) -> list[str]:
    if len(names) == 1:
        return [f"{names[0]} ──▶ {dsa_type}"]
    lines: list[str] = []
    for index, name in enumerate(names):
        if index == 0:
            lines.append(f"{name} ──┐")
        elif index == len(names) - 1:
            lines.append(f"{name} ──┘")
        else:
            lines.append(f"{name} ──┤")
    lines.append(f"▶ {dsa_type}")
    return lines
