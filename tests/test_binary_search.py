"""Tests for binary search algorithm."""

import math

from dsa_visualizer.algorithms.search.binary import binary_search


class TestBinarySearchResults:
    """Tests for binary search correctness."""

    def test_find_element_at_beginning(self):
        """Finds element at index 0."""
        arr = [10, 20, 30, 40, 50]
        steps = list(binary_search(arr, 10))

        final_step = steps[-1]
        assert final_step.is_complete
        assert final_step.result == 0

    def test_find_element_in_middle(self):
        """Finds element at middle index."""
        arr = [10, 20, 30, 40, 50]
        steps = list(binary_search(arr, 30))

        final_step = steps[-1]
        assert final_step.is_complete
        assert final_step.result == 2

    def test_find_element_at_end(self):
        """Finds element at last index."""
        arr = [10, 20, 30, 40, 50]
        steps = list(binary_search(arr, 50))

        final_step = steps[-1]
        assert final_step.is_complete
        assert final_step.result == 4

    def test_element_not_found(self):
        """Returns -1 when element not in array."""
        arr = [10, 20, 30, 40, 50]
        steps = list(binary_search(arr, 25))

        final_step = steps[-1]
        assert final_step.is_complete
        assert final_step.result == -1

    def test_empty_array(self):
        """Returns -1 for empty array."""
        steps = list(binary_search([], 10))

        assert len(steps) == 1
        final_step = steps[0]
        assert final_step.is_complete
        assert final_step.result == -1

    def test_single_element_found(self):
        """Finds element in single-element array."""
        steps = list(binary_search([42], 42))

        final_step = steps[-1]
        assert final_step.is_complete
        assert final_step.result == 0

    def test_single_element_not_found(self):
        """Returns -1 for single-element array when not found."""
        steps = list(binary_search([42], 99))

        final_step = steps[-1]
        assert final_step.is_complete
        assert final_step.result == -1

    def test_target_smaller_than_all(self):
        """Returns -1 when target smaller than all elements."""
        arr = [10, 20, 30, 40, 50]
        steps = list(binary_search(arr, 5))

        final_step = steps[-1]
        assert final_step.is_complete
        assert final_step.result == -1

    def test_target_larger_than_all(self):
        """Returns -1 when target larger than all elements."""
        arr = [10, 20, 30, 40, 50]
        steps = list(binary_search(arr, 100))

        final_step = steps[-1]
        assert final_step.is_complete
        assert final_step.result == -1


class TestBinarySearchSteps:
    """Tests for binary search step generation."""

    def test_logarithmic_step_count(self):
        """Step count is O(log n)."""
        arr = list(range(0, 1000, 10))  # 100 elements
        steps = list(binary_search(arr, 990))  # Last element

        # Should be around log2(100) * 2 (each iteration has 2 steps)
        # Plus maybe 1-2 extra for final steps
        max_steps = 2 * math.ceil(math.log2(100)) + 2
        assert len(steps) <= max_steps

    def test_boundaries_shown(self):
        """Search boundaries are shown in highlights."""
        arr = [10, 20, 30, 40, 50]
        steps = list(binary_search(arr, 20))

        # First step should show boundaries
        first_step = steps[0]
        assert first_step.highlights.boundaries is not None
        low, high = first_step.highlights.boundaries
        assert low == 0
        assert high == 4

    def test_boundaries_narrow(self):
        """Boundaries narrow as search progresses."""
        arr = [10, 20, 30, 40, 50, 60, 70, 80, 90]
        steps = list(binary_search(arr, 80))

        # Collect all boundary ranges
        boundary_ranges = []
        for step in steps:
            if step.highlights.boundaries is not None:
                boundary_ranges.append(step.highlights.boundaries)

        # Boundaries should narrow (or stay same)
        for i in range(1, len(boundary_ranges)):
            prev_low, prev_high = boundary_ranges[i - 1]
            curr_low, curr_high = boundary_ranges[i]
            prev_range = prev_high - prev_low
            curr_range = curr_high - curr_low
            assert curr_range <= prev_range

    def test_mid_highlighted(self):
        """Mid element is highlighted as current."""
        arr = [10, 20, 30, 40, 50]
        steps = list(binary_search(arr, 30))

        # First step mid should be 2 (middle of 0-4)
        first_step = steps[0]
        assert 2 in first_step.highlights.current

    def test_found_highlight_on_match(self):
        """Found highlight set correctly when match found."""
        arr = [10, 20, 30, 40, 50]
        steps = list(binary_search(arr, 30))

        final_step = steps[-1]
        assert 2 in final_step.highlights.found

    def test_action_describes_comparison(self):
        """Action text describes comparisons."""
        arr = [10, 20, 30, 40, 50]
        steps = list(binary_search(arr, 10))

        # Should have actions describing comparisons
        actions = [s.action for s in steps]
        action_text = " ".join(actions)

        # Should mention searching left or right
        assert "left" in action_text.lower() or "found" in action_text.lower()


class TestBinarySearchGenerator:
    """Tests for generator behavior."""

    def test_is_generator(self):
        """binary_search returns a generator."""
        result = binary_search([1, 2, 3], 2)
        assert hasattr(result, "__iter__")
        assert hasattr(result, "__next__")

    def test_can_iterate_step_by_step(self):
        """Can consume steps one at a time."""
        gen = binary_search([10, 20, 30, 40, 50], 30)

        step1 = next(gen)
        assert step1.step_number == 1
        assert not step1.is_complete

    def test_all_steps_have_data(self):
        """All steps contain the original data."""
        arr = [10, 20, 30, 40, 50]
        steps = list(binary_search(arr, 30))

        for step in steps:
            assert step.data == arr
