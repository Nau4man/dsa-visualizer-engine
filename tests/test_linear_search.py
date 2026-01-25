"""Tests for linear search algorithm."""

from dsa_visualizer.algorithms.search.linear import linear_search


class TestLinearSearchResults:
    """Tests for linear search correctness."""

    def test_find_element_at_beginning(self):
        """Finds element at index 0."""
        arr = [10, 20, 30, 40, 50]
        steps = list(linear_search(arr, 10))

        final_step = steps[-1]
        assert final_step.is_complete
        assert final_step.result == 0

    def test_find_element_in_middle(self):
        """Finds element in the middle of array."""
        arr = [10, 20, 30, 40, 50]
        steps = list(linear_search(arr, 30))

        final_step = steps[-1]
        assert final_step.is_complete
        assert final_step.result == 2

    def test_find_element_at_end(self):
        """Finds element at the last index."""
        arr = [10, 20, 30, 40, 50]
        steps = list(linear_search(arr, 50))

        final_step = steps[-1]
        assert final_step.is_complete
        assert final_step.result == 4

    def test_element_not_found(self):
        """Returns -1 when element not in array."""
        arr = [10, 20, 30, 40, 50]
        steps = list(linear_search(arr, 99))

        final_step = steps[-1]
        assert final_step.is_complete
        assert final_step.result == -1
        assert "not found" in final_step.action

    def test_empty_array(self):
        """Returns -1 for empty array."""
        steps = list(linear_search([], 10))

        assert len(steps) == 1
        final_step = steps[0]
        assert final_step.is_complete
        assert final_step.result == -1
        assert "empty" in final_step.action.lower()

    def test_single_element_found(self):
        """Finds element in single-element array."""
        steps = list(linear_search([42], 42))

        final_step = steps[-1]
        assert final_step.is_complete
        assert final_step.result == 0

    def test_single_element_not_found(self):
        """Returns -1 for single-element array when not found."""
        steps = list(linear_search([42], 99))

        final_step = steps[-1]
        assert final_step.is_complete
        assert final_step.result == -1

    def test_works_with_strings(self):
        """Works with string elements."""
        arr = ["apple", "banana", "cherry"]
        steps = list(linear_search(arr, "banana"))

        final_step = steps[-1]
        assert final_step.is_complete
        assert final_step.result == 1

    def test_finds_first_duplicate(self):
        """Finds first occurrence when duplicates exist."""
        arr = [10, 20, 30, 20, 40]
        steps = list(linear_search(arr, 20))

        final_step = steps[-1]
        assert final_step.is_complete
        assert final_step.result == 1  # First occurrence


class TestLinearSearchSteps:
    """Tests for linear search step generation."""

    def test_step_count_when_found_immediately(self):
        """Minimal steps when found at index 0."""
        arr = [10, 20, 30]
        steps = list(linear_search(arr, 10))

        # Should be: examine[0], found
        assert len(steps) == 2
        assert steps[-1].is_complete

    def test_step_count_when_not_found(self):
        """Full scan when element not found."""
        arr = [10, 20, 30]
        steps = list(linear_search(arr, 99))

        # For each element: examine + compare, then final not-found
        # 3 elements * 2 steps each + 1 final = 7 steps
        assert len(steps) == 7
        assert steps[-1].is_complete

    def test_steps_have_incrementing_numbers(self):
        """Step numbers increment correctly."""
        arr = [10, 20, 30]
        steps = list(linear_search(arr, 20))

        for i, step in enumerate(steps):
            assert step.step_number == i + 1

    def test_current_highlight_tracks_position(self):
        """Current highlight shows correct index."""
        arr = [10, 20, 30]
        steps = list(linear_search(arr, 30))

        # First examine step should have current={0}
        assert 0 in steps[0].highlights.current

        # Third examine step (index 2) - need to find the right step
        # Steps are: examine[0], compare[0], examine[1], compare[1], examine[2], found
        examine_step_2 = steps[4]  # examine index 2
        assert 2 in examine_step_2.highlights.current

    def test_visited_accumulates(self):
        """Visited set grows as search progresses."""
        arr = [10, 20, 30, 40]
        steps = list(linear_search(arr, 99))

        # After checking all elements, visited should contain all indices
        final_step = steps[-1]
        assert final_step.highlights.visited == frozenset({0, 1, 2, 3})

    def test_found_highlight_on_match(self):
        """Found highlight set correctly when match found."""
        arr = [10, 20, 30]
        steps = list(linear_search(arr, 20))

        final_step = steps[-1]
        assert 1 in final_step.highlights.found

    def test_data_preserved_in_steps(self):
        """Each step contains copy of original data."""
        arr = [10, 20, 30]
        steps = list(linear_search(arr, 20))

        for step in steps:
            assert step.data == [10, 20, 30]

    def test_action_describes_operation(self):
        """Action text describes what's happening."""
        arr = [10, 20, 30]
        steps = list(linear_search(arr, 20))

        # First step should mention examining index 0
        assert "index 0" in steps[0].action.lower() or "0" in steps[0].action

        # Final step should mention found
        assert "found" in steps[-1].action.lower()


class TestLinearSearchGenerator:
    """Tests for generator behavior."""

    def test_is_generator(self):
        """linear_search returns a generator."""
        result = linear_search([1, 2, 3], 2)
        assert hasattr(result, "__iter__")
        assert hasattr(result, "__next__")

    def test_can_iterate_step_by_step(self):
        """Can consume steps one at a time."""
        gen = linear_search([10, 20, 30], 20)

        step1 = next(gen)
        assert step1.step_number == 1
        assert not step1.is_complete

        step2 = next(gen)
        assert step2.step_number == 2

    def test_stops_early_when_found(self):
        """Generator stops after finding element."""
        arr = [10, 20, 30, 40, 50]
        steps = list(linear_search(arr, 20))

        # Should not have examined indices 2, 3, 4
        all_examined = set()
        for step in steps:
            all_examined.update(step.highlights.current)
            all_examined.update(step.highlights.visited)

        # Should have examined 0 and 1, found at 1
        assert 0 in all_examined
        assert 1 in all_examined
        # Should not have visited beyond the found element
        assert 2 not in steps[-1].highlights.visited
