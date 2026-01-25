from dsa_visualizer.data_structures.implementations.structures import LinkedList
from dsa_visualizer.data_structures.render.linked_list import render_linked_list


def test_render_linked_list_three_nodes() -> None:
    LinkedList._reset_address_counter()
    linked_list = LinkedList(["A", "B", "C"])
    head = linked_list.head
    assert head is not None
    assert head.next is not None
    next_address = hex(id(head.next))
    data_width = max(8, len("data"), len("A"))
    next_width = max(8, len("next"), len(next_address))
    top = f"┌{'─' * data_width}┬{'─' * next_width}┐"
    header = f"│{'data'.center(data_width)}│{'next'.center(next_width)}│"
    bottom = f"└{'─' * data_width}┴{'─' * next_width}┘"
    row = f" {'A'.center(data_width)} {next_address.center(next_width)}"
    expected = (
        "Head ──▶ ┌────┬─────┐ ──▶ ┌────┬─────┐ ──▶ ┌────┬─────┐\n"
        "         │ A  │  •  │     │ B  │  •  │     │ C  │ NULL│\n"
        "         └────┴─────┘     └────┴─────┘     └────┴─────┘\n"
        "\n"
        "Node Structure\n"
        f"{top}\n"
        f"{header}\n"
        f"{bottom}\n"
        f"{row}"
    )
    assert render_linked_list(linked_list) == expected
