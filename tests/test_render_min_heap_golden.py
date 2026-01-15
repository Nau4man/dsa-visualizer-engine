from dsa_visualizer.core.structures import MinHeap
from dsa_visualizer.render.min_heap import render_min_heap


def test_render_min_heap_sample() -> None:
    heap = MinHeap([1, 3, 5, 7, 9])
    expected = (
        "           [1]\n"
        "            ▼\n"
        "      ┌─────────────┐\n"
        "      ▼             ▼\n"
        "     [3]           [5]\n"
        "      ▼\n"
        "   ┌───────┐\n"
        "   ▼       ▼\n"
        "  [7]     [9]"
    )
    assert render_min_heap(heap.items()) == expected


def test_render_min_heap_empty() -> None:
    assert render_min_heap([]) == "(empty)"
