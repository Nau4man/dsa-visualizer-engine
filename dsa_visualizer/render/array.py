from __future__ import annotations


def render_array(values: list[object]) -> str:
    if not values:
        return "(empty)"

    max_len = 1
    for index, value in enumerate(values):
        max_len = max(max_len, len(str(index)), len(str(value)))

    cell_width = max_len + 3
    prefix = "Index → "
    spacer = " " * len(prefix)

    def cell(text: str) -> str:
        return f" {text} ".ljust(cell_width)

    def border(left: str, mid: str, right: str) -> str:
        segments = [left]
        segments.append("─" * cell_width)
        for _ in values[1:]:
            segments.append(mid)
            segments.append("─" * cell_width)
        segments.append(right)
        return "".join(segments)

    top = border("┌", "┬", "┐")
    middle = border("├", "┼", "┤")
    bottom = border("└", "┴", "┘")
    index_cells = [cell(str(index)) for index in range(len(values))]
    value_cells = [cell(str(value)) for value in values]
    lines = [
        f"{spacer}{top}",
        f"{prefix}│{'│'.join(index_cells)}│",
        f"{spacer}{middle}",
        f"{'Array → '}│{'│'.join(value_cells)}│",
        f"{spacer}{bottom}",
    ]
    return "\n".join(lines)
