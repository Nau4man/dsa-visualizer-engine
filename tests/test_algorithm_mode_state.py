"""Tests for algorithm mode state in DSAApp."""

from dsa_visualizer.algorithms.runner import AlgorithmRunner
from dsa_visualizer.algorithms.types import AlgorithmStep, HighlightContext


def make_step(num: int, is_complete: bool = False) -> AlgorithmStep:
    """Helper to create a test step."""
    return AlgorithmStep(
        step_number=num,
        action=f"Step {num}",
        highlights=HighlightContext(),
        data=[1, 2, 3],
        is_complete=is_complete,
    )


class TestAlgorithmModeState:
    """Tests for algorithm mode state management."""

    def test_algorithm_runner_can_be_created(self):
        """AlgorithmRunner can be created for use with DSAApp."""
        steps = [make_step(1), make_step(2, is_complete=True)]
        runner = AlgorithmRunner.from_steps("Linear Search", steps)

        assert runner.name == "Linear Search"
        assert len(runner.steps) == 2

    def test_runner_advance_returns_steps(self):
        """Runner advance returns steps correctly."""
        steps = [make_step(1), make_step(2, is_complete=True)]
        runner = AlgorithmRunner.from_steps("Linear Search", steps)

        step1 = runner.advance()
        assert step1 is not None
        assert step1.step_number == 1

        step2 = runner.advance()
        assert step2 is not None
        assert step2.step_number == 2

    def test_runner_current_returns_current_step(self):
        """Runner current returns step without advancing."""
        steps = [make_step(1), make_step(2, is_complete=True)]
        runner = AlgorithmRunner.from_steps("Linear Search", steps)

        runner.advance()
        current = runner.current()
        assert current is not None
        assert current.step_number == 1

        # Call again, same result
        current2 = runner.current()
        assert current2 is not None
        assert current2.step_number == 1

    def test_runner_rewind_goes_back(self):
        """Runner rewind moves backward."""
        steps = [make_step(1), make_step(2), make_step(3, is_complete=True)]
        runner = AlgorithmRunner.from_steps("Linear Search", steps)

        runner.advance()
        runner.advance()
        runner.advance()

        step = runner.rewind()
        assert step is not None
        assert step.step_number == 2

    def test_runner_reset_goes_to_start(self):
        """Runner reset goes back to beginning."""
        steps = [make_step(1), make_step(2, is_complete=True)]
        runner = AlgorithmRunner.from_steps("Linear Search", steps)

        runner.advance()
        runner.advance()
        runner.reset()

        assert runner.current_index == -1
        assert runner.current() is None
