from __future__ import annotations

from rich.text import Text
from textual.content import Content
from textual.selection import Selection
from textual.widgets import Static


class SafeStatic(Static):
    """Static that ignores out-of-range selections to avoid copy crashes."""

    def get_selection(self, selection: Selection) -> tuple[str, str] | None:
        visual = self._render()
        if isinstance(visual, (Text, Content)):
            text = str(visual)
        else:
            return None

        if selection.start is None:
            return None

        lines = text.splitlines() or [""]
        max_line_index = len(lines) - 1
        if selection.start.y > max_line_index:
            return None
        if selection.end is not None and selection.end.y > max_line_index:
            return None

        try:
            return selection.extract(text), "\n"
        except IndexError:
            return None


class NoSelectStatic(SafeStatic):
    """Static that opts out of text selection entirely."""

    ALLOW_SELECT = False
