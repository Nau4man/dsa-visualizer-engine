"""Algorithm style converter for Rich text styling.

Converts ASCII text with highlight markers to Rich Text with styles.
"""

from __future__ import annotations

from rich.text import Text

from dsa_visualizer.algorithms.render.highlights import (
    MARKER_CURRENT,
    MARKER_VISITED,
    MARKER_FOUND,
    MARKER_COMPARING,
    MARKER_ELIMINATED,
    MARKER_BOUNDARY_L,
    MARKER_BOUNDARY_R,
)


# Style mappings for markers
MARKER_STYLES = {
    MARKER_CURRENT: "bold yellow",
    MARKER_VISITED: "dim",
    MARKER_FOUND: "bold green",
    MARKER_COMPARING: "bold cyan",
    MARKER_ELIMINATED: "dim red",
    MARKER_BOUNDARY_L: "bold magenta",
    MARKER_BOUNDARY_R: "bold magenta",
}


def apply_algorithm_styles(ascii_text: str) -> Text:
    """Convert ASCII text with markers to styled Rich Text.

    Scans the text for marker characters and applies appropriate styles.

    Args:
        ascii_text: Plain ASCII text with embedded markers.

    Returns:
        Rich Text object with styles applied to markers.
    """
    text = Text()
    i = 0

    while i < len(ascii_text):
        char = ascii_text[i]

        if char in MARKER_STYLES:
            style = MARKER_STYLES[char]
            text.append(char, style=style)

            # For current/comparing markers, also style the following number
            if char in (MARKER_CURRENT, MARKER_FOUND, MARKER_COMPARING, MARKER_VISITED):
                # Look ahead for digits
                j = i + 1
                while j < len(ascii_text) and ascii_text[j].isdigit():
                    j += 1
                if j > i + 1:
                    number = ascii_text[i + 1 : j]
                    text.append(number, style=style)
                    i = j
                    continue
        else:
            text.append(char)

        i += 1

    return text


def style_index_cell(index: int, marker: str) -> Text:
    """Create a styled index cell for display.

    Args:
        index: The array index.
        marker: The marker character (or empty string).

    Returns:
        Rich Text object with styled index.
    """
    text = Text()

    if marker:
        style = MARKER_STYLES.get(marker, "")
        text.append(marker, style=style)
        text.append(str(index), style=style)
    else:
        text.append(str(index))

    return text


def get_legend_text() -> Text:
    """Create legend text explaining the markers.

    Returns:
        Rich Text with styled legend.
    """
    text = Text()
    text.append("Legend: ")

    text.append(MARKER_CURRENT, style=MARKER_STYLES[MARKER_CURRENT])
    text.append("=current  ", style="dim")

    text.append(MARKER_COMPARING, style=MARKER_STYLES[MARKER_COMPARING])
    text.append("=comparing  ", style="dim")

    text.append(MARKER_VISITED, style=MARKER_STYLES[MARKER_VISITED])
    text.append("=visited  ", style="dim")

    text.append(MARKER_FOUND, style=MARKER_STYLES[MARKER_FOUND])
    text.append("=found  ", style="dim")

    text.append("[", style=MARKER_STYLES[MARKER_BOUNDARY_L])
    text.append("]", style=MARKER_STYLES[MARKER_BOUNDARY_R])
    text.append("=boundaries", style="dim")

    return text
