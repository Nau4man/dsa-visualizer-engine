# DSA Visualizer Engine

Terminal-based interactive notebook that executes real Python and visualizes data
structures as live ASCII diagrams. The UI shows a scrollable code history alongside
the current memory state so you can see how variables bind, mutate, and share
objects.

## Requirements

- Python >= 3.14
- `uv` (recommended) for running commands

## Install

Clone the repo and run using `uv`:

```bash
uv run dsa
```

Or run the entrypoint directly:

```bash
uv run python main.py
```

## Usage

Type Python code in the input area and press Enter to execute when the block is
complete. Multi-line blocks are supported. Each executed cell appears in the
notebook with a success/error indicator. The memory panel updates after every
execution.

Built-in classes are available by default:

- `LinkedList`, `DoublyLinkedList`
- `Stack`, `Queue`
- `BinaryTree`, `BinarySearchTree`
- `MinHeap`
- `Graph`

Custom structures are supported through structural detection (for example,
linked lists via `value/next`, queues via `enqueue/dequeue/peek`, heaps via
`insert/pop_min/peek`, trees via `left/right`).

## Supported Visualizations

All diagrams must follow `ASCII_VISUALS.md`. Current coverage includes:

- Primitives (int, float, bool, string, None)
- Array (list)
- Hash Table (dict, separate chaining)
- Linked List (singly, doubly)
- Stack (LIFO)
- Queue (FIFO)
- Binary Tree
- Binary Search Tree
- Min Heap
- Graph (directed/undirected adjacency list)

## Development

Run lint and tests with:

```bash
uv run ruff check .
uv run pytest -q
```

## Project Docs

- `SPEC.md` defines behavior and UI rules.
- `TODO.md` is the required task order (one task at a time).
- `ASCII_VISUALS.md` is the source of truth for rendering.
