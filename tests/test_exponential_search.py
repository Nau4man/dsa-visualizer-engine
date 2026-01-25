"""Tests for exponential search algorithm."""

from dsa_visualizer.algorithms.search.exponential import exponential_search


class TestExponentialSearchResults:
    """Tests for exponential search correctness."""

    def test_find_element_at_beginning(self):
        """Finds element at index 0."""
        arr = [10, 20, 30, 40, 50, 60, 70, 80, 90]
        steps = list(exponential_search(arr, 10))

        final_step = steps[-1]
        assert final_step.is_complete
        assert final_step.result == 0

    def test_find_element_in_middle(self):
        """Finds element in middle."""
        arr = [10, 20, 30, 40, 50, 60, 70, 80, 90]
        steps = list(exponential_search(arr, 50))

        final_step = steps[-1]
        assert final_step.is_complete
        assert final_step.result == 4

    def test_find_element_at_end(self):
        """Finds element at last index."""
        arr = [10, 20, 30, 40, 50, 60, 70, 80, 90]
        steps = list(exponential_search(arr, 90))

        final_step = steps[-1]
        assert final_step.is_complete
        assert final_step.result == 8

    def test_element_not_found(self):
        """Returns -1 when element not in array."""
        arr = [10, 20, 30, 40, 50]
        steps = list(exponential_search(arr, 25))

        final_step = steps[-1]
        assert final_step.is_complete
        assert final_step.result == -1

    def test_empty_array(self):
        """Returns -1 for empty array."""
        steps = list(exponential_search([], 10))

        assert len(steps) == 1
        final_step = steps[0]
        assert final_step.is_complete
        assert final_step.result == -1

    def test_single_element_found(self):
        """Finds element in single-element array."""
        steps = list(exponential_search([42], 42))

        final_step = steps[-1]
        assert final_step.is_complete
        assert final_step.result == 0

    def test_single_element_not_found(self):
        """Returns -1 for single-element array when not found."""
        steps = list(exponential_search([42], 99))

        final_step = steps[-1]
        assert final_step.is_complete
        assert final_step.result == -1

    def test_find_at_index_one(self):
        """Finds element at index 1."""
        arr = [10, 20, 30, 40, 50]
        steps = list(exponential_search(arr, 20))

        final_step = steps[-1]
        assert final_step.is_complete
        assert final_step.result == 1


class TestExponentialSearchSteps:
    """Tests for exponential search step generation."""

    def test_exponential_expansion_mentioned(self):
        """Exponential expansion is mentioned in steps."""
        arr = list(range(0, 1000, 10))
        steps = list(exponential_search(arr, 500))

        actions = " ".join(s.action for s in steps)
        assert "exponential" in actions.lower() or "expand" in actions.lower()

    def test_binary_search_phase(self):
        """Binary search phase is mentioned."""
        arr = list(range(0, 1000, 10))
        steps = list(exponential_search(arr, 500))

        actions = " ".join(s.action for s in steps)
        assert "binary" in actions.lower()

    def test_boundaries_shown(self):
        """Search boundaries shown in highlights."""
        arr = [10, 20, 30, 40, 50]
        steps = list(exponential_search(arr, 30))

        has_boundaries = any(s.highlights.boundaries is not None for s in steps)
        assert has_boundaries

    def test_efficient_for_early_elements(self):
        """Efficient when target is near the beginning."""
        arr = list(range(0, 10000, 10))  # 1000 elements
        steps = list(exponential_search(arr, 30))  # Element at index 3

        # Should find quickly (exponential finds small range fast)
        assert len(steps) <= 15

    def test_found_highlight_on_match(self):
        """Found highlight set correctly when match found."""
        arr = [10, 20, 30, 40, 50]
        steps = list(exponential_search(arr, 30))

        final_step = steps[-1]
        assert 2 in final_step.highlights.found


class TestExponentialSearchGenerator:
    """Tests for generator behavior."""

    def test_is_generator(self):
        """exponential_search returns a generator."""
        result = exponential_search([1, 2, 3], 2)
        assert hasattr(result, "__iter__")
        assert hasattr(result, "__next__")

    def test_all_steps_have_data(self):
        """All steps contain the original data."""
        arr = [10, 20, 30, 40, 50]
        steps = list(exponential_search(arr, 30))

        for step in steps:
            assert step.data == arr
