from textual import events
from textual.app import App, ComposeResult
from rich.text import Text
from textual.containers import Horizontal, VerticalScroll
from textual.widgets import Static, TextArea

from dsa_visualizer.core.executor import Executor
from dsa_visualizer.core.input_accumulator import classify_buffer
from dsa_visualizer.core.snapshotter import Snapshot, Snapshotter, diff_snapshots
from dsa_visualizer.core.types import Cell, MemoryBlock
from dsa_visualizer.render.memory_view import get_memory_blocks, render_memory
from dsa_visualizer.ui.cell_render import render_cell_text
from dsa_visualizer.ui.input_area import InputArea
from dsa_visualizer.ui.input_utils import clamp_input_height
from dsa_visualizer.ui.overview import render_overview
from dsa_visualizer.ui.text_constants import BANNER, INPUT_PLACEHOLDER

MIN_INPUT_LINES = 5
MAX_INPUT_LINES = 10


def render_memory_block_text(block: MemoryBlock, *, expanded: bool) -> Text:
    """Render a memory block with expand/collapse support."""
    marker = " ▾" if expanded else " ▸"

    text = Text()
    # First line of header with marker
    header_lines = block.header.split("\n")
    text.append(header_lines[0])
    text.append(marker, style="dim")

    # Additional header lines (for aliased variables)
    for line in header_lines[1:]:
        text.append("\n")
        text.append(line)

    # Show content if expanded
    if expanded:
        text.append("\n")
        text.append(block.content)

    return text


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

    #memory-history {
        height: 1fr;
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

    .memory-cell {
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
                    with VerticalScroll(id="memory-history"):
                        pass  # Memory cells will be mounted here

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
        # Memory cell tracking
        self._memory_blocks: dict[str, MemoryBlock] = {}
        self._memory_widgets: dict[str, Static] = {}
        self._memory_expanded: dict[str, bool] = {}
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
        # Handle code cell clicks
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
            return
        # Handle memory cell clicks
        if event.widget.id and event.widget.id.startswith("mem-"):
            widget_id = event.widget.id[4:]  # Remove "mem-" prefix
            block_id = widget_id.replace("_", "#", 1)  # Restore obj#N format
            block = self._memory_blocks.get(block_id)
            if block is None:
                return
            expanded = not self._memory_expanded.get(block_id, True)
            self._memory_expanded[block_id] = expanded
            widget = self._memory_widgets.get(block_id)
            if widget is not None:
                widget.update(render_memory_block_text(block, expanded=expanded))

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
        """Update memory view with individual expandable cells."""
        memory_history = self.query_one("#memory-history", VerticalScroll)

        # Get current blocks
        blocks = get_memory_blocks(snapshot)
        new_block_ids = {block.block_id for block in blocks}
        old_block_ids = set(self._memory_blocks.keys())

        # Remove widgets for blocks that no longer exist
        for block_id in old_block_ids - new_block_ids:
            widget = self._memory_widgets.pop(block_id, None)
            if widget is not None:
                widget.remove()
            self._memory_blocks.pop(block_id, None)
            self._memory_expanded.pop(block_id, None)

        # Update or add widgets for current blocks
        for block in blocks:
            self._memory_blocks[block.block_id] = block

            # Default to expanded for new blocks
            if block.block_id not in self._memory_expanded:
                self._memory_expanded[block.block_id] = True

            expanded = self._memory_expanded[block.block_id]

            if block.block_id in self._memory_widgets:
                # Update existing widget
                widget = self._memory_widgets[block.block_id]
                widget.update(render_memory_block_text(block, expanded=expanded))
            else:
                # Create new widget (sanitize ID: replace # with _)
                safe_id = block.block_id.replace("#", "_")
                widget = Static(
                    render_memory_block_text(block, expanded=expanded),
                    classes="memory-cell",
                    id=f"mem-{safe_id}",
                )
                memory_history.mount(widget)
                self._memory_widgets[block.block_id] = widget

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
