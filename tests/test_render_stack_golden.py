from dsa_visualizer.data_structures.render.stack import render_stack


def test_render_stack_four_items() -> None:
    expected = (
        "Top\n"
        " │\n"
        " ▼\n"
        "┌─────┐\n"
        "│  D  │\n"
        "├─────┤\n"
        "│  C  │\n"
        "├─────┤\n"
        "│  B  │\n"
        "├─────┤\n"
        "│  A  │\n"
        "└─────┘"
    )
    assert render_stack(["A", "B", "C", "D"]) == expected


def test_render_stack_empty() -> None:
    expected = "Top\n │\n ▼\n(empty)"
    assert render_stack([]) == expected
