from rich.text import Text

from dsa_visualizer.ui.theme import (
    BODY_STYLE,
    DIVIDER_STYLE,
    HEADING_STYLE,
    LEVEL_STYLES,
    OVERVIEW_SEPARATOR_STYLE,
)

DATA_STRUCTURES_HEADING = "Data Structures"

OVERVIEW_LINES = [
    ("│", "", "", 0, False),
    ("├──▶ Primitive", "", "Worst-case Big(O) for basic operations", 1, True),
    ("│     ├──▶ Integer", "10", "access O(1)", 2, False),
    ("│     ├──▶ Float", "3.14", "access O(1)", 2, False),
    ("│     ├──▶ Boolean", "True", "access O(1)", 2, False),
    ("│     ├──▶ Character", "'a'", "access O(1)", 2, False),
    (
        "│     └──▶ String",
        "\"hi\"",
        "index O(1) | search O(n) | insert O(n) | delete O(n)",
        2,
        False,
    ),
    ("│", "", "", 0, False),
    ("└──▶ Non-Primitive", "", "", 1, True),
    (
        "      ├──▶ Linear Data Structures",
        "",
        "Worst-case Big(O) for access/search/insert/delete",
        2,
        True,
    ),
    (
        "      │     ├──▶ Array",
        "[10, 22, 7]",
        "access O(1) | search O(n) | insert O(n) | delete O(n)",
        3,
        False,
    ),
    (
        "      │     ├──▶ Linked List",
        "10 -> 22 -> 7 -> null",
        "access O(n) | search O(n) | insert O(n) | delete O(n)",
        3,
        False,
    ),
    (
        "      │     ├──▶ Stack",
        "[1, 2, 3] top=3",
        "push O(1) | pop O(1) | peek O(1)",
        3,
        False,
    ),
    (
        "      │     └──▶ Queue",
        "[1, 2, 3] front=1",
        "enqueue O(1) | dequeue O(1) | peek O(1)",
        3,
        False,
    ),
    ("      │", "", "", 0, False),
    (
        "      └──▶ Non-Linear Data Structures",
        "",
        "Worst-case Big(O) for search/insert/delete/traverse",
        2,
        True,
    ),
    ("            ├──▶ Tree", "A(B,C)", "traverse O(n) | search O(n)", 3, False),
    (
        "            ├──▶ Binary Search Tree",
        "5(3,7)",
        "search O(n) | insert O(n) | delete O(n)",
        3,
        False,
    ),
    (
        "            ├──▶ Heap",
        "[1, 3, 5]",
        "insert O(log n) | delete O(log n) | peek O(1)",
        3,
        False,
    ),
    (
        "            └──▶ Graph",
        "A->B,C",
        "traverse O(V+E) | search O(V+E)",
        3,
        False,
    ),
]


def render_heading() -> Text:
    return Text(DATA_STRUCTURES_HEADING, style=HEADING_STYLE)


def render_overview() -> Text:
    left_width = max(len(left) for left, _, _, _, _ in OVERVIEW_LINES)
    example_width = max(len(example) for _, example, _, _, _ in OVERVIEW_LINES)
    text = Text()
    for index, (left, example, desc, level, is_heading) in enumerate(OVERVIEW_LINES):
        heading_style = LEVEL_STYLES[min(level, len(LEVEL_STYLES) - 1)]
        label_style = heading_style if is_heading else BODY_STYLE
        desc_style = heading_style if is_heading else BODY_STYLE
        if desc:
            left_padded = left.ljust(left_width)
            example_padded = example.ljust(example_width)
            text.append(left_padded, style=label_style)
            text.append(" │ ", style=DIVIDER_STYLE)
            text.append(example_padded, style=desc_style)
            text.append(" │ ", style=DIVIDER_STYLE)
            if " | " in desc:
                parts = desc.split(" | ")
                text.append(parts[0], style=desc_style)
                for part in parts[1:]:
                    text.append(" | ", style=OVERVIEW_SEPARATOR_STYLE)
                    text.append(part, style=desc_style)
            else:
                text.append(desc, style=desc_style)
        else:
            text.append(left, style=DIVIDER_STYLE)
        if index < len(OVERVIEW_LINES) - 1:
            text.append("\n")
    return text
