from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Cell:
    cell_id: int
    code: str
    ok: bool = True
    error: str | None = None
    snapshot_text: str | None = None
