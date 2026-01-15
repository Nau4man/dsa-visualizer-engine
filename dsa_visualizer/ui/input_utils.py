def clamp_input_height(text: str, min_lines: int, max_lines: int) -> int:
    line_count = text.count("\n") + 1
    return max(min_lines, min(max_lines, line_count))


def indent_for_newline(line: str) -> str | None:
    if not line.rstrip().endswith(":"):
        return None
    leading = line[: len(line) - len(line.lstrip())]
    return f"{leading}    "
