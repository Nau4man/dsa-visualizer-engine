from __future__ import annotations

from dsa_visualizer.algorithms.types import TreeHighlightContext
from dsa_visualizer.algorithms.render.highlights import get_node_marker


def render_binary_tree(
    root: object | None,
    highlights: TreeHighlightContext | None = None,
) -> str:
    if root is None:
        return "(empty)"
    levels = _build_levels(root)
    label_width = _label_width(levels, highlights)
    lines: list[str] = []
    max_level = len(levels)
    gaps = _level_gaps(max_level)
    for level_index, level in enumerate(levels):
        gap = gaps[level_index]
        indent = gap // 2
        positions = _level_positions(level, indent, gap, label_width)
        lines.append(_render_level_line(level, positions, label_width, highlights))
        if level_index == max_level - 1:
            break
        if not _level_has_children(level):
            break
        lines.append(_render_parent_arrows(level, positions, label_width))
        child_gap = gaps[level_index + 1]
        child_positions = _level_positions(
            levels[level_index + 1],
            child_gap // 2,
            child_gap,
            label_width,
        )
        lines.append(_render_branch_line(level, child_positions, label_width))
        lines.append(
            _render_child_arrows(levels[level_index + 1], child_positions, label_width)
        )
    return "\n".join(line.rstrip() for line in lines)


def _build_levels(root: object) -> list[list[object | None]]:
    levels: list[list[object | None]] = []
    current: list[object | None] = [root]
    while any(node is not None for node in current):
        levels.append(current)
        next_level: list[object | None] = []
        for node in current:
            if node is None:
                next_level.extend([None, None])
            else:
                next_level.append(getattr(node, "left", None))
                next_level.append(getattr(node, "right", None))
        current = next_level
    return levels


def _level_has_children(level: list[object | None]) -> bool:
    for node in level:
        if node is None:
            continue
        if _node_has_child(node):
            return True
    return False


def _label_width(
    levels: list[list[object | None]],
    highlights: TreeHighlightContext | None = None,
) -> int:
    max_len = 1
    for level in levels:
        for node in level:
            if node is None:
                continue
            value_len = len(str(_node_value(node)))
            # Account for marker character if highlights are active
            if highlights is not None:
                marker = get_node_marker(node, highlights)
                if marker:
                    value_len += 1  # marker takes 1 character
            max_len = max(max_len, value_len)
    return max(4, max_len + 2)


def _level_gaps(level_count: int) -> list[int]:
    if level_count <= 0:
        return []
    gaps = [0] * level_count
    gaps[-1] = 4
    for index in range(level_count - 2, -1, -1):
        gaps[index] = gaps[index + 1] * 2 + 2
    return gaps


def _level_positions(
    level: list[object | None], indent: int, gap: int, label_width: int
) -> list[int]:
    positions: list[int] = []
    step = gap + label_width
    for idx in range(len(level)):
        positions.append(indent + idx * step)
    return positions


def _render_level_line(
    level: list[object | None],
    positions: list[int],
    label_width: int,
    highlights: TreeHighlightContext | None = None,
) -> str:
    width = positions[-1] + label_width if positions else label_width
    line = [" "] * width
    for node, pos in zip(level, positions):
        if node is None:
            continue
        label = _format_label(node, label_width, highlights)
        for i, ch in enumerate(label):
            line[pos + i] = ch
    return "".join(line).rstrip()


def _render_parent_arrows(
    level: list[object | None], positions: list[int], label_width: int
) -> str:
    width = positions[-1] + label_width if positions else label_width
    line = [" "] * width
    for node, pos in zip(level, positions):
        if node is None:
            continue
        if not _node_has_child(node):
            continue
        center = pos + _label_center_offset(node, label_width)
        line[center] = "▼"
    return "".join(line).rstrip()


def _render_branch_line(
    level: list[object | None], child_positions: list[int], label_width: int
) -> str:
    if not child_positions:
        return ""
    width = child_positions[-1] + label_width
    line = [" "] * width
    for index, node in enumerate(level):
        if node is None:
            continue
        left = getattr(node, "left", None)
        right = getattr(node, "right", None)
        if left is None and right is None:
            continue
        left_index = index * 2
        right_index = left_index + 1
        left_child = left
        right_child = right
        left_center = child_positions[left_index] + _label_center_offset(
            left_child, label_width
        )
        right_center = child_positions[right_index] + _label_center_offset(
            right_child, label_width
        )
        if left is None:
            left_center = right_center
        if right is None:
            right_center = left_center
        if left_center == right_center:
            line[left_center] = "│"
            continue
        line[left_center] = "┌"
        line[right_center] = "┐"
        for pos in range(left_center + 1, right_center):
            line[pos] = "─"
    return "".join(line).rstrip()


def _render_child_arrows(
    level: list[object | None], positions: list[int], label_width: int
) -> str:
    if not positions:
        return ""
    width = positions[-1] + label_width
    line = [" "] * width
    for node, pos in zip(level, positions):
        if node is None:
            continue
        center = pos + _label_center_offset(node, label_width)
        line[center] = "▼"
    return "".join(line).rstrip()


def _node_value(node: object) -> object:
    if hasattr(node, "value"):
        return getattr(node, "value")
    return getattr(node, "data")


def _format_label(
    node: object,
    width: int,
    highlights: TreeHighlightContext | None = None,
) -> str:
    value = str(_node_value(node))
    marker = ""
    if highlights is not None:
        marker = get_node_marker(node, highlights)
    label = f"[{marker}{value}]"
    return label.ljust(width)


def _label_center_offset(node: object | None, label_width: int) -> int:
    if label_width <= 3:
        return label_width // 2
    return (label_width // 2) - 1


def _node_has_child(node: object) -> bool:
    return (
        getattr(node, "left", None) is not None
        or getattr(node, "right", None) is not None
    )
