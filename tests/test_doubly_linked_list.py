from dsa_visualizer.data_structures.implementations.structures import DoublyLinkedList


def test_delete_middle_node() -> None:
    dll = DoublyLinkedList(["A", "B", "C"])
    assert dll.delete("B") is True
    assert dll.head is not None
    assert dll.head.data == "A"
    assert dll.head.next is not None
    assert dll.head.next.data == "C"
    assert dll.head.next.prev is dll.head
    assert len(dll) == 2


def test_delete_head_node() -> None:
    dll = DoublyLinkedList(["A", "B"])
    assert dll.delete("A") is True
    assert dll.head is not None
    assert dll.head.data == "B"
    assert dll.head.prev is None
    assert dll.tail is dll.head
    assert len(dll) == 1


def test_delete_tail_node() -> None:
    dll = DoublyLinkedList(["A", "B"])
    assert dll.delete("B") is True
    assert dll.tail is not None
    assert dll.tail.data == "A"
    assert dll.tail.next is None
    assert dll.head is dll.tail
    assert len(dll) == 1


def test_delete_missing_value() -> None:
    dll = DoublyLinkedList(["A", "B"])
    assert dll.delete("Z") is False
    assert len(dll) == 2
