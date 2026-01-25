"""Tests for AlgorithmRunner class."""

from dsa_visualizer.algorithms.types import HighlightContext, AlgorithmStep
from dsa_visualizer.algorithms.runner import AlgorithmRunner


def make_step(num: int, is_complete: bool = False) -> AlgorithmStep:
    """Helper to create a test step."""
    return AlgorithmStep(
        step_number=num,
        action=f"Step {num}",
        highlights=HighlightContext(),
        data=[],
        is_complete=is_complete,
    )


def make_generator(count: int):
    """Helper to create a generator yielding count steps."""
    for i in range(1, count + 1):
        yield make_step(i, is_complete=(i == count))


class TestAlgorithmRunnerFromSteps:
    """Tests for AlgorithmRunner created from pre-computed steps."""

    def test_create_from_steps(self):
        """Can create runner from list of steps."""
        steps = [make_step(1), make_step(2), make_step(3, is_complete=True)]
        runner = AlgorithmRunner.from_steps("Test", steps)

        assert runner.name == "Test"
        assert len(runner.steps) == 3
        assert runner.current_index == -1
        assert runner.step_number == 0

    def test_advance_moves_forward(self):
        """advance() moves to next step and returns it."""
        steps = [make_step(1), make_step(2), make_step(3)]
        runner = AlgorithmRunner.from_steps("Test", steps)

        step = runner.advance()
        assert step is not None
        assert step.step_number == 1
        assert runner.current_index == 0
        assert runner.step_number == 1

        step = runner.advance()
        assert step is not None
        assert step.step_number == 2
        assert runner.current_index == 1

    def test_advance_returns_none_at_end(self):
        """advance() returns None when no more steps."""
        steps = [make_step(1)]
        runner = AlgorithmRunner.from_steps("Test", steps)

        runner.advance()  # Move to step 1
        step = runner.advance()  # Try to go past end
        assert step is None
        assert runner.current_index == 0  # Stays at last valid

    def test_rewind_moves_backward(self):
        """rewind() moves to previous step and returns it."""
        steps = [make_step(1), make_step(2), make_step(3)]
        runner = AlgorithmRunner.from_steps("Test", steps)

        runner.advance()
        runner.advance()
        runner.advance()
        assert runner.current_index == 2

        step = runner.rewind()
        assert step is not None
        assert step.step_number == 2
        assert runner.current_index == 1

    def test_rewind_returns_none_at_start(self):
        """rewind() returns None when at beginning."""
        steps = [make_step(1)]
        runner = AlgorithmRunner.from_steps("Test", steps)

        # Not started yet
        step = runner.rewind()
        assert step is None
        assert runner.current_index == -1

        # After one advance, rewind goes back to -1
        runner.advance()
        step = runner.rewind()
        assert step is None
        assert runner.current_index == -1

    def test_reset_goes_to_beginning(self):
        """reset() sets index to -1."""
        steps = [make_step(1), make_step(2)]
        runner = AlgorithmRunner.from_steps("Test", steps)

        runner.advance()
        runner.advance()
        assert runner.current_index == 1

        runner.reset()
        assert runner.current_index == -1
        assert runner.step_number == 0

    def test_current_returns_step_without_moving(self):
        """current() returns current step without advancing."""
        steps = [make_step(1), make_step(2)]
        runner = AlgorithmRunner.from_steps("Test", steps)

        # Not started
        assert runner.current() is None

        runner.advance()
        step = runner.current()
        assert step is not None
        assert step.step_number == 1

        # Call again, same result
        step2 = runner.current()
        assert step2 is not None
        assert step2.step_number == 1
        assert runner.current_index == 0  # Didn't move

    def test_empty_steps_list(self):
        """Handles empty steps list gracefully."""
        runner = AlgorithmRunner.from_steps("Test", [])

        assert runner.current() is None
        assert runner.advance() is None
        assert runner.rewind() is None
        assert runner.total_steps == 0

    def test_is_complete_true_when_at_complete_step(self):
        """is_complete is True when current step has is_complete=True."""
        steps = [make_step(1), make_step(2, is_complete=True)]
        runner = AlgorithmRunner.from_steps("Test", steps)

        runner.advance()
        assert not runner.is_complete

        runner.advance()
        assert runner.is_complete

    def test_total_steps_known_for_from_steps(self):
        """total_steps returns count when created from list."""
        steps = [make_step(1), make_step(2), make_step(3)]
        runner = AlgorithmRunner.from_steps("Test", steps)

        assert runner.total_steps == 3


class TestAlgorithmRunnerFromGenerator:
    """Tests for AlgorithmRunner created from generator."""

    def test_create_from_generator(self):
        """Can create runner from generator."""
        gen = make_generator(3)
        runner = AlgorithmRunner.from_generator("Test", gen)

        assert runner.name == "Test"
        assert len(runner.steps) == 0  # Not collected yet
        assert runner.current_index == -1

    def test_advance_collects_steps_lazily(self):
        """advance() collects steps from generator on demand."""
        gen = make_generator(3)
        runner = AlgorithmRunner.from_generator("Test", gen)

        step = runner.advance()
        assert step is not None
        assert step.step_number == 1
        assert len(runner.steps) == 1

        step = runner.advance()
        assert step is not None
        assert step.step_number == 2
        assert len(runner.steps) == 2

    def test_rewind_uses_collected_steps(self):
        """rewind() can navigate back through collected steps."""
        gen = make_generator(3)
        runner = AlgorithmRunner.from_generator("Test", gen)

        runner.advance()
        runner.advance()
        runner.advance()
        assert len(runner.steps) == 3

        step = runner.rewind()
        assert step is not None
        assert step.step_number == 2

        step = runner.rewind()
        assert step is not None
        assert step.step_number == 1

    def test_reset_allows_replay(self):
        """After reset, can advance through collected steps again."""
        gen = make_generator(3)
        runner = AlgorithmRunner.from_generator("Test", gen)

        # Exhaust generator
        runner.advance()
        runner.advance()
        runner.advance()
        runner.advance()  # Returns None

        runner.reset()

        # Can replay from collected steps
        step = runner.advance()
        assert step is not None
        assert step.step_number == 1

    def test_total_steps_none_while_generator_active(self):
        """total_steps is None while generator not exhausted."""
        gen = make_generator(3)
        runner = AlgorithmRunner.from_generator("Test", gen)

        assert runner.total_steps is None

        runner.advance()
        assert runner.total_steps is None

    def test_total_steps_known_after_exhaustion(self):
        """total_steps returns count after generator exhausted."""
        gen = make_generator(3)
        runner = AlgorithmRunner.from_generator("Test", gen)

        # Exhaust
        while runner.advance() is not None:
            pass

        assert runner.total_steps == 3

    def test_generator_exhaustion(self):
        """advance() returns None when generator exhausted."""
        gen = make_generator(2)
        runner = AlgorithmRunner.from_generator("Test", gen)

        assert runner.advance() is not None
        assert runner.advance() is not None
        assert runner.advance() is None  # Generator exhausted
        assert runner.advance() is None  # Still None
