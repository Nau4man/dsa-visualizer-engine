"""Tests for algorithm panel widget."""

from dsa_visualizer.algorithms.runner import AlgorithmRunner
from dsa_visualizer.algorithms.types import AlgorithmStep, HighlightContext
from dsa_visualizer.algorithms.ui.panel import (
    render_algorithm_panel,
    render_algorithm_header,
)


def make_step(
    num: int, action: str = "Test action", is_complete: bool = False, result: object = None
) -> AlgorithmStep:
    """Helper to create a test step."""
    return AlgorithmStep(
        step_number=num,
        action=action,
        highlights=HighlightContext(),
        data=[1, 2, 3],
        is_complete=is_complete,
        result=result,
    )


class TestRenderAlgorithmPanel:
    """Tests for render_algorithm_panel function."""

    def test_shows_algorithm_name(self):
        """Panel shows the algorithm name."""
        steps = [make_step(1)]
        runner = AlgorithmRunner.from_steps("Linear Search", steps)
        runner.advance()

        text = render_algorithm_panel(runner, runner.current())
        plain = text.plain

        assert "Linear Search" in plain

    def test_shows_complexity_for_known_algorithms(self):
        """Panel shows complexity for known algorithms."""
        steps = [make_step(1)]
        runner = AlgorithmRunner.from_steps("Linear Search", steps)
        runner.advance()

        text = render_algorithm_panel(runner, runner.current())
        plain = text.plain

        assert "O(n)" in plain

    def test_shows_step_number(self):
        """Panel shows current step number."""
        steps = [make_step(1), make_step(2)]
        runner = AlgorithmRunner.from_steps("Linear Search", steps)
        runner.advance()

        text = render_algorithm_panel(runner, runner.current())
        plain = text.plain

        assert "Step 1" in plain

    def test_shows_total_steps_when_known(self):
        """Panel shows total steps when available."""
        steps = [make_step(1), make_step(2), make_step(3)]
        runner = AlgorithmRunner.from_steps("Test", steps)
        runner.advance()

        text = render_algorithm_panel(runner, runner.current())
        plain = text.plain

        assert "of 3" in plain

    def test_shows_action_text(self):
        """Panel shows the current action description."""
        steps = [make_step(1, action="Compare arr[0] with target")]
        runner = AlgorithmRunner.from_steps("Test", steps)
        runner.advance()

        text = render_algorithm_panel(runner, runner.current())
        plain = text.plain

        assert "Compare arr[0] with target" in plain

    def test_shows_controls_hint(self):
        """Panel shows keyboard controls hint."""
        steps = [make_step(1)]
        runner = AlgorithmRunner.from_steps("Test", steps)
        runner.advance()

        text = render_algorithm_panel(runner, runner.current())
        plain = text.plain

        assert "Space" in plain or "N" in plain
        assert "Prev" in plain or "P" in plain
        assert "Reset" in plain or "R" in plain
        assert "Esc" in plain

    def test_shows_found_status_when_complete(self):
        """Panel shows FOUND status when element found."""
        steps = [make_step(1), make_step(2, is_complete=True, result=1)]
        runner = AlgorithmRunner.from_steps("Test", steps)
        runner.advance()
        runner.advance()

        text = render_algorithm_panel(runner, runner.current())
        plain = text.plain

        assert "FOUND" in plain

    def test_shows_not_found_status_when_complete(self):
        """Panel shows NOT FOUND status when element not found."""
        steps = [make_step(1), make_step(2, is_complete=True, result=-1)]
        runner = AlgorithmRunner.from_steps("Test", steps)
        runner.advance()
        runner.advance()

        text = render_algorithm_panel(runner, runner.current())
        plain = text.plain

        assert "NOT FOUND" in plain

    def test_handles_none_step(self):
        """Panel handles None step gracefully."""
        steps = [make_step(1)]
        runner = AlgorithmRunner.from_steps("Test", steps)
        # Don't advance, so current() returns None

        text = render_algorithm_panel(runner, None)
        plain = text.plain

        assert "Test" in plain
        assert "Step 0" in plain


class TestRenderAlgorithmHeader:
    """Tests for render_algorithm_header function."""

    def test_shows_algorithm_name(self):
        """Header shows algorithm name."""
        steps = [make_step(1)]
        runner = AlgorithmRunner.from_steps("Binary Search", steps)

        text = render_algorithm_header(runner)
        plain = text.plain

        assert "Binary Search" in plain

    def test_shows_complexity(self):
        """Header shows complexity for known algorithms."""
        steps = [make_step(1)]
        runner = AlgorithmRunner.from_steps("Binary Search", steps)

        text = render_algorithm_header(runner)
        plain = text.plain

        assert "O(log n)" in plain

    def test_no_complexity_for_unknown(self):
        """Header handles unknown algorithms gracefully."""
        steps = [make_step(1)]
        runner = AlgorithmRunner.from_steps("Custom Algorithm", steps)

        text = render_algorithm_header(runner)
        plain = text.plain

        assert "Custom Algorithm" in plain
