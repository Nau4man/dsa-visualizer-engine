from dsa_visualizer.core.types import Cell


def append_cell(cells: list[Cell], code: str) -> Cell:
    cell = Cell(cell_id=len(cells) + 1, code=code)
    cells.append(cell)
    return cell


def test_append_cells_increments_ids() -> None:
    cells: list[Cell] = []
    first = append_cell(cells, "x=1")
    second = append_cell(cells, "x=2")
    assert first.cell_id == 1
    assert second.cell_id == 2


def test_append_cells_preserves_order() -> None:
    cells: list[Cell] = []
    append_cell(cells, "a=1")
    append_cell(cells, "b=2")
    assert [cell.code for cell in cells] == ["a=1", "b=2"]
