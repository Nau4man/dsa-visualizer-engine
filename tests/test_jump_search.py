"""Tests for jump search algorithm."""

import math

from dsa_visualizer.algorithms.search.jump import jump_search


class TestJumpSearchResults:
    """Tests for jump search correctness."""

    def test_find_element_at_beginning(self):
        """Finds element at index 0."""
        arr = [10, 20, 30, 40, 50, 60, 70, 80, 90]
        steps = list(jump_search(arr, 10))

        final_step = steps[-1]
        assert final_step.is_complete
        assert final_step.result == 0

    def test_find_element_in_middle(self):
        """Finds element in middle."""
        arr = [10, 20, 30, 40, 50, 60, 70, 80, 90]
        steps = list(jump_search(arr, 50))

        final_step = steps[-1]
        assert final_step.is_complete
        assert final_step.result == 4

    def test_find_element_at_end(self):
        """Finds element at last index."""
        arr = [10, 20, 30, 40, 50, 60, 70, 80, 90]
        steps = list(jump_search(arr, 90))

        final_step = steps[-1]
        assert final_step.is_complete
        assert final_step.result == 8

    def test_element_not_found(self):
        """Returns -1 when element not in array."""
        arr = [10, 20, 30, 40, 50]
        steps = list(jump_search(arr, 25))

        final_step = steps[-1]
        assert final_step.is_complete
        assert final_step.result == -1

    def test_empty_array(self):
        """Returns -1 for empty array."""
        steps = list(jump_search([], 10))

        assert len(steps) == 1
        final_step = steps[0]
        assert final_step.is_complete
        assert final_step.result == -1

    def test_single_element_found(self):
        """Finds element in single-element array."""
        steps = list(jump_search([42], 42))

        final_step = steps[-1]
        assert final_step.is_complete
        assert final_step.result == 0

    def test_single_element_not_found(self):
        """Returns -1 for single-element array when not found."""
        steps = list(jump_search([42], 99))

        final_step = steps[-1]
        assert final_step.is_complete
        assert final_step.result == -1


class TestJumpSearchSteps:
    """Tests for jump search step generation."""

    def test_jump_size_mentioned(self):
        """Jump size is mentioned in steps."""
        arr = list(range(0, 100, 10))  # 10 elements
        steps = list(jump_search(arr, 50))

        actions = " ".join(s.action for s in steps)
        assert "jump" in actions.lower()

    def test_sqrt_n_complexity(self):
        """Step count is approximately O(√n)."""
        arr = list(range(0, 1000, 10))  # 100 elements
        steps = list(jump_search(arr, 950))

        # Jump phase: ~√100 = 10 jumps max
        # Linear phase: ~√100 = 10 comparisons max
        # Total: ~20 steps + some overhead
        max_steps = 2 * int(math.sqrt(100)) + 10
        assert len(steps) <= max_steps

    def test_boundaries_shown(self):
        """Block boundaries shown in highlights."""
        arr = list(range(0, 100, 10))
        steps = list(jump_search(arr, 50))

        # Should have boundaries at some point
        has_boundaries = any(s.highlights.boundaries is not None for s in steps)
        assert has_boundaries

    def test_linear_search_within_block(self):
        """Does linear search within identified block."""
        arr = [10, 20, 30, 40, 50, 60, 70, 80, 90]
        steps = list(jump_search(arr, 35))  # Not in array

        actions = " ".join(s.action for s in steps)
        # Should mention linear search
        assert "linear" in actions.lower() or "check" in actions.lower()


class TestJumpSearchGenerator:
    """Tests for generator behavior."""

    def test_is_generator(self):
        """jump_search returns a generator."""
        result = jump_search([1, 2, 3], 2)
        assert hasattr(result, "__iter__")
        assert hasattr(result, "__next__")

    def test_all_steps_have_data(self):
        """All steps contain the original data."""
        arr = [10, 20, 30, 40, 50]
        steps = list(jump_search(arr, 30))

        for step in steps:
            assert step.data == arr
