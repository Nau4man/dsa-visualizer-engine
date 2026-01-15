from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import codeop

Status = Literal["complete", "incomplete", "error"]


@dataclass(frozen=True)
class AccumulationResult:
    status: Status
    error: str | None = None


def classify_buffer(buffer: str, *, force_submit: bool = False) -> AccumulationResult:
    if buffer.strip() == "":
        return AccumulationResult("incomplete")
    try:
        compiled = codeop.compile_command(buffer, symbol="exec")
    except SyntaxError as exc:
        return AccumulationResult("error", str(exc))
    if compiled is None:
        if force_submit:
            return AccumulationResult("error", "Incomplete code")
        return AccumulationResult("incomplete")
    return AccumulationResult("complete")
