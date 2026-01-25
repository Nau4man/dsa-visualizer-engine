from dsa_visualizer.core.snapshotter import Snapshotter
from dsa_visualizer.render.memory_view import render_memory


class QueueNode:
    def __init__(self, value: object) -> None:
        self.value = value
        self.next = None


class LinkedList:
    def __init__(self) -> None:
        self.head = None

    def append(self, value: object) -> None:
        new_node = Node(value)
        if self.head is None:
            self.head = new_node
            return
        curr = self.head
        while curr.next:
            curr = curr.next
        curr.next = new_node


def test_structural_linked_list_rendering() -> None:
    linked_list = LinkedList()
    linked_list.append("A")
    linked_list.append("B")
    assert linked_list.head is not None
    assert linked_list.head.next is not None
    next_address = hex(id(linked_list.head.next))

    snapshotter = Snapshotter()
    snapshot = snapshotter.snapshot({"lst": linked_list})
    rendered = render_memory(snapshot)

    assert "lst ──▶ Linked List" in rendered
    assert "Node Structure" in rendered
    assert next_address in rendered


class DNode:
    def __init__(self, value: object) -> None:
        self.value = value
        self.prev = None
        self.next = None


class DoublyLinkedList:
    def __init__(self) -> None:
        self.head = None
        self.tail = None

    def append(self, value: object) -> None:
        new_node = DNode(value)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
            return
        assert self.tail is not None
        new_node.prev = self.tail
        self.tail.next = new_node
        self.tail = new_node


def test_structural_doubly_linked_list_rendering() -> None:
    linked_list = DoublyLinkedList()
    linked_list.append("A")
    linked_list.append("B")
    assert linked_list.head is not None
    assert linked_list.head.next is not None
    next_address = hex(id(linked_list.head.next))

    snapshotter = Snapshotter()
    snapshot = snapshotter.snapshot({"dlist": linked_list})
    rendered = render_memory(snapshot)

    assert "dlist ──▶ Doubly Linked List" in rendered
    assert "Node Structure" in rendered
    assert next_address in rendered


def test_snapshot_skips_class_and_function_definitions() -> None:
    snapshotter = Snapshotter()

    class Demo:
        pass

    def helper() -> None:
        return None

    snapshot = snapshotter.snapshot({"Demo": Demo, "helper": helper, "x": 1})
    assert "Demo" not in snapshot.names
    assert "helper" not in snapshot.names
    assert snapshot.names["x"] == 1


def test_stack_rendering_in_memory_view() -> None:
    from dsa_visualizer.data_structures.implementations.structures import Stack

    stack = Stack(["A", "B"])
    snapshotter = Snapshotter()
    snapshot = snapshotter.snapshot({"stack": stack})
    rendered = render_memory(snapshot)

    assert "stack ──▶ Stack" in rendered
    assert "Top" in rendered


class CustomStack:
    def __init__(self) -> None:
        self._items: list[object] = []

    def push(self, value: object) -> None:
        self._items.append(value)

    def pop(self) -> object | None:
        if not self._items:
            return None
        return self._items.pop()

    def peek(self) -> object | None:
        if not self._items:
            return None
        return self._items[-1]


def test_structural_stack_rendering() -> None:
    stack = CustomStack()
    stack.push("A")
    stack.push("B")
    snapshotter = Snapshotter()
    snapshot = snapshotter.snapshot({"custom": stack})
    rendered = render_memory(snapshot)

    assert "custom ──▶ Stack" in rendered
    assert "Top" in rendered


class DataStack:
    def __init__(self) -> None:
        self._data: list[object] = []

    def push(self, value: object) -> None:
        self._data.append(value)

    def pop(self) -> object | None:
        if not self._data:
            return None
        return self._data.pop()

    def peek(self) -> object | None:
        if not self._data:
            return None
        return self._data[-1]


def test_structural_stack_data_list_rendering() -> None:
    stack = DataStack()
    stack.push("X")
    snapshotter = Snapshotter()
    snapshot = snapshotter.snapshot({"stack": stack})
    rendered = render_memory(snapshot)

    assert "stack ──▶ Stack" in rendered
    assert "X" in rendered


class CustomQueue:
    def __init__(self) -> None:
        self._data: list[object] = []

    def enqueue(self, value: object) -> None:
        self._data.append(value)

    def dequeue(self) -> object | None:
        if not self._data:
            return None
        return self._data.pop(0)

    def peek(self) -> object | None:
        if not self._data:
            return None
        return self._data[0]


def test_structural_queue_rendering() -> None:
    queue = CustomQueue()
    queue.enqueue("A")
    queue.enqueue("B")
    snapshotter = Snapshotter()
    snapshot = snapshotter.snapshot({"queue": queue})
    rendered = render_memory(snapshot)

    assert "queue ──▶ Queue" in rendered
    assert "Front" in rendered


class Node:
    def __init__(self, value: object) -> None:
        self.value = value
        self.next = None


class NodeQueue:
    def __init__(self) -> None:
        self.front = None
        self.rear = None

    def enqueue(self, value: object) -> None:
        new_node = QueueNode(value)
        if self.rear is None:
            self.front = new_node
            self.rear = new_node
            return
        self.rear.next = new_node
        self.rear = new_node

    def dequeue(self) -> object | None:
        if self.front is None:
            return None
        value = self.front.value
        self.front = self.front.next
        if self.front is None:
            self.rear = None
        return value

    def peek(self) -> object | None:
        if self.front is None:
            return None
        return self.front.value


def test_structural_node_queue_rendering() -> None:
    queue = NodeQueue()
    queue.enqueue("A")
    queue.enqueue("B")
    snapshotter = Snapshotter()
    snapshot = snapshotter.snapshot({"queue": queue})
    rendered = render_memory(snapshot)

    assert "queue ──▶ Queue" in rendered
    assert "A" in rendered
