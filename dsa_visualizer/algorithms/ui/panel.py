"""Algorithm panel widget for displaying algorithm execution state."""

from __future__ import annotations

from rich.text import Text

from dsa_visualizer.algorithms.runner import AlgorithmRunner
from dsa_visualizer.algorithms.types import AlgorithmStep


# Algorithm complexity info for display
ALGORITHM_INFO = {
    "Linear Search": "O(n)",
    "Binary Search": "O(log n)",
    "Jump Search": "O(√n)",
    "Interpolation Search": "O(log log n) avg",
    "Exponential Search": "O(log n)",
    "DFS": "O(V + E)",
    "BFS": "O(V + E)",
    "BST Search": "O(log n) avg",
}


def render_algorithm_panel(
    runner: AlgorithmRunner,
    step: AlgorithmStep | None,
) -> Text:
    """Render the algorithm info panel.

    Shows:
    - Algorithm name and complexity
    - Current step number
    - Action description
    - Controls hint

    Args:
        runner: The algorithm runner managing execution.
        step: The current algorithm step (may be None if not started).

    Returns:
        Rich Text object for display.
    """
    text = Text()

    # Algorithm name and complexity
    complexity = ALGORITHM_INFO.get(runner.name, "")
    text.append(f"Algorithm: {runner.name}", style="bold #f6c64a")
    if complexity:
        text.append(f"  [{complexity}]", style="dim")
    text.append("\n")

    # Step counter
    if runner.total_steps is not None:
        text.append(f"Step {runner.step_number} of {runner.total_steps}\n")
    else:
        text.append(f"Step {runner.step_number}\n")

    # Status indicator
    if step is not None and step.is_complete:
        if step.result is not None and step.result != -1:
            text.append("Status: ", style="dim")
            text.append("FOUND", style="bold green")
            text.append(f" at index {step.result}\n")
        else:
            text.append("Status: ", style="dim")
            text.append("NOT FOUND", style="bold red")
            text.append("\n")

    # Current action
    if step is not None:
        text.append(f"\n{step.action}\n", style="bold")

    # Separator
    text.append("\n")

    # Controls hint
    text.append("Controls: ", style="dim")
    text.append("Space/N", style="bold")
    text.append("=Next  ", style="dim")
    text.append("P", style="bold")
    text.append("=Prev  ", style="dim")
    text.append("R", style="bold")
    text.append("=Reset  ", style="dim")
    text.append("Esc", style="bold")
    text.append("=Exit", style="dim")

    return text


def render_algorithm_header(runner: AlgorithmRunner) -> Text:
    """Render a compact header for the algorithm panel.

    Args:
        runner: The algorithm runner.

    Returns:
        Rich Text object with compact header.
    """
    text = Text()
    text.append("▶ ", style="bold #f6c64a")
    text.append(runner.name, style="bold")

    complexity = ALGORITHM_INFO.get(runner.name, "")
    if complexity:
        text.append(f"  [{complexity}]", style="dim")

    return text
