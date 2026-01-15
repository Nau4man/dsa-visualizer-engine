from __future__ import annotations

from dsa_visualizer.core.structures import LinkedList


def render_linked_list(target: object) -> str:
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
    connector = " ──▶ "
    indent = " " * len("Head ──▶ ")
    gap = " " * len(connector)
    top = connector.join(box[0] for box in boxes)
    mid = gap.join(box[1] for box in boxes)
    bottom = gap.join(box[2] for box in boxes)
    return [f"Head ──▶ {top}", f"{indent}{mid}", f"{indent}{bottom}"]


def _render_node_box(node: object, data_width: int, pointer_width: int) -> list[str]:
    data_text = str(_node_value(node))
    pointer_text = "NULL" if node.next is None else "•"
    top = f"┌{'─' * data_width}┬{'─' * pointer_width}┐"
    middle = f"│{data_text.center(data_width)}│{pointer_text.center(pointer_width)}│"
    bottom = f"└{'─' * data_width}┴{'─' * pointer_width}┘"
    return [top, middle, bottom]


def _render_node_structure(nodes: list[object]) -> list[str]:
    data_label = "data"
    next_label = "next"
    if nodes:
        node = nodes[0]
        data_text = str(_node_value(node))
        next_text = _format_next_address(node.next)
    else:
        data_text = ""
        next_text = "NULL"
    data_width = max(8, len(data_label), len(data_text))
    next_width = max(8, len(next_label), len(next_text))
    top = f"┌{'─' * data_width}┬{'─' * next_width}┐"
    header = f"│{data_label.center(data_width)}│{next_label.center(next_width)}│"
    bottom = f"└{'─' * data_width}┴{'─' * next_width}┘"
    row = f" {data_text.center(data_width)} {next_text.center(next_width)}"
    return [top, header, bottom, row]


def _format_next_address(node: object | None) -> str:
    if node is None:
        return "NULL"
    return hex(id(node))


def _node_value(node: object) -> object:
    if hasattr(node, "value"):
        return getattr(node, "value")
    return getattr(node, "data")


def _resolve_head(target: object) -> object | None:
    if isinstance(target, LinkedList):
        return target.head
    if _is_node_like(target):
        return target
    try:
        head = getattr(target, "head")
    except AttributeError:
        return None
    if head is None:
        return None
    return head if _is_node_like(head) else None


def _is_node_like(value: object) -> bool:
    try:
        getattr(value, "next")
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
