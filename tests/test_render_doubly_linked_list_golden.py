from dsa_visualizer.data_structures.implementations.structures import DoublyLinkedList
from dsa_visualizer.data_structures.render.doubly_linked_list import render_doubly_linked_list


def test_render_doubly_linked_list_three_nodes() -> None:
    linked_list = DoublyLinkedList(["A", "B", "C"])
    head = linked_list.head
    assert head is not None
    assert head.next is not None
    next_address = hex(id(head.next))
    prev_address = "NULL"
    prev_width = max(8, len("prev"), len(prev_address))
    data_width = max(8, len("data"), len("A"))
    next_width = max(8, len("next"), len(next_address))
    top = f"┌{'─' * prev_width}┬{'─' * data_width}┬{'─' * next_width}┐"
    header = (
        f"│{'prev'.center(prev_width)}│{'data'.center(data_width)}│"
        f"{'next'.center(next_width)}│"
    )
    bottom = f"└{'─' * prev_width}┴{'─' * data_width}┴{'─' * next_width}┘"
    row = (
        f" {prev_address.center(prev_width)} "
        f"{'A'.center(data_width)} "
        f"{next_address.center(next_width)}"
    )
    expected = (
        "Head ──▶ ┌─────┬────┬─────┐ ⇄ ┌─────┬────┬─────┐ ⇄ ┌─────┬────┬─────┐\n"
        "         │NULL │ A  │  •  │   │  •  │ B  │  •  │   │  •  │ C  │NULL │\n"
        "         └─────┴────┴─────┘   └─────┴────┴─────┘   └─────┴────┴─────┘\n"
        "\n"
        "Node Structure\n"
        f"{top}\n"
        f"{header}\n"
        f"{bottom}\n"
        f"{row}"
    )
    assert render_doubly_linked_list(linked_list) == expected
