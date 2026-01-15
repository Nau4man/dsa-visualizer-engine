from __future__ import annotations

from rich.text import Text

from dsa_visualizer.core.types import Cell


def render_cell_text(cell: Cell, *, expanded: bool) -> Text:
    status = "✔" if cell.ok else "✖"
    status_style = "green" if cell.ok else "red"
    code_lines = cell.code.rstrip().splitlines() or [""]
    first_line = Text()
    first_line.append(status, style=status_style)
    first_line.append(f" {code_lines[0]}")
    if cell.snapshot_text:
        marker = " ▾" if expanded else " ▸"
        first_line.append(marker, style="dim")

    lines: list[Text] = [first_line]
    if len(code_lines) > 1:
        for line in code_lines[1:]:
            lines.append(Text(line))
    if cell.error:
        lines.append(Text(cell.error))
    if expanded and cell.snapshot_text:
        lines.append(Text(""))
        lines.append(Text(cell.snapshot_text))
    return Text("\n").join(lines)
