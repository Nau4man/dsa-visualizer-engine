from __future__ import annotations

from dataclasses import dataclass
import types

from dsa_visualizer.data_structures.implementations.structures import (
    BinarySearchTree,
    BinaryTree,
    BinaryTreeNode,
    DoublyLinkedList,
    DoublyLinkedListNode,
    Graph,
    LinkedList,
    LinkedListNode,
    MinHeap,
    Queue,
    Stack,
)


PRIMITIVE_TYPES = (int, float, bool, str, type(None))

# Names that are built-in to the executor and should not be shown in memory view
BUILTIN_NAMES = frozenset({
    "EXAMPLES",
    "search",
    "tree_search",
    "tree_traverse",
    "algo_help",
    "LinkedList",
    "DoublyLinkedList",
    "Stack",
    "Queue",
    "BinaryTree",
    "BinarySearchTree",
    "MinHeap",
    "Graph",
})


@dataclass(frozen=True)
class ObjectRecord:
    obj_id: str
    address: str
    py_type: str
    dsa_type: str
    summary: str
    payload: object | None = None


@dataclass(frozen=True)
class Snapshot:
    names: dict[str, object]
    objects: dict[str, ObjectRecord]


def diff_snapshots(previous: Snapshot, current: Snapshot) -> Snapshot:
    names: dict[str, object] = {}
    objects: dict[str, ObjectRecord] = {}
    for name, target in current.names.items():
        if name not in previous.names or previous.names[name] != target:
            names[name] = target
            if isinstance(target, str) and target in current.objects:
                objects[target] = current.objects[target]
    return Snapshot(names=names, objects=objects)


class Snapshotter:
    def __init__(self) -> None:
        self._id_map: dict[int, str] = {}
        self._counter = 0

    def snapshot(self, globals_dict: dict[str, object]) -> Snapshot:
        names: dict[str, object] = {}
        objects: dict[str, ObjectRecord] = {}
        for name, value in globals_dict.items():
            if name.startswith("__"):
                continue
            if name in BUILTIN_NAMES:
                continue
            if isinstance(value, PRIMITIVE_TYPES):
                names[name] = value
            elif isinstance(value, (types.FunctionType, type)):
                continue
            else:
                obj_id = self._get_or_create_id(value)
                names[name] = obj_id
                if obj_id not in objects:
                    objects[obj_id] = self._build_object_record(obj_id, value)
        return Snapshot(names=names, objects=objects)

    def _get_or_create_id(self, value: object) -> str:
        key = id(value)
        if key not in self._id_map:
            self._counter += 1
            self._id_map[key] = f"obj#{self._counter}"
        return self._id_map[key]

    def _build_object_record(self, obj_id: str, value: object) -> ObjectRecord:
        py_type = type(value).__name__
        address = hex(id(value))
        if isinstance(value, list):
            return ObjectRecord(
                obj_id,
                address,
                py_type,
                "Array",
                f"len={len(value)}",
                list(value),
            )
        if isinstance(value, dict):
            return ObjectRecord(
                obj_id,
                address,
                py_type,
                "Hash Table",
                f"size={len(value)}",
                dict(value),
            )
        if isinstance(value, Stack):
            items = value.items()
            return ObjectRecord(
                obj_id,
                address,
                py_type,
                "Stack",
                f"size={len(items)}",
                items,
            )
        if isinstance(value, Queue):
            items = value.items()
            return ObjectRecord(
                obj_id,
                address,
                py_type,
                "Queue",
                f"size={len(items)}",
                items,
            )
        if isinstance(value, MinHeap):
            items = value.items()
            return ObjectRecord(
                obj_id,
                address,
                py_type,
                "Min Heap",
                f"size={len(items)}",
                items,
            )
        if isinstance(value, Graph):
            adjacency = value.adjacency()
            return ObjectRecord(
                obj_id,
                address,
                py_type,
                "Directed Graph" if value.directed else "Undirected Graph",
                f"nodes={len(adjacency)}",
                adjacency,
            )
        if _is_heap_like(value):
            items = _heap_items(value)
            return ObjectRecord(
                obj_id,
                address,
                py_type,
                "Min Heap",
                f"size={len(items)}",
                items,
            )
        if _is_graph_like(value):
            adjacency, directed = _graph_payload(value)
            return ObjectRecord(
                obj_id,
                address,
                py_type,
                "Directed Graph" if directed else "Undirected Graph",
                f"nodes={len(adjacency)}",
                adjacency,
            )
        if _is_stack_like(value):
            items = _stack_items(value)
            return ObjectRecord(
                obj_id,
                address,
                py_type,
                "Stack",
                f"size={len(items)}",
                items,
            )
        if _is_queue_like(value):
            items = _queue_items(value)
            return ObjectRecord(
                obj_id,
                address,
                py_type,
                "Queue",
                f"size={len(items)}",
                items,
            )
        if isinstance(value, BinarySearchTree):
            return ObjectRecord(
                obj_id,
                address,
                py_type,
                "Binary Search Tree",
                "rooted",
                value.root,
            )
        is_tree, tree_root = _binary_tree_payload(value)
        if is_tree:
            return ObjectRecord(
                obj_id,
                address,
                py_type,
                "Binary Tree",
                "rooted",
                tree_root,
            )
        is_doubly, doubly_head = _doubly_linked_list_payload(value)
        if is_doubly:
            doubly_len = _linked_list_length(doubly_head)
            return ObjectRecord(
                obj_id,
                address,
                py_type,
                "Doubly Linked List",
                f"len={doubly_len}",
                doubly_head,
            )

        is_linked_list, linked_head = _linked_list_payload(value)
        if is_linked_list:
            linked_len = _linked_list_length(linked_head)
            return ObjectRecord(
                obj_id,
                address,
                py_type,
                "Linked List",
                f"len={linked_len}",
                linked_head,
            )
        return ObjectRecord(obj_id, address, py_type, "Object", "unrendered", None)


def _linked_list_payload(value: object) -> tuple[bool, LinkedListNode | None]:
    if isinstance(value, LinkedList):
        return True, value.head
    if _is_node_like(value):
        return True, value
    try:
        head = getattr(value, "head")
    except AttributeError:
        return False, None
    if head is None:
        return True, None
    return (True, head) if _is_node_like(head) else (False, None)


def _doubly_linked_list_payload(
    value: object,
) -> tuple[bool, DoublyLinkedListNode | None]:
    if isinstance(value, DoublyLinkedList):
        return True, value.head
    if _is_doubly_node_like(value):
        return True, value
    try:
        head = getattr(value, "head")
    except AttributeError:
        return False, None
    if head is None:
        return True, None
    return (True, head) if _is_doubly_node_like(head) else (False, None)


def _is_node_like(value: object) -> bool:
    try:
        getattr(value, "next")
    except AttributeError:
        return False
    return hasattr(value, "value") or hasattr(value, "data")


def _is_doubly_node_like(value: object) -> bool:
    try:
        getattr(value, "next")
        getattr(value, "prev")
    except AttributeError:
        return False
    return hasattr(value, "value") or hasattr(value, "data")


def _is_stack_like(value: object) -> bool:
    return all(callable(getattr(value, name, None)) for name in ("push", "pop", "peek"))


def _stack_items(value: object) -> list[object]:
    items_attr = getattr(value, "items", None)
    if callable(items_attr):
        try:
            items = items_attr()
        except TypeError:
            items = None
    else:
        items = items_attr
    if isinstance(items, (list, tuple)):
        return list(items)
    private_items = getattr(value, "_items", None)
    if isinstance(private_items, (list, tuple)):
        return list(private_items)
    data_items = getattr(value, "_data", None)
    if isinstance(data_items, (list, tuple)):
        return list(data_items)
    plain_data = getattr(value, "data", None)
    if isinstance(plain_data, (list, tuple)):
        return list(plain_data)
    stack_items = getattr(value, "stack", None)
    if isinstance(stack_items, (list, tuple)):
        return list(stack_items)
    try:
        return list(value)
    except TypeError:
        return []


def _is_queue_like(value: object) -> bool:
    return all(
        callable(getattr(value, name, None)) for name in ("enqueue", "dequeue", "peek")
    )


def _queue_items(value: object) -> list[object]:
    front = getattr(value, "front", None)
    if _is_node_like(front):
        return _node_chain_values(front)
    items_attr = getattr(value, "items", None)
    if callable(items_attr):
        try:
            items = items_attr()
        except TypeError:
            items = None
    else:
        items = items_attr
    if isinstance(items, (list, tuple)):
        return list(items)
    private_items = getattr(value, "_items", None)
    if isinstance(private_items, (list, tuple)):
        return list(private_items)
    data_items = getattr(value, "_data", None)
    if isinstance(data_items, (list, tuple)):
        return list(data_items)
    plain_data = getattr(value, "data", None)
    if isinstance(plain_data, (list, tuple)):
        return list(plain_data)
    queue_items = getattr(value, "queue", None)
    if isinstance(queue_items, (list, tuple)):
        return list(queue_items)
    try:
        return list(value)
    except TypeError:
        return []


def _is_heap_like(value: object) -> bool:
    return all(
        callable(getattr(value, name, None)) for name in ("insert", "pop_min", "peek")
    )


def _heap_items(value: object) -> list[object]:
    items_attr = getattr(value, "items", None)
    if callable(items_attr):
        try:
            items = items_attr()
        except TypeError:
            items = None
    else:
        items = items_attr
    if isinstance(items, (list, tuple)):
        return list(items)
    heap_data = getattr(value, "_items", None)
    if isinstance(heap_data, (list, tuple)):
        return list(heap_data)
    heap_data = getattr(value, "_data", None)
    if isinstance(heap_data, (list, tuple)):
        return list(heap_data)
    heap_data = getattr(value, "data", None)
    if isinstance(heap_data, (list, tuple)):
        return list(heap_data)
    heap_data = getattr(value, "heap", None)
    if isinstance(heap_data, (list, tuple)):
        return list(heap_data)
    try:
        return list(value)
    except TypeError:
        return []


def _is_graph_like(value: object) -> bool:
    if hasattr(value, "adjacency") and callable(getattr(value, "adjacency")):
        return True
    for name in ("adjacency", "adj", "graph"):
        if isinstance(getattr(value, name, None), dict):
            return True
    return False


def _graph_payload(value: object) -> tuple[dict[object, list[object]], bool]:
    directed = bool(getattr(value, "directed", False))
    adjacency = None
    if callable(getattr(value, "adjacency", None)):
        try:
            adjacency = value.adjacency()
        except TypeError:
            adjacency = None
    if adjacency is None:
        for name in ("adjacency", "adj", "graph"):
            candidate = getattr(value, name, None)
            if isinstance(candidate, dict):
                adjacency = candidate
                break
    if adjacency is None:
        adjacency = {}
    normalized: dict[object, list[object]] = {}
    for node, neighbors in adjacency.items():
        if neighbors is None:
            normalized[node] = []
        elif isinstance(neighbors, (list, tuple, set)):
            normalized[node] = list(neighbors)
        else:
            normalized[node] = list(neighbors)
    return normalized, directed


def _node_chain_values(head: object) -> list[object]:
    values: list[object] = []
    seen: set[int] = set()
    current = head
    while _is_node_like(current):
        node_id = id(current)
        if node_id in seen:
            break
        seen.add(node_id)
        if hasattr(current, "value"):
            values.append(getattr(current, "value"))
        else:
            values.append(getattr(current, "data"))
        current = getattr(current, "next", None)
    return values


def _linked_list_length(head: LinkedListNode | DoublyLinkedListNode | None) -> int:
    seen: set[int] = set()
    count = 0
    current = head
    while current is not None:
        node_id = id(current)
        if node_id in seen:
            break
        seen.add(node_id)
        count += 1
        current = current.next
    return count


def _binary_tree_payload(value: object) -> tuple[bool, BinaryTreeNode | None]:
    if isinstance(value, BinaryTree):
        return True, value.root
    if _is_tree_node_like(value):
        return True, value
    try:
        root = getattr(value, "root")
    except AttributeError:
        return False, None
    if root is None:
        return True, None
    return (True, root) if _is_tree_node_like(root) else (False, None)


def _is_tree_node_like(value: object) -> bool:
    try:
        getattr(value, "left")
        getattr(value, "right")
    except AttributeError:
        return False
    return hasattr(value, "value") or hasattr(value, "data")
