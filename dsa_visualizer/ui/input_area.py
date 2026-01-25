from textual.binding import Binding
from textual.widgets import TextArea

from dsa_visualizer.ui.input_utils import indent_for_newline


class InputArea(TextArea):
    BINDINGS = [
        *TextArea.BINDINGS,
        Binding("ctrl+a", "select_all", "Select all", priority=True),
    ]

    def on_key(self, event) -> None:
        if event.character == "?":
            handler = getattr(self.app, "toggle_help", None)
            if callable(handler):
                handler()
            event.prevent_default()
            event.stop()
            return
        if event.key == "ctrl+enter":
            handler = getattr(self.app, "handle_code_enter", None)
            if callable(handler):
                handler(force_submit=True)
            event.prevent_default()
            return
        if event.key == "enter":
            line_index, _column = self.cursor_location
            lines = self.text.split("\n")
            line = lines[line_index] if line_index < len(lines) else ""
            indent = indent_for_newline(line)
            if indent is not None:
                self.insert(f"\n{indent}")
                event.prevent_default()
                return
            handler = getattr(self.app, "handle_code_enter", None)
            if callable(handler):
                if handler(force_submit=False):
                    event.prevent_default()
