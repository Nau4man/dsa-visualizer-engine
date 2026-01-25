from textual import events
from textual.app import App, ComposeResult
from rich.text import Text
from textual.containers import Horizontal, VerticalScroll
from textual.widgets import TextArea

from dsa_visualizer.algorithms.runner import AlgorithmRunner
from dsa_visualizer.algorithms.types import AlgorithmStep
from dsa_visualizer.core.executor import Executor
from dsa_visualizer.core.input_accumulator import classify_buffer
from dsa_visualizer.core.snapshotter import Snapshot, Snapshotter, diff_snapshots
from dsa_visualizer.core.types import Cell, MemoryBlock
from dsa_visualizer.data_structures.render.array import render_array
from dsa_visualizer.render.memory_view import get_memory_blocks, render_memory
from dsa_visualizer.ui.cell_render import render_cell_text
from dsa_visualizer.ui.input_area import InputArea
from dsa_visualizer.ui.input_utils import clamp_input_height
from dsa_visualizer.ui.safe_static import NoSelectStatic, SafeStatic
from dsa_visualizer.algorithms.ui.overview import render_algorithm_overview
from dsa_visualizer.data_structures.ui.overview import render_overview
from dsa_visualizer.ui.text_constants import BANNER, INPUT_PLACEHOLDER

MIN_INPUT_LINES = 5
MAX_INPUT_LINES = 10


def _safe_block_id(block_id: str) -> str:
    """Create a DOM-safe id that round-trips for object ids like obj#1."""
    return block_id.replace("#", "__hash__")


def _restore_block_id(safe_id: str) -> str:
    """Restore the original block id from a DOM-safe id."""
    return safe_id.replace("__hash__", "#")


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

    #algorithm-overview-panel {
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

    #welcome-panel {
        padding: 0 1;
        margin: 0 0 1 0;
    }

    """

    def compose(self) -> ComposeResult:
        yield NoSelectStatic(BANNER, id="banner")
        with VerticalScroll(id="content"):
            yield NoSelectStatic(render_overview(), id="overview-panel")
            yield NoSelectStatic(id="algorithm-overview-panel")
            with Horizontal(id="output"):
                with VerticalScroll(id="notebook"):
                    with VerticalScroll(id="notebook-history"):
                        yield NoSelectStatic(
                            self._make_section_title("Code Workspace", "")
                        )
                        yield SafeStatic(self._help_text(), id="help-panel")
                        yield SafeStatic(self._welcome_text(), id="welcome-panel")
                    yield InputArea(placeholder=INPUT_PLACEHOLDER, id="input-cell")
                with VerticalScroll(id="memory"):
                    yield NoSelectStatic(
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
        self._cell_widgets: dict[int, SafeStatic] = {}
        self._cell_expanded: dict[int, bool] = {}
        self._overview_collapsed = False
        self._algorithm_overview_collapsed = True  # Collapsed by default
        # Memory cell tracking
        self._memory_blocks: dict[str, MemoryBlock] = {}
        self._memory_widgets: dict[str, SafeStatic] = {}
        self._memory_expanded: dict[str, bool] = {}
        # Algorithm mode state
        self._algorithm_mode: bool = False
        self._algorithm_runner: AlgorithmRunner | None = None
        self._algorithm_data: list | None = None
        self._algorithm_timer: object | None = None
        self._algorithm_speed: float = 0.7  # seconds between steps
        self._algorithm_run_id: int = 0
        self._algorithm_block_id: str | None = None
        self._render_overview_panel()
        self._render_algorithm_overview_panel()

    def on_key(self, event) -> None:
        # Handle algorithm mode keys first
        if self._algorithm_mode:
            if event.key in ("escape", "q"):
                self._exit_algorithm_mode()
                event.prevent_default()
                return
            elif event.key in ("plus", "equal"):
                # Speed up (reduce interval)
                self._algorithm_speed = max(0.1, self._algorithm_speed - 0.1)
                self._restart_algorithm_timer()
                event.prevent_default()
                return
            elif event.key in ("minus", "underscore"):
                # Slow down (increase interval)
                self._algorithm_speed = min(2.0, self._algorithm_speed + 0.1)
                self._restart_algorithm_timer()
                event.prevent_default()
                return

        # Normal mode keys
        if event.character == "?":
            self._toggle_help()
            event.prevent_default()
        elif event.key == "ctrl+q":
            self.exit()
            event.prevent_default()

    def on_click(self, event: events.Click) -> None:
        if event.widget.id == "overview-panel":
            self._overview_collapsed = not self._overview_collapsed
            # Collapse the other panel when expanding this one
            if not self._overview_collapsed:
                self._algorithm_overview_collapsed = True
                self._render_algorithm_overview_panel()
            self._render_overview_panel()
            return
        if event.widget.id == "algorithm-overview-panel":
            self._algorithm_overview_collapsed = not self._algorithm_overview_collapsed
            # Collapse the other panel when expanding this one
            if not self._algorithm_overview_collapsed:
                self._overview_collapsed = True
                self._render_overview_panel()
            self._render_algorithm_overview_panel()
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
            block_id = _restore_block_id(widget_id)
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

                # Check for pending algorithm
                pending = self._executor.pop_pending_algorithm()
                if pending is not None:
                    self._enter_algorithm_mode(pending.runner, pending.data)
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
        widget = SafeStatic(
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
        newly_added = [block.block_id for block in blocks if block.block_id not in old_block_ids]

        # Remove widgets for blocks that no longer exist
        for block_id in old_block_ids - new_block_ids:
            if block_id.startswith("algorithm_viz_"):
                continue
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
                safe_id = _safe_block_id(block.block_id)
                widget = SafeStatic(
                    render_memory_block_text(block, expanded=expanded),
                    classes="memory-cell",
                    id=f"mem-{safe_id}",
                )
                memory_history.mount(widget)
                self._memory_widgets[block.block_id] = widget

        # Auto-collapse previous blocks when a new block appears
        if newly_added:
            latest_id = newly_added[-1]
            for block_id in list(self._memory_expanded.keys()):
                if block_id != latest_id:
                    self._memory_expanded[block_id] = False
            self._memory_expanded[latest_id] = True
            # Refresh visible widgets after collapse
            for block_id, widget in self._memory_widgets.items():
                block = self._memory_blocks.get(block_id)
                if block is not None:
                    widget.update(
                        render_memory_block_text(
                            block, expanded=self._memory_expanded.get(block_id, True)
                        )
                    )

        memory = self.query_one("#memory", VerticalScroll)
        self.call_after_refresh(memory.scroll_end, animate=False)
        content = self.query_one("#content", VerticalScroll)
        self.call_after_refresh(content.scroll_end, animate=False)

    def _toggle_help(self) -> None:
        panel = self.query_one("#help-panel", SafeStatic)
        showing = panel.styles.display != "none"
        panel.styles.display = "none" if showing else "block"
        if not showing:
            notebook = self.query_one("#notebook-history", VerticalScroll)
            self.call_after_refresh(notebook.scroll_home, animate=False)
            content = self.query_one("#content", VerticalScroll)
            self.call_after_refresh(content.scroll_home, animate=False)

    def toggle_help(self) -> None:
        self._toggle_help()

    def _help_text(self) -> Text:
        text = Text()
        text.append("DSA Visualizer", style="bold #3cbf5a")
        text.append(" - Interactive Data Structure & Algorithm Explorer\n\n")

        text.append("GETTING STARTED\n", style="bold")
        text.append("  Type Python code in the input area below.\n")
        text.append("  Data structures and algorithm steps visualized on the right.\n")
        text.append("  See ", style="dim")
        text.append("Data Structures", style="bold")
        text.append(" and ", style="dim")
        text.append("Algorithms", style="bold")
        text.append(" panels above for reference.\n\n", style="dim")

        text.append("KEYBOARD SHORTCUTS\n", style="bold")
        text.append("  Enter       Run code (when complete)\n")
        text.append("  Ctrl+Enter  Force run\n")
        text.append("  ?           Toggle this help\n")
        text.append("  Ctrl+Q      Quit\n")
        text.append("  Shift+Drag  Select text, then Ctrl+C to copy\n\n")

        text.append("ALGORITHM MODE ", style="bold")
        text.append("(during visualization)\n", style="dim")
        text.append("  +           Speed up animation\n")
        text.append("  -           Slow down animation\n")
        text.append("  Esc         Stop and exit\n")

        return text

    def _welcome_text(self) -> Text:
        text = Text()
        text.append("Type Python code below to visualize data structures and algorithms. ")
        text.append("Press ", style="dim")
        text.append("?", style="bold")
        text.append(" for help.", style="dim")
        return text

    def _render_overview_panel(self) -> None:
        panel = self.query_one("#overview-panel", NoSelectStatic)
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

    def _render_algorithm_overview_panel(self) -> None:
        panel = self.query_one("#algorithm-overview-panel", NoSelectStatic)
        if self._algorithm_overview_collapsed:
            text = Text()
            text.append("▶ Algorithms", style="bold #3cbf5a")
            text.append("  · click to expand", style="dim")
            panel.update(text)
        else:
            text = Text()
            text.append("▼ Algorithms", style="bold #3cbf5a")
            text.append("  · click to collapse", style="dim")
            text.append("\n")
            text.append(render_algorithm_overview())
            panel.update(text)

    # Algorithm mode methods

    def _enter_algorithm_mode(
        self, runner: AlgorithmRunner, data: list
    ) -> None:
        """Enter algorithm visualization mode with auto-animation."""
        self._algorithm_mode = True
        self._algorithm_runner = runner
        self._algorithm_data = data
        self._algorithm_run_id += 1
        self._algorithm_block_id = f"algorithm_viz_{self._algorithm_run_id}"
        # Advance to first step and render
        self._algorithm_runner.advance()
        self._render_algorithm_step()
        # Start animation timer
        self._algorithm_timer = self.set_interval(
            self._algorithm_speed, self._auto_step
        )

    def _exit_algorithm_mode(self) -> None:
        """Exit algorithm visualization mode."""
        # Stop animation timer
        if self._algorithm_timer is not None:
            self._algorithm_timer.stop()
            self._algorithm_timer = None
        self._algorithm_mode = False
        self._algorithm_runner = None
        self._algorithm_data = None
        self._algorithm_block_id = None
        # Clear algorithm panel if it exists
        try:
            panel = self.query_one("#algorithm-panel", SafeStatic)
            panel.styles.display = "none"
        except Exception:
            pass
        # Keep algorithm visualization block visible after completion.

    def _render_algorithm_step(self) -> None:
        """Render the current algorithm step."""
        if self._algorithm_runner is None:
            return

        step = self._algorithm_runner.current()
        if step is None:
            return

        # Render the algorithm panel (step info)
        self._render_algorithm_panel(step)

        # Render the data structure with highlights
        self._render_algorithm_visualization(step)

    def _render_algorithm_panel(self, step: AlgorithmStep) -> None:
        """Render the algorithm info panel."""
        runner = self._algorithm_runner
        if runner is None:
            return

        text = Text()
        text.append(f"Algorithm: {runner.name}\n", style="bold #f6c64a")

        # Step counter
        if runner.total_steps is not None:
            text.append(f"Step {runner.step_number} of {runner.total_steps}\n")
        else:
            text.append(f"Step {runner.step_number}\n")

        # Current action
        text.append(f"\n{step.action}\n", style="bold")

        # Controls hint
        text.append("\nControls: ", style="dim")
        text.append("+", style="bold")
        text.append("=Faster  ", style="dim")
        text.append("-", style="bold")
        text.append("=Slower  ", style="dim")
        text.append("Esc", style="bold")
        text.append("=Stop", style="dim")

        # Update or create the panel
        try:
            panel = self.query_one("#algorithm-panel", SafeStatic)
            panel.update(text)
            panel.styles.display = "block"
        except Exception:
            # Panel doesn't exist yet, that's ok for now
            pass

    def _render_algorithm_visualization(self, step: AlgorithmStep) -> None:
        """Render the data structure with algorithm highlights."""
        if not isinstance(step.data, list):
            return

        # Render array with highlights
        content = render_array(step.data, highlights=step.highlights)

        block_id = self._algorithm_block_id or "algorithm_viz"
        # Create a memory block for display
        block = MemoryBlock(
            block_id=block_id,
            header="Array ──▶ searching",
            summary=f"Step {step.step_number}",
            content=content,
        )

        # Update memory view to show this
        memory_history = self.query_one("#memory-history", VerticalScroll)

        is_new_block = block.block_id not in self._memory_expanded
        if is_new_block:
            # Collapse all previous blocks when a new algorithm block is added
            for existing_id in list(self._memory_expanded.keys()):
                self._memory_expanded[existing_id] = False
            self._memory_expanded[block.block_id] = True
        expanded = self._memory_expanded.get(block.block_id, True)

        # Create or update the algorithm visualization widget
        # First check if widget exists in DOM
        try:
            safe_id = _safe_block_id(block.block_id)
            existing_widget = self.query_one(f"#mem-{safe_id}", SafeStatic)
            existing_widget.update(render_memory_block_text(block, expanded=expanded))
            self._memory_widgets[block.block_id] = existing_widget
            self._memory_blocks[block.block_id] = block
        except Exception:
            # Widget doesn't exist, create it
            safe_id = _safe_block_id(block.block_id)
            widget = SafeStatic(
                render_memory_block_text(block, expanded=expanded),
                classes="memory-cell",
                id=f"mem-{safe_id}",
            )
            memory_history.mount(widget)
            self._memory_widgets[block.block_id] = widget
            self._memory_blocks[block.block_id] = block

    def _auto_step(self) -> None:
        """Automatically advance to the next step (called by timer)."""
        if self._algorithm_runner is None:
            return

        # Check if current step is complete
        current = self._algorithm_runner.current()
        if current is not None and current.is_complete:
            # Algorithm finished, stop animation after a brief pause
            self._exit_algorithm_mode()
            return

        # Advance to next step
        step = self._algorithm_runner.advance()
        if step is not None:
            self._render_algorithm_step()
            # Check if this step completes the algorithm
            if step.is_complete:
                # Keep showing for a moment, then exit
                if self._algorithm_timer is not None:
                    self._algorithm_timer.stop()
                self.set_timer(1.5, self._exit_algorithm_mode)
        else:
            # No more steps, exit
            self._exit_algorithm_mode()

    def _restart_algorithm_timer(self) -> None:
        """Restart the animation timer with current speed."""
        if self._algorithm_timer is not None:
            self._algorithm_timer.stop()
        self._algorithm_timer = self.set_interval(
            self._algorithm_speed, self._auto_step
        )

    @property
    def algorithm_mode(self) -> bool:
        """Whether the app is in algorithm visualization mode."""
        return self._algorithm_mode


def main() -> None:
    """Entry point for the DSA Visualizer Engine."""
    DSAApp().run()


if __name__ == "__main__":
    main()
