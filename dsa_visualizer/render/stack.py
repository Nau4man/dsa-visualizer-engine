from __future__ import annotations


def render_stack(values: list[object]) -> str:
    lines: list[str] = ["Top", " │", " ▼"]
    if not values:
        lines.append("(empty)")
        return "\n".join(lines)

    text_values = [str(value) for value in values]
    inner_width = max(5, max(len(text) for text in text_values) + 2)
    top = f"┌{'─' * inner_width}┐"
    middle = "│{}│"
    divider = f"├{'─' * inner_width}┤"
    bottom = f"└{'─' * inner_width}┘"

    for index, value in enumerate(reversed(text_values)):
        lines.append(top if index == 0 else divider)
        lines.append(middle.format(value.center(inner_width)))
    lines.append(bottom)
    return "\n".join(lines)
