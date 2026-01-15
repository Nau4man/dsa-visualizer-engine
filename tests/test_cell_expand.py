from dsa_visualizer.core.types import Cell
from dsa_visualizer.ui.cell_render import render_cell_text


def test_cell_render_collapsed_hides_snapshot() -> None:
    cell = Cell(cell_id=1, code="x=1", ok=True, snapshot_text="snap")
    text = render_cell_text(cell, expanded=False).plain
    assert "snap" not in text


def test_cell_render_expanded_shows_snapshot() -> None:
    cell = Cell(cell_id=1, code="x=1", ok=True, snapshot_text="snap")
    text = render_cell_text(cell, expanded=True).plain
    assert "snap" in text
