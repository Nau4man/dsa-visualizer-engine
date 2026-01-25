from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Iterator


@dataclass
class LinkedListNode:
    data: object
    next: LinkedListNode | None = None
    address: int = 0


class LinkedList:
    _address_counter = 0
    _address_step = 4
    _address_base = 0x1000

    def __init__(self, values: Iterable[object] | None = None) -> None:
        self.head: LinkedListNode | None = None
        self.tail: LinkedListNode | None = None
        self._length = 0
        if values is not None:
            for value in values:
                self.append(value)

    def append(self, value: object) -> LinkedListNode:
        node = LinkedListNode(data=value)
        node.address = self._next_address()
        if self.head is None:
            self.head = node
            self.tail = node
        else:
            assert self.tail is not None
            self.tail.next = node
            self.tail = node
        self._length += 1
        return node

    def __len__(self) -> int:
        return self._length

    def nodes(self) -> Iterator[LinkedListNode]:
        seen: set[int] = set()
        current = self.head
        while current is not None:
            if id(current) in seen:
                break
            seen.add(id(current))
            yield current
            current = current.next

    @classmethod
    def _next_address(cls) -> int:
        cls._address_counter += 1
        return cls._address_base + cls._address_step * cls._address_counter

    @classmethod
    def _reset_address_counter(cls) -> None:
        cls._address_counter = 0


@dataclass
class DoublyLinkedListNode:
    data: object
    prev: DoublyLinkedListNode | None = None
    next: DoublyLinkedListNode | None = None


class DoublyLinkedList:
    def __init__(self, values: Iterable[object] | None = None) -> None:
        self.head: DoublyLinkedListNode | None = None
        self.tail: DoublyLinkedListNode | None = None
        self._length = 0
        if values is not None:
            for value in values:
                self.append(value)

    def append(self, value: object) -> DoublyLinkedListNode:
        node = DoublyLinkedListNode(data=value)
        if self.head is None:
            self.head = node
            self.tail = node
        else:
            assert self.tail is not None
            node.prev = self.tail
            self.tail.next = node
            self.tail = node
        self._length += 1
        return node

    def delete(self, value: object) -> bool:
        current = self.head
        while current is not None:
            if current.data == value:
                if current.prev is not None:
                    current.prev.next = current.next
                else:
                    self.head = current.next
                if current.next is not None:
                    current.next.prev = current.prev
                else:
                    self.tail = current.prev
                self._length -= 1
                return True
            current = current.next
        return False

    def __len__(self) -> int:
        return self._length


class Stack:
    def __init__(self, values: Iterable[object] | None = None) -> None:
        self._items: list[object] = []
        if values is not None:
            for value in values:
                self.push(value)

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

    def __len__(self) -> int:
        return len(self._items)

    def items(self) -> list[object]:
        return list(self._items)


class Queue:
    def __init__(self, values: Iterable[object] | None = None) -> None:
        self._items: list[object] = []
        if values is not None:
            for value in values:
                self.enqueue(value)

    def enqueue(self, value: object) -> None:
        self._items.append(value)

    def dequeue(self) -> object | None:
        if not self._items:
            return None
        return self._items.pop(0)

    def peek(self) -> object | None:
        if not self._items:
            return None
        return self._items[0]

    def __len__(self) -> int:
        return len(self._items)

    def items(self) -> list[object]:
        return list(self._items)


@dataclass
class BinaryTreeNode:
    value: object
    left: BinaryTreeNode | None = None
    right: BinaryTreeNode | None = None


class BinaryTree:
    def __init__(self, values: Iterable[object] | None = None) -> None:
        self.root: BinaryTreeNode | None = None
        if values is not None:
            for value in values:
                self.insert(value)

    def insert(self, value: object) -> BinaryTreeNode:
        node = BinaryTreeNode(value=value)
        if self.root is None:
            self.root = node
            return node
        queue: list[BinaryTreeNode] = [self.root]
        while queue:
            current = queue.pop(0)
            if current.left is None:
                current.left = node
                return node
            if current.right is None:
                current.right = node
                return node
            queue.append(current.left)
            queue.append(current.right)
        return node

    def search(self, value: object) -> BinaryTreeNode | None:
        if self.root is None:
            return None
        queue: list[BinaryTreeNode] = [self.root]
        while queue:
            current = queue.pop(0)
            if current.value == value:
                return current
            if current.left is not None:
                queue.append(current.left)
            if current.right is not None:
                queue.append(current.right)
        return None

    def delete(self, value: object) -> bool:
        if self.root is None:
            return False
        if self.root.left is None and self.root.right is None:
            if self.root.value == value:
                self.root = None
                return True
            return False

        queue: list[BinaryTreeNode] = [self.root]
        node_to_delete: BinaryTreeNode | None = None
        last_node: BinaryTreeNode | None = None
        parent_of_last: BinaryTreeNode | None = None
        while queue:
            last_node = queue.pop(0)
            if last_node.value == value:
                node_to_delete = last_node
            if last_node.left is not None:
                parent_of_last = last_node
                queue.append(last_node.left)
            if last_node.right is not None:
                parent_of_last = last_node
                queue.append(last_node.right)

        if node_to_delete is None or last_node is None:
            return False

        node_to_delete.value = last_node.value
        if parent_of_last is not None:
            if parent_of_last.left is last_node:
                parent_of_last.left = None
            elif parent_of_last.right is last_node:
                parent_of_last.right = None
        else:
            self.root = None
        return True


@dataclass
class BSTNode:
    value: object
    left: BSTNode | None = None
    right: BSTNode | None = None


class BinarySearchTree:
    def __init__(self, values: Iterable[object] | None = None) -> None:
        self.root: BSTNode | None = None
        if values is not None:
            for value in values:
                self.insert(value)

    def insert(self, value: object) -> BSTNode:
        node = BSTNode(value=value)
        if self.root is None:
            self.root = node
            return node
        current = self.root
        while True:
            if value < current.value:
                if current.left is None:
                    current.left = node
                    return node
                current = current.left
            else:
                if current.right is None:
                    current.right = node
                    return node
                current = current.right

    def search(self, value: object) -> BSTNode | None:
        current = self.root
        while current is not None:
            if value == current.value:
                return current
            if value < current.value:
                current = current.left
            else:
                current = current.right
        return None

    def delete(self, value: object) -> bool:
        self.root, deleted = self._delete_node(self.root, value)
        return deleted

    def _delete_node(
        self, node: BSTNode | None, value: object
    ) -> tuple[BSTNode | None, bool]:
        if node is None:
            return None, False
        if value < node.value:
            node.left, deleted = self._delete_node(node.left, value)
            return node, deleted
        if value > node.value:
            node.right, deleted = self._delete_node(node.right, value)
            return node, deleted

        if node.left is None and node.right is None:
            return None, True
        if node.left is None:
            return node.right, True
        if node.right is None:
            return node.left, True

        successor_parent = node
        successor = node.right
        while successor.left is not None:
            successor_parent = successor
            successor = successor.left
        node.value = successor.value
        if successor_parent is node:
            successor_parent.right = successor.right
        else:
            successor_parent.left = successor.right
        return node, True


class MinHeap:
    def __init__(self, values: Iterable[object] | None = None) -> None:
        self._items: list[object] = []
        if values is not None:
            for value in values:
                self.insert(value)

    def insert(self, value: object) -> None:
        self._items.append(value)
        self._bubble_up(len(self._items) - 1)

    def pop_min(self) -> object | None:
        if not self._items:
            return None
        if len(self._items) == 1:
            return self._items.pop()
        root = self._items[0]
        self._items[0] = self._items.pop()
        self._bubble_down(0)
        return root

    def peek(self) -> object | None:
        if not self._items:
            return None
        return self._items[0]

    def __len__(self) -> int:
        return len(self._items)

    def items(self) -> list[object]:
        return list(self._items)

    def _bubble_up(self, index: int) -> None:
        while index > 0:
            parent = (index - 1) // 2
            if self._items[index] < self._items[parent]:
                self._items[index], self._items[parent] = (
                    self._items[parent],
                    self._items[index],
                )
                index = parent
            else:
                break

    def _bubble_down(self, index: int) -> None:
        size = len(self._items)
        while True:
            left = index * 2 + 1
            right = left + 1
            smallest = index
            if left < size and self._items[left] < self._items[smallest]:
                smallest = left
            if right < size and self._items[right] < self._items[smallest]:
                smallest = right
            if smallest == index:
                break
            self._items[index], self._items[smallest] = (
                self._items[smallest],
                self._items[index],
            )
            index = smallest


class Graph:
    def __init__(self, *, directed: bool = False) -> None:
        self.directed = directed
        self._adjacency: dict[object, list[object]] = {}

    def add_node(self, node: object) -> None:
        if node not in self._adjacency:
            self._adjacency[node] = []

    def add_edge(self, source: object, target: object) -> None:
        self.add_node(source)
        self.add_node(target)
        self._adjacency[source].append(target)
        if not self.directed:
            self._adjacency[target].append(source)

    def adjacency(self) -> dict[object, list[object]]:
        return {node: list(neighbors) for node, neighbors in self._adjacency.items()}
