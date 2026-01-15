from textual import events
from textual.app import App, ComposeResult
from rich.text import Text
from textual.containers import Horizontal, VerticalScroll
from textual.widgets import Static, TextArea

from dsa_visualizer.core.executor import Executor
from dsa_visualizer.core.input_accumulator import classify_buffer
from dsa_visualizer.core.snapshotter import Snapshot, Snapshotter, diff_snapshots
from dsa_visualizer.render.memory_view import render_memory
from dsa_visualizer.core.types import Cell
from dsa_visualizer.ui.cell_render import render_cell_text
from dsa_visualizer.ui.input_area import InputArea
from dsa_visualizer.ui.input_utils import clamp_input_height
from dsa_visualizer.ui.overview import render_heading, render_overview
from dsa_visualizer.ui.text_constants import BANNER, INPUT_PLACEHOLDER

MIN_INPUT_LINES = 5
MAX_INPUT_LINES = 10


class DSAApp(App):
    CSS = """
    Screen {
        layout: vertical;
        scrollbar-visibility: hidden;
    }

    VerticalScroll {
        scrollbar-visibility: hidden;
        scrollbar-gutter: auto;
        scrollbar-size-vertical: 0;
    }

    #banner {
        color: #3cbf5a;
        content-align: center middle;
        height: 3;
        text-align: center;
    }

    #heading {
        height: 1;
    }

    #content {
        height: 1fr;
    }

    #overview-panel {
        border: round #2f2f2f;
        padding: 0 1;
    }

    #overview {
        padding: 0 1;
    }

    #output {
        layout: horizontal;
        padding: 0 1;
    }

    #notebook {
        width: 1fr;
        border: round #2f2f2f;
        padding: 0 1;
    }

    #notebook-history {
        height: 1fr;
    }

    #memory {
        width: 1fr;
        border: round #2f2f2f;
        padding: 0 1;
    }

    #input-cell {
        border: round #3cbf5a;
        height: 5;
    }

    .cell-output {
        border: round #3a3a3a;
        padding: 0 1;
        margin: 0 0 0 0;
    }

    #help-panel {
        display: none;
        border: round #2f2f2f;
        padding: 0 1;
        margin: 0 0 1 0;
    }

    """

    def compose(self) -> ComposeResult:
        yield Static(BANNER, id="banner")
        yield Static(render_heading(), id="heading")
        with VerticalScroll(id="content"):
            yield Static(render_overview(), id="overview-panel")
            with Horizontal(id="output"):
                with VerticalScroll(id="notebook"):
                    with VerticalScroll(id="notebook-history"):
                        yield Static(self._make_section_title("Code Workspace", ""))
                        yield Static(self._help_text(), id="help-panel")
                    yield InputArea(placeholder=INPUT_PLACEHOLDER, id="input-cell")
                with VerticalScroll(id="memory"):
                    yield Static(
                        self._make_section_title(
                            "Data Structures Visualization", "in real time"
                        )
                    )
                    yield Static("", id="memory-body", markup=False)

    def on_text_area_changed(self, event: TextArea.Changed) -> None:
        text_area = event.text_area
        text = text_area.text
        if text.strip() == "" and text != "":
            text_area.text = ""
            return
        height = clamp_input_height(text_area.text, MIN_INPUT_LINES, MAX_INPUT_LINES)
        text_area.styles.height = height

    def on_mount(self) -> None:
        self._cells: list[Cell] = []
        self._executor = Executor()
        self._snapshotter = Snapshotter()
        self._last_snapshot = self._snapshotter.snapshot(self._executor.globals)
        self._cell_widgets: dict[int, Static] = {}
        self._cell_expanded: dict[int, bool] = {}
        self._overview_collapsed = False
        self._render_overview_panel()

    def on_key(self, event) -> None:
        if event.key == "?":
            self._toggle_help()
            event.prevent_default()
        elif event.key == "ctrl+q":
            self.exit()
            event.prevent_default()

    def on_click(self, event: events.Click) -> None:
        if event.widget.id == "overview-panel":
            self._overview_collapsed = not self._overview_collapsed
            self._render_overview_panel()
            return
        if event.widget.id and event.widget.id.startswith("cell-"):
            try:
                cell_id = int(event.widget.id.split("-", 1)[1])
            except ValueError:
                return
            cell = next((item for item in self._cells if item.cell_id == cell_id), None)
            if cell is None or not cell.snapshot_text:
                return
            expanded = not self._cell_expanded.get(cell_id, False)
            self._cell_expanded[cell_id] = expanded
            widget = self._cell_widgets.get(cell_id)
            if widget is not None:
                widget.update(render_cell_text(cell, expanded=expanded))

    def handle_code_enter(self, *, force_submit: bool) -> bool:
        text_area = self.query_one("#input-cell", InputArea)
        result = classify_buffer(text_area.text, force_submit=force_submit)
        if result.status == "incomplete":
            return False
        if result.status == "error":
            self._append_cell(text_area.text, ok=False, error=result.error)
        else:
            execution = self._executor.execute(text_area.text)
            snapshot_text = None
            if execution.ok:
                snapshot = self._snapshotter.snapshot(self._executor.globals)
                delta = diff_snapshots(self._last_snapshot, snapshot)
                self._update_memory(snapshot)
                snapshot_text = render_memory(delta) or "(no changes)"
                self._last_snapshot = snapshot
            self._append_cell(
                text_area.text,
                ok=execution.ok,
                error=execution.error,
                snapshot_text=snapshot_text,
            )
        text_area.text = ""
        text_area.scroll_visible()
        return True

    def _append_cell(
        self,
        code: str,
        *,
        ok: bool,
        error: str | None,
        snapshot_text: str | None = None,
    ) -> None:
        cell = Cell(
            cell_id=len(self._cells) + 1,
            code=code,
            ok=ok,
            error=error,
            snapshot_text=snapshot_text,
        )
        self._cells.append(cell)
        notebook = self.query_one("#notebook-history", VerticalScroll)
        widget = Static(
            render_cell_text(cell, expanded=False),
            classes="cell-output",
            id=f"cell-{cell.cell_id}",
        )
        notebook.mount(widget)
        self._cell_widgets[cell.cell_id] = widget
        self._cell_expanded[cell.cell_id] = False
        self.call_after_refresh(notebook.scroll_end, animate=False)
        content = self.query_one("#content", VerticalScroll)
        self.call_after_refresh(content.scroll_end, animate=False)

    def _make_section_title(self, title: str, subtitle: str) -> Text:
        text = Text()
        text.append("▌", style="bold #3cbf5a")
        text.append(f" {title}", style="bold")
        if subtitle:
            text.append("  · ", style="dim")
            text.append(subtitle, style="dim")
        return text

    def _update_memory(self, snapshot: Snapshot) -> None:
        memory_body = self.query_one("#memory-body", Static)
        memory_body.update(render_memory(snapshot))
        memory = self.query_one("#memory", VerticalScroll)
        self.call_after_refresh(memory.scroll_end, animate=False)
        content = self.query_one("#content", VerticalScroll)
        self.call_after_refresh(content.scroll_end, animate=False)

    def _toggle_help(self) -> None:
        panel = self.query_one("#help-panel", Static)
        panel.styles.display = "none" if panel.styles.display != "none" else "block"

    def toggle_help(self) -> None:
        self._toggle_help()

    def _help_text(self) -> Text:
        text = Text()
        text.append("Shortcuts\n", style="bold")
        text.append("• Enter: run when complete / new line when incomplete\n")
        text.append("• Ctrl+Enter: force run\n")
        text.append("• ?: toggle help\n")
        text.append("• Ctrl+Q: quit\n")
        return text

    def _render_overview_panel(self) -> None:
        panel = self.query_one("#overview-panel", Static)
        if self._overview_collapsed:
            text = Text()
            text.append("▶ Data Structures", style="bold #3cbf5a")
            text.append("  · click to expand", style="dim")
            panel.update(text)
        else:
            text = Text()
            text.append("▼ Data Structures", style="bold #3cbf5a")
            text.append("  · click to collapse", style="dim")
            text.append("\n")
            text.append(render_overview())
            panel.update(text)



def main() -> None:
    """Entry point for the DSA Visualizer Engine."""
    DSAApp().run()


if __name__ == "__main__":
    main()
