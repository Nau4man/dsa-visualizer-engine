from __future__ import annotations

from dsa_visualizer.data_structures.implementations.structures import DoublyLinkedList


def render_doubly_linked_list(target: object) -> str:
    head = _resolve_head(target)
    nodes = _iter_nodes(head)
    lines = _render_chain(nodes)
    lines.append("")
    lines.append("Node Structure")
    lines.extend(_render_node_structure(nodes))
    return "\n".join(lines)


def _render_chain(nodes: list[object]) -> list[str]:
    if not nodes:
        return ["Head ──▶ NULL"]
    data_texts = [str(_node_value(node)) for node in nodes]
    data_width = max(4, max(len(text) for text in data_texts))
    pointer_width = max(5, len("NULL"))
    boxes = [_render_node_box(node, data_width, pointer_width) for node in nodes]
    connector = " ⇄ "
    indent = " " * len("Head ──▶ ")
    gap = " " * len(connector)
    top = connector.join(box[0] for box in boxes)
    mid = gap.join(box[1] for box in boxes)
    bottom = gap.join(box[2] for box in boxes)
    return [f"Head ──▶ {top}", f"{indent}{mid}", f"{indent}{bottom}"]


def _render_node_box(node: object, data_width: int, pointer_width: int) -> list[str]:
    data_text = str(_node_value(node))
    prev_text = "NULL" if getattr(node, "prev", None) is None else "•"
    next_text = "NULL" if getattr(node, "next", None) is None else "•"
    top = f"┌{'─' * pointer_width}┬{'─' * data_width}┬{'─' * pointer_width}┐"
    if pointer_width == 5:
        prev_cell = _format_pointer_cell(prev_text)
        next_cell = _format_pointer_cell(next_text)
    else:
        prev_cell = prev_text.center(pointer_width)
        next_cell = next_text.center(pointer_width)
    middle = f"│{prev_cell}│{data_text.center(data_width)}│{next_cell}│"
    bottom = f"└{'─' * pointer_width}┴{'─' * data_width}┴{'─' * pointer_width}┘"
    return [top, middle, bottom]


def _render_node_structure(nodes: list[object]) -> list[str]:
    prev_label = "prev"
    data_label = "data"
    next_label = "next"
    if nodes:
        node = nodes[0]
        prev_text = _format_address(getattr(node, "prev", None))
        data_text = str(_node_value(node))
        next_text = _format_address(getattr(node, "next", None))
    else:
        prev_text = "NULL"
        data_text = ""
        next_text = "NULL"
    prev_width = max(8, len(prev_label), len(prev_text))
    data_width = max(8, len(data_label), len(data_text))
    next_width = max(8, len(next_label), len(next_text))
    top = f"┌{'─' * prev_width}┬{'─' * data_width}┬{'─' * next_width}┐"
    header = (
        f"│{prev_label.center(prev_width)}│{data_label.center(data_width)}│"
        f"{next_label.center(next_width)}│"
    )
    bottom = f"└{'─' * prev_width}┴{'─' * data_width}┴{'─' * next_width}┘"
    row = (
        f" {prev_text.center(prev_width)} "
        f"{data_text.center(data_width)} "
        f"{next_text.center(next_width)}"
    )
    return [top, header, bottom, row]


def _format_address(node: object | None) -> str:
    if node is None:
        return "NULL"
    return hex(id(node))


def _format_pointer_cell(text: str) -> str:
    if text == "NULL":
        return "NULL "
    return "  •  "


def _node_value(node: object) -> object:
    if hasattr(node, "value"):
        return getattr(node, "value")
    return getattr(node, "data")


def _resolve_head(target: object) -> object | None:
    if isinstance(target, DoublyLinkedList):
        return target.head
    if _is_doubly_node_like(target):
        return target
    try:
        head = getattr(target, "head")
    except AttributeError:
        return None
    if head is None:
        return None
    return head if _is_doubly_node_like(head) else None


def _is_doubly_node_like(value: object) -> bool:
    try:
        getattr(value, "next")
        getattr(value, "prev")
    except AttributeError:
        return False
    return hasattr(value, "value") or hasattr(value, "data")


def _iter_nodes(head: object | None) -> list[object]:
    nodes: list[object] = []
    seen: set[int] = set()
    current = head
    while current is not None:
        node_id = id(current)
        if node_id in seen:
            break
        seen.add(node_id)
        nodes.append(current)
        current = getattr(current, "next", None)
    return nodes
