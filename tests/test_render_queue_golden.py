from dsa_visualizer.render.queue import render_queue


def test_render_queue_four_items() -> None:
    expected = (
        "Front ──▶ ┌─────┬─────┬─────┬─────┐ ──▶ Rear\n"
        "          │  A  │  B  │  C  │  D  │\n"
        "          └─────┴─────┴─────┴─────┘"
    )
    assert render_queue(["A", "B", "C", "D"]) == expected


def test_render_queue_empty() -> None:
    expected = "Front ──▶ (empty) ──▶ Rear"
    assert render_queue([]) == expected
