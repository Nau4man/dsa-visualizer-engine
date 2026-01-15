from __future__ import annotations

from dataclasses import dataclass

from dsa_visualizer.core.structures import (
    BinarySearchTree,
    BinaryTree,
    DoublyLinkedList,
    Graph,
    LinkedList,
    MinHeap,
    Queue,
    Stack,
)

@dataclass(frozen=True)
class ExecutionResult:
    ok: bool
    error: str | None = None


class Executor:
    def __init__(self) -> None:
        self.globals: dict[str, object] = {
            "LinkedList": LinkedList,
            "DoublyLinkedList": DoublyLinkedList,
            "Stack": Stack,
            "Queue": Queue,
            "BinaryTree": BinaryTree,
            "BinarySearchTree": BinarySearchTree,
            "MinHeap": MinHeap,
            "Graph": Graph,
        }

    def execute(self, source: str) -> ExecutionResult:
        try:
            compiled = compile(source, "<input>", "exec")
            exec(compiled, self.globals)
        except Exception as exc:  # noqa: BLE001 - surface error message to user
            return ExecutionResult(False, str(exc))
        return ExecutionResult(True, None)
