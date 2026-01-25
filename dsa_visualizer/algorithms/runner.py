from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass, field

from dsa_visualizer.algorithms.types import AlgorithmStep


@dataclass
class AlgorithmRunner:
    """Manages step-by-step algorithm execution.

    Collects steps from an algorithm generator and allows navigation
    through them (forward, backward, reset).
    """

    name: str
    """Name of the algorithm being run."""

    steps: list[AlgorithmStep] = field(default_factory=list)
    """History of algorithm steps."""

    current_index: int = -1
    """Current position in steps (-1 means not started)."""

    _generator: Iterator[AlgorithmStep] | None = field(default=None, repr=False)
    """Internal generator for lazy step collection."""

    @classmethod
    def from_generator(
        cls, name: str, generator: Iterator[AlgorithmStep]
    ) -> AlgorithmRunner:
        """Create a runner from an algorithm generator.

        Steps are collected lazily as advance() is called.
        """
        return cls(name=name, steps=[], current_index=-1, _generator=generator)

    @classmethod
    def from_steps(cls, name: str, steps: list[AlgorithmStep]) -> AlgorithmRunner:
        """Create a runner from a pre-computed list of steps."""
        return cls(name=name, steps=list(steps), current_index=-1, _generator=None)

    def advance(self) -> AlgorithmStep | None:
        """Move forward one step and return it.

        If at the end of collected steps and generator exists,
        try to get the next step from the generator.

        Returns None if no more steps available.
        """
        next_index = self.current_index + 1

        # If we have the step already, just move to it
        if next_index < len(self.steps):
            self.current_index = next_index
            return self.steps[self.current_index]

        # Try to get next step from generator
        if self._generator is not None:
            try:
                step = next(self._generator)
                self.steps.append(step)
                self.current_index = next_index
                return step
            except StopIteration:
                self._generator = None
                return None

        return None

    def rewind(self) -> AlgorithmStep | None:
        """Move backward one step and return it.

        Returns None if already at the beginning (index -1).
        """
        if self.current_index <= -1:
            return None

        self.current_index -= 1

        if self.current_index == -1:
            return None

        return self.steps[self.current_index]

    def reset(self) -> None:
        """Reset to the beginning (before first step)."""
        self.current_index = -1

    def current(self) -> AlgorithmStep | None:
        """Get the current step without moving.

        Returns None if not started (index -1).
        """
        if self.current_index < 0 or self.current_index >= len(self.steps):
            return None
        return self.steps[self.current_index]

    @property
    def is_complete(self) -> bool:
        """Check if the algorithm has finished.

        True if we've seen a step with is_complete=True and
        we're at that step, or if generator is exhausted and
        we're at the last step.
        """
        current = self.current()
        if current is not None and current.is_complete:
            return True

        # Also consider complete if generator exhausted and at last step
        if self._generator is None and self.current_index == len(self.steps) - 1:
            return len(self.steps) > 0

        return False

    @property
    def total_steps(self) -> int | None:
        """Return total step count if known (generator exhausted), else None."""
        if self._generator is None:
            return len(self.steps)
        return None

    @property
    def step_number(self) -> int:
        """Return current step number (1-indexed), or 0 if not started."""
        return self.current_index + 1
