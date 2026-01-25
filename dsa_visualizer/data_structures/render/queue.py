from __future__ import annotations


def render_queue(values: list[object]) -> str:
    if not values:
        return "Front ──▶ (empty) ──▶ Rear"

    text_values = [str(value) for value in values]
    cell_width = max(5, max(len(text) for text in text_values) + 2)
    top = "┌" + "┬".join("─" * cell_width for _ in text_values) + "┐"
    middle = "│" + "│".join(text.center(cell_width) for text in text_values) + "│"
    bottom = "└" + "┴".join("─" * cell_width for _ in text_values) + "┘"
    prefix = "Front ──▶ "
    indent = " " * len(prefix)
    return "\n".join(
        [
            f"{prefix}{top} ──▶ Rear",
            f"{indent}{middle}",
            f"{indent}{bottom}",
        ]
    )
