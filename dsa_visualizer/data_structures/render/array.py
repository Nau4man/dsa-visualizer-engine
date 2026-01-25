from __future__ import annotations

from dsa_visualizer.algorithms.types import HighlightContext
from dsa_visualizer.algorithms.render.highlights import (
    get_index_marker,
    is_at_left_boundary,
    is_at_right_boundary,
)


def render_array(
    values: list[object],
    highlights: HighlightContext | None = None,
) -> str:
    """Render an array as an ASCII table.

    Args:
        values: The array values to render.
        highlights: Optional highlight context for algorithm visualization.

    Returns:
        ASCII string representation of the array.
    """
    if not values:
        return "(empty)"

    # Calculate cell width, accounting for possible markers
    max_len = 1
    for index, value in enumerate(values):
        index_str = str(index)
        # Add space for marker if highlights provided
        if highlights is not None:
            marker = get_index_marker(index, highlights)
            if marker:
                index_str = f"{marker}{index}"
        max_len = max(max_len, len(index_str), len(str(value)))

    cell_width = max_len + 3
    prefix = "Index → "
    spacer = " " * len(prefix)

    def cell(text: str) -> str:
        return f" {text} ".ljust(cell_width)

    def border(
        left: str, mid: str, right: str, highlight_indices: set[int] | None = None
    ) -> str:
        segments = [left]
        segments.append("─" * cell_width)
        for i in range(1, len(values)):
            segments.append(mid)
            segments.append("─" * cell_width)
        segments.append(right)
        return "".join(segments)

    # Build top border with optional boundary markers
    if highlights is not None and highlights.boundaries is not None:
        top = _build_boundary_border(
            "┌", "┬", "┐", cell_width, len(values), highlights
        )
        bottom = _build_boundary_border(
            "└", "┴", "┘", cell_width, len(values), highlights
        )
    else:
        top = border("┌", "┬", "┐")
        bottom = border("└", "┴", "┘")

    middle = border("├", "┼", "┤")

    # Build index cells with markers
    index_cells = []
    for index in range(len(values)):
        if highlights is not None:
            marker = get_index_marker(index, highlights)
            if marker:
                index_cells.append(cell(f"{marker}{index}"))
            else:
                index_cells.append(cell(str(index)))
        else:
            index_cells.append(cell(str(index)))

    value_cells = [cell(str(value)) for value in values]

    lines = [
        f"{spacer}{top}",
        f"{prefix}│{'│'.join(index_cells)}│",
        f"{spacer}{middle}",
        f"{'Array → '}│{'│'.join(value_cells)}│",
        f"{spacer}{bottom}",
    ]
    return "\n".join(lines)


def _build_boundary_border(
    left: str,
    mid: str,
    right: str,
    cell_width: int,
    count: int,
    highlights: HighlightContext,
) -> str:
    """Build border with boundary markers.

    Shows [ at left boundary and ] at right boundary.
    """
    segments = []

    for i in range(count):
        # Left edge of cell
        if i == 0:
            if is_at_left_boundary(i, highlights):
                segments.append("[")
            else:
                segments.append(left)
        else:
            if is_at_left_boundary(i, highlights):
                segments.append("[")
            else:
                segments.append(mid)

        # Cell content (dashes)
        segments.append("─" * cell_width)

        # Check if this cell is the right boundary (add ] after it)
        if is_at_right_boundary(i, highlights) and i < count - 1:
            segments.append("]")
            # Skip the next separator since we added ]
            continue

    # Right edge of last cell
    if is_at_right_boundary(count - 1, highlights):
        segments.append("]")
    else:
        segments.append(right)

    return "".join(segments)
