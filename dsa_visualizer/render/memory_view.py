from __future__ import annotations

from dsa_visualizer.core.snapshotter import ObjectRecord, Snapshot
from dsa_visualizer.core.types import MemoryBlock
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


def get_memory_blocks(snapshot: Snapshot) -> list[MemoryBlock]:
    """Return a list of MemoryBlocks for each variable/object in the snapshot."""
    blocks: list[MemoryBlock] = []
    object_names: dict[str, list[str]] = {}

    for name, target in snapshot.names.items():
        if isinstance(target, str) and target.startswith("obj#"):
            object_names.setdefault(target, []).append(name)
        else:
            # Primitive value
            content = render_primitive(name, target)
            type_name = type(target).__name__ if target is not None else "None"
            header = f"{name} ──▶ {type_name}"
            summary = repr(target) if target is not None else "None"
            blocks.append(MemoryBlock(
                block_id=f"var_{name}",
                header=header,
                summary=summary,
                content=content,
            ))

    for obj_id, names in object_names.items():
        record = snapshot.objects.get(obj_id)
        if record is None:
            continue
        header_lines, content = _render_object_block(record, sorted(names))
        header = header_lines[0] if len(header_lines) == 1 else header_lines[-1]
        full_header = "\n".join(header_lines)
        blocks.append(MemoryBlock(
            block_id=obj_id,
            header=full_header,
            summary=record.summary,
            content=content,
        ))

    return blocks


def render_memory(snapshot: Snapshot) -> str:
    """Render all memory blocks as a single string (legacy compatibility)."""
    blocks = get_memory_blocks(snapshot)
    if not blocks:
        return ""
    parts: list[str] = []
    for block in blocks:
        parts.append(block.header)
        parts.append(block.content)
        parts.append("")
    if parts and parts[-1] == "":
        parts.pop()
    return "\n".join(parts)


def _render_object_block(
    record: ObjectRecord, names: list[str]
) -> tuple[list[str], str]:
    """Return (header_lines, content_string) for an object."""
    header = _render_names_header(names, record.dsa_type)
    content = _render_object_content(record)
    return header, content


def _render_object_content(record: ObjectRecord) -> str:
    """Render just the content part of an object (no header)."""
    if record.dsa_type == "Array" and isinstance(record.payload, list):
        return render_array(record.payload)
    if record.dsa_type == "Hash Table" and isinstance(record.payload, dict):
        return render_hashmap(record.payload)
    if record.dsa_type == "Doubly Linked List":
        return render_doubly_linked_list(record.payload)
    if record.dsa_type == "Linked List":
        return render_linked_list(record.payload)
    if record.dsa_type == "Stack" and isinstance(record.payload, list):
        return render_stack(record.payload)
    if record.dsa_type == "Queue" and isinstance(record.payload, list):
        return render_queue(record.payload)
    if record.dsa_type == "Binary Search Tree":
        return render_binary_search_tree(record.payload)
    if record.dsa_type == "Binary Tree":
        return render_binary_tree(record.payload)
    if record.dsa_type == "Min Heap" and isinstance(record.payload, list):
        return render_min_heap(record.payload)
    if record.dsa_type == "Undirected Graph" and isinstance(record.payload, dict):
        return render_graph(record.payload, directed=False)
    if record.dsa_type == "Directed Graph" and isinstance(record.payload, dict):
        return render_graph(record.payload, directed=True)
    return f"{record.dsa_type} {record.summary}".strip()


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
