"""Tests for interpolation search algorithm."""

from dsa_visualizer.algorithms.search.interpolation import interpolation_search


class TestInterpolationSearchResults:
    """Tests for interpolation search correctness."""

    def test_find_element_at_beginning(self):
        """Finds element at index 0."""
        arr = [10, 20, 30, 40, 50, 60, 70, 80, 90]
        steps = list(interpolation_search(arr, 10))

        final_step = steps[-1]
        assert final_step.is_complete
        assert final_step.result == 0

    def test_find_element_in_middle(self):
        """Finds element in middle."""
        arr = [10, 20, 30, 40, 50, 60, 70, 80, 90]
        steps = list(interpolation_search(arr, 50))

        final_step = steps[-1]
        assert final_step.is_complete
        assert final_step.result == 4

    def test_find_element_at_end(self):
        """Finds element at last index."""
        arr = [10, 20, 30, 40, 50, 60, 70, 80, 90]
        steps = list(interpolation_search(arr, 90))

        final_step = steps[-1]
        assert final_step.is_complete
        assert final_step.result == 8

    def test_element_not_found(self):
        """Returns -1 when element not in array."""
        arr = [10, 20, 30, 40, 50]
        steps = list(interpolation_search(arr, 25))

        final_step = steps[-1]
        assert final_step.is_complete
        assert final_step.result == -1

    def test_empty_array(self):
        """Returns -1 for empty array."""
        steps = list(interpolation_search([], 10))

        assert len(steps) == 1
        final_step = steps[0]
        assert final_step.is_complete
        assert final_step.result == -1

    def test_single_element_found(self):
        """Finds element in single-element array."""
        steps = list(interpolation_search([42], 42))

        final_step = steps[-1]
        assert final_step.is_complete
        assert final_step.result == 0

    def test_single_element_not_found(self):
        """Returns -1 for single-element array when not found."""
        steps = list(interpolation_search([42], 99))

        final_step = steps[-1]
        assert final_step.is_complete
        assert final_step.result == -1

    def test_target_out_of_range_low(self):
        """Returns -1 when target smaller than all elements."""
        arr = [10, 20, 30, 40, 50]
        steps = list(interpolation_search(arr, 5))

        final_step = steps[-1]
        assert final_step.is_complete
        assert final_step.result == -1

    def test_target_out_of_range_high(self):
        """Returns -1 when target larger than all elements."""
        arr = [10, 20, 30, 40, 50]
        steps = list(interpolation_search(arr, 100))

        final_step = steps[-1]
        assert final_step.is_complete
        assert final_step.result == -1


class TestInterpolationSearchSteps:
    """Tests for interpolation search step generation."""

    def test_interpolation_mentioned(self):
        """Interpolation is mentioned in steps."""
        arr = [10, 20, 30, 40, 50, 60, 70, 80, 90]
        steps = list(interpolation_search(arr, 50))

        actions = " ".join(s.action for s in steps)
        assert "interpolat" in actions.lower()

    def test_boundaries_shown(self):
        """Search boundaries shown in highlights."""
        arr = [10, 20, 30, 40, 50]
        steps = list(interpolation_search(arr, 30))

        # Should have boundaries at some point
        has_boundaries = any(s.highlights.boundaries is not None for s in steps)
        assert has_boundaries

    def test_uniform_distribution_efficient(self):
        """Efficient on uniformly distributed data."""
        # Uniformly distributed array
        arr = list(range(0, 1000, 10))  # 100 elements
        steps = list(interpolation_search(arr, 500))

        # Should find quickly (much fewer than log2(100) iterations)
        # For uniform distribution, often finds in 1-3 iterations
        assert len(steps) <= 10

    def test_found_highlight_on_match(self):
        """Found highlight set correctly when match found."""
        arr = [10, 20, 30, 40, 50]
        steps = list(interpolation_search(arr, 30))

        final_step = steps[-1]
        assert 2 in final_step.highlights.found


class TestInterpolationSearchGenerator:
    """Tests for generator behavior."""

    def test_is_generator(self):
        """interpolation_search returns a generator."""
        result = interpolation_search([1, 2, 3], 2)
        assert hasattr(result, "__iter__")
        assert hasattr(result, "__next__")

    def test_all_steps_have_data(self):
        """All steps contain the original data."""
        arr = [10, 20, 30, 40, 50]
        steps = list(interpolation_search(arr, 30))

        for step in steps:
            assert step.data == arr


class TestInterpolationSearchEdgeCases:
    """Edge case tests for interpolation search."""

    def test_all_same_values(self):
        """Handles array with all same values."""
        arr = [5, 5, 5, 5, 5]
        steps = list(interpolation_search(arr, 5))

        final_step = steps[-1]
        assert final_step.is_complete
        # Should find one of them (position 0 due to formula)
        assert final_step.result in [0, 1, 2, 3, 4]

    def test_two_elements_find_first(self):
        """Finds first of two elements."""
        arr = [10, 20]
        steps = list(interpolation_search(arr, 10))

        final_step = steps[-1]
        assert final_step.is_complete
        assert final_step.result == 0

    def test_two_elements_find_second(self):
        """Finds second of two elements."""
        arr = [10, 20]
        steps = list(interpolation_search(arr, 20))

        final_step = steps[-1]
        assert final_step.is_complete
        assert final_step.result == 1
