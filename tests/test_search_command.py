"""Tests for search command functionality."""

from dsa_visualizer.core.executor import (
    Executor,
    SEARCH_ALGORITHMS,
    ALGORITHM_NAMES,
)


class TestSearchCommand:
    """Tests for the search command in executor."""

    def test_search_function_in_globals(self):
        """search function is available in executor globals."""
        executor = Executor()
        assert "search" in executor.globals
        assert callable(executor.globals["search"])

    def test_search_linear_creates_pending(self):
        """search("linear", ...) creates pending algorithm."""
        executor = Executor()
        result = executor.execute('search("linear", [1, 2, 3], 2)')

        assert result.ok
        pending = executor.pop_pending_algorithm()
        assert pending is not None
        assert pending.runner.name == "Linear Search"
        assert pending.data == [1, 2, 3]

    def test_search_returns_status_message(self):
        """search() returns a status message."""
        executor = Executor()

        # Execute with explicit capture of return value
        executor.execute('result = search("linear", [1, 2, 3], 2)')

        result_value = executor.globals.get("result")
        assert result_value is not None
        assert "Linear Search" in result_value

    def test_search_unknown_algorithm_raises(self):
        """search() with unknown algorithm raises ValueError."""
        executor = Executor()
        result = executor.execute('search("unknown", [1, 2, 3], 2)')

        assert not result.ok
        assert "Unknown algorithm" in result.error

    def test_search_available_algorithms_in_error(self):
        """Error message lists available algorithms."""
        executor = Executor()
        result = executor.execute('search("bad", [1, 2, 3], 2)')

        assert "linear" in result.error.lower()

    def test_pending_cleared_before_execution(self):
        """Pending algorithm is cleared before new execution."""
        executor = Executor()

        # First search
        executor.execute('search("linear", [1, 2, 3], 2)')
        pending1 = executor.pending_algorithm
        assert pending1 is not None

        # Non-search execution clears pending
        executor.execute('x = 1')
        pending2 = executor.pending_algorithm
        assert pending2 is None

    def test_pop_pending_clears_it(self):
        """pop_pending_algorithm clears the pending algorithm."""
        executor = Executor()
        executor.execute('search("linear", [1, 2, 3], 2)')

        pending1 = executor.pop_pending_algorithm()
        pending2 = executor.pop_pending_algorithm()

        assert pending1 is not None
        assert pending2 is None

    def test_search_preserves_data_copy(self):
        """search() makes a copy of the data."""
        executor = Executor()
        executor.execute('arr = [1, 2, 3]')
        executor.execute('search("linear", arr, 2)')

        pending = executor.pop_pending_algorithm()
        assert pending.data == [1, 2, 3]

        # Modify original, pending should be unaffected
        executor.execute('arr.append(4)')
        assert pending.data == [1, 2, 3]


class TestSearchAlgorithmRegistry:
    """Tests for algorithm registry."""

    def test_linear_search_registered(self):
        """Linear search is in the registry."""
        assert "linear" in SEARCH_ALGORITHMS
        assert "linear" in ALGORITHM_NAMES

    def test_algorithm_names_match_registry(self):
        """All registered algorithms have display names."""
        for algo_key in SEARCH_ALGORITHMS:
            assert algo_key in ALGORITHM_NAMES


class TestSearchWithRunner:
    """Tests for runner created by search command."""

    def test_runner_can_advance(self):
        """Runner from search can advance through steps."""
        executor = Executor()
        executor.execute('search("linear", [10, 20, 30], 20)')

        pending = executor.pop_pending_algorithm()
        runner = pending.runner

        step1 = runner.advance()
        assert step1 is not None
        assert step1.step_number == 1

    def test_runner_produces_valid_steps(self):
        """Steps from runner have expected structure."""
        executor = Executor()
        executor.execute('search("linear", [10, 20, 30], 20)')

        pending = executor.pop_pending_algorithm()
        runner = pending.runner

        step = runner.advance()
        assert step.action is not None
        assert step.highlights is not None
        assert step.data == [10, 20, 30]
