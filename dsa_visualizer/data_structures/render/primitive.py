from __future__ import annotations

import struct
import sys


def render_primitive(name: str, value: object) -> str:
    if value is None:
        return _render_null(name)
    if isinstance(value, bool):
        return _render_bool(name, value)
    if isinstance(value, int):
        return _render_int(name, value)
    if isinstance(value, float):
        return _render_float(name, value)
    if isinstance(value, str) and len(value) == 1:
        return _render_char(name, value)
    if isinstance(value, str):
        return _render_string(name, value)
    return _render_generic(name, value)


def _render_int(name: str, value: int) -> str:
    size_bytes = sys.getsizeof(value)
    bits = _bytes_to_bits(_int_to_bytes(value))
    lines = [
        f"Address: {hex(id(value))}",
        "",
        "type: int",
        f"size: {size_bytes} bytes",
        f"bits: {bits}",
        f"value: {value}",
    ]
    return _boxed(name, lines)


def _render_bool(name: str, value: bool) -> str:
    size_bytes = sys.getsizeof(value)
    bits = _bytes_to_bits(_int_to_bytes(1 if value else 0, size=1))
    lines = [
        f"Address: {hex(id(value))}",
        "",
        "type: bool",
        f"size: {size_bytes} bytes",
        f"bits: {bits}",
        f"value: {str(value).lower()}",
    ]
    return _boxed(name, lines)


def _render_char(name: str, value: str) -> str:
    size_bytes = sys.getsizeof(value)
    codepoint = ord(value)
    bits = _bytes_to_bits(_int_to_bytes(codepoint, size=1))
    lines = [
        f"Address: {hex(id(value))}",
        "",
        "type: char (ASCII)",
        f"size: {size_bytes} bytes",
        f"bits: {bits}",
        f"value: '{value}' ({codepoint})",
    ]
    return _boxed(name, lines)


def _render_float(name: str, value: float) -> str:
    size_bytes = sys.getsizeof(value)
    packed = struct.pack(">f", value)
    bits = "".join(f"{byte:08b}" for byte in packed)
    sign = bits[0]
    exponent = bits[1:9]
    mantissa = bits[9:]
    mantissa_short = _shorten_bits(mantissa, 9)
    lines = [
        f"Address: {hex(id(value))}",
        "",
        "type: float32",
        f"size: {size_bytes} bytes",
        "sign | exponent | mantissa",
        f"  {sign}  | {exponent} | {mantissa_short}",
        f"value: {value}",
    ]
    return _boxed(name, lines)


def _render_null(name: str) -> str:
    size_bytes = sys.getsizeof(None)
    lines = [
        "type: NULL",
        f"size: {size_bytes} bytes",
        "meaning: no object",
    ]
    return _boxed(name, lines)


def _render_string(name: str, value: str) -> str:
    size_bytes = sys.getsizeof(value)
    encoded = value.encode("utf-8")
    bits = _bytes_to_bits(encoded)
    lines = [
        f"Address: {hex(id(value))}",
        "",
        "type: string",
        f"size: {size_bytes} bytes",
        f"bits: {bits}",
        f"value: \"{value}\"",
    ]
    return _boxed(name, lines)


def _render_generic(name: str, value: object) -> str:
    size_bytes = sys.getsizeof(value)
    lines = [
        f"Address: {hex(id(value))}",
        "",
        f"type: {type(value).__name__}",
        f"size: {size_bytes} bytes",
        f"value: {value!r}",
    ]
    return _boxed(name, lines)


def _boxed(name: str, lines: list[str]) -> str:
    body = [line for line in lines if line != ""]
    width = max(len(line) for line in body) if body else 0
    top = "┌" + "─" * (width + 2) + "┐"
    bottom = "└" + "─" * (width + 2) + "┘"
    content = [f"│ {line.ljust(width)} │" for line in body]
    header = [f"{name}"]
    return "\n".join(header + [top] + content + [bottom])


def _int_to_bytes(value: int, *, size: int | None = None) -> bytes:
    if size is None:
        size = max(1, (value.bit_length() + 7) // 8)
    return value.to_bytes(size, "big", signed=value < 0)


def _bytes_to_bits(data: bytes) -> str:
    return " ".join(f"{byte:08b}" for byte in data)


def _shorten_bits(bits: str, limit: int) -> str:
    if len(bits) <= limit:
        return bits
    return f"{bits[:limit]}..."
