"""Algorithm overview panel content for the main UI."""

from rich.text import Text

from dsa_visualizer.ui.theme import (
    BODY_STYLE,
    DIVIDER_STYLE,
    LEVEL_STYLES,
    OVERVIEW_SEPARATOR_STYLE,
)

# (label, usage/example, complexity, level, is_heading)
ALGORITHM_OVERVIEW_LINES = [
    ("│", "", "", 0, False),
    ("├──▶ Array Search", "search('binary', [1,3,5,7], 5)", "", 1, True),
    ("│     ├──▶ linear", "", "O(n)", 2, False),
    ("│     ├──▶ binary", "", "O(log n) - requires sorted", 2, False),
    ("│     ├──▶ jump", "", "O(√n) - requires sorted", 2, False),
    ("│     ├──▶ interpolation", "", "O(log log n) avg - requires sorted", 2, False),
    ("│     └──▶ exponential", "", "O(log n) - requires sorted", 2, False),
    ("│", "", "", 0, False),
    ("├──▶ Tree Search", "tree_search('dfs', tree, 10)", "", 1, True),
    ("│     ├──▶ dfs", "", "O(n) - Depth-First Search", 2, False),
    ("│     ├──▶ bfs", "", "O(n) - Breadth-First Search", 2, False),
    ("│     └──▶ bst", "", "O(log n) avg - BST property", 2, False),
    ("│", "", "", 0, False),
    ("└──▶ Tree Traversal", "tree_traverse('dfs', tree)", "", 1, True),
    ("      ├──▶ dfs", "", "Pre-order (root, left, right)", 2, False),
    ("      └──▶ bfs", "", "Level-order", 2, False),
]


def render_algorithm_overview() -> Text:
    """Render algorithm help content for the collapsible panel."""
    left_width = max(len(left) for left, _, _, _, _ in ALGORITHM_OVERVIEW_LINES)
    example_width = max(len(example) for _, example, _, _, _ in ALGORITHM_OVERVIEW_LINES)
    text = Text()
    for index, (left, example, desc, level, is_heading) in enumerate(
        ALGORITHM_OVERVIEW_LINES
    ):
        heading_style = LEVEL_STYLES[min(level, len(LEVEL_STYLES) - 1)]
        label_style = heading_style if is_heading else BODY_STYLE
        desc_style = heading_style if is_heading else BODY_STYLE

        if example or desc:
            left_padded = left.ljust(left_width)
            example_padded = example.ljust(example_width)
            text.append(left_padded, style=label_style)
            text.append(" │ ", style=DIVIDER_STYLE)
            text.append(example_padded, style=desc_style)
            if desc:
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

        if index < len(ALGORITHM_OVERVIEW_LINES) - 1:
            text.append("\n")
    return text
