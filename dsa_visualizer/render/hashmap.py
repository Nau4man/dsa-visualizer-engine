from __future__ import annotations

import hashlib


def render_hashmap(values: dict[object, object]) -> str:
    bucket_count = max(5, len(values))
    buckets: list[list[tuple[object, object]]] = [[] for _ in range(bucket_count)]
    for key, value in values.items():
        index = _stable_hash(key) % bucket_count
        buckets[index].append((key, value))

    lines: list[str] = ["Index"]
    for index, bucket in enumerate(buckets):
        lines.extend(_render_bucket(index, bucket))

    lines.append("")
    lines.append("Node Structure")
    lines.extend(_render_node_structure(values, buckets))
    return "\n".join(lines)


def _render_bucket(index: int, bucket: list[tuple[object, object]]) -> list[str]:
    prefix = f" {index} ──▶ "
    if not bucket:
        return [f"{prefix}NULL"]

    boxes = [_render_node_box(key, value) for key, value in bucket]
    height = len(boxes[0])
    lines: list[str] = []
    indent = " " * len(prefix)
    for row_index in range(height):
        row = " ──▶ ".join(box[row_index] for box in boxes)
        if row_index == 0:
            lines.append(f"{prefix}{row} ──▶ NULL")
        else:
            lines.append(f"{indent}{row}")
    return lines


def _render_node_box(key: object, value: object) -> list[str]:
    key_label = "key"
    value_label = "value"
    key_text = str(key)
    value_text = str(value)
    key_width = max(len(key_label), len(key_text))
    value_width = max(len(value_label), len(value_text))
    top = f"┌{'─' * (key_width + 2)}┬{'─' * (value_width + 2)}┐"
    middle = (
        f"│ {key_text.ljust(key_width)} │ {value_text.ljust(value_width)} │"
    )
    bottom = f"└{'─' * (key_width + 2)}┴{'─' * (value_width + 2)}┘"
    return [top, middle, bottom]


def _render_node_structure(
    values: dict[object, object],
    buckets: list[list[tuple[object, object]]],
) -> list[str]:
    min_width = 8
    key_label = "key"
    value_label = "value"
    next_label = "next"
    next_value = "NULL"
    if values:
        last_key, last_value = next(reversed(values.items()))
        key_text = str(last_key)
        value_text = str(last_value)
        next_value = _find_next_address(last_key, buckets)
    else:
        key_text = ""
        value_text = ""
    key_width = max(min_width, len(key_label), len(key_text))
    value_width = max(min_width, len(value_label), len(value_text))
    next_width = max(min_width, len(next_label), len(next_value))
    top = (
        f"┌{'─' * key_width}┬{'─' * value_width}┬"
        f"{'─' * next_width}┐"
    )
    header = (
        f"│{key_label.center(key_width)}│{value_label.center(value_width)}│"
        f"{next_label.center(next_width)}│"
    )
    bottom = (
        f"└{'─' * key_width}┴{'─' * value_width}┴"
        f"{'─' * next_width}┘"
    )
    row = _render_node_row(
        key_text, value_text, next_value, key_width, value_width, next_width
    )
    return [top, header, bottom, row]


def _render_node_row(
    key_text: str,
    value_text: str,
    next_text: str,
    key_width: int,
    value_width: int,
    next_width: int,
) -> str:
    key_cell = key_text.center(key_width)
    value_cell = value_text.center(value_width)
    next_cell = next_text.center(next_width)
    return f" {key_cell} {value_cell} {next_cell}"


def _find_next_address(
    key: object,
    buckets: list[list[tuple[object, object]]],
) -> str:
    for bucket in buckets:
        for index, (bucket_key, _) in enumerate(bucket):
            if bucket_key == key:
                if index + 1 < len(bucket):
                    next_key = bucket[index + 1][0]
                    return _format_address(next_key)
                return "NULL"
    return "NULL"


def _stable_hash(value: object) -> int:
    data = repr(value).encode("utf-8")
    return int(hashlib.sha256(data).hexdigest(), 16)


def _format_address(value: object) -> str:
    digest = _stable_hash(value)
    return f"0x{digest & 0xFFFF:04x}"
