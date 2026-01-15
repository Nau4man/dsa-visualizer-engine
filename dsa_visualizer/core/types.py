from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Cell:
    cell_id: int
    code: str
    ok: bool = True
    error: str | None = None
    snapshot_text: str | None = None


@dataclass(frozen=True)
class MemoryBlock:
    """Represents a single memory visualization block."""
    block_id: str  # e.g., "var_x" or "obj#1"
    header: str  # e.g., "x ──▶ int" or "arr ──▶ Array"
    summary: str  # Short description shown when collapsed
    content: str  # Full visualization content
