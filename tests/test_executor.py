from dsa_visualizer.core.executor import Executor


def test_executor_persists_state() -> None:
    executor = Executor()
    executor.execute("x = 1")
    executor.execute("x += 1")
    assert executor.globals["x"] == 2


def test_executor_error_returns_message() -> None:
    executor = Executor()
    result = executor.execute("raise ValueError('nope')")
    assert result.ok is False
    assert result.error


def test_executor_has_example_datasets() -> None:
    executor = Executor()
    examples = executor.globals["EXAMPLES"]

    # Check arrays exist
    assert "arrays" in examples
    assert "small" in examples["arrays"]
    assert "medium" in examples["arrays"]
    assert "large" in examples["arrays"]

    # Check trees exist
    assert "trees" in examples
    assert "balanced" in examples["trees"]
    assert "small" in examples["trees"]


def test_executor_example_arrays_are_sorted() -> None:
    executor = Executor()
    examples = executor.globals["EXAMPLES"]

    # Small, medium, large should be sorted for binary search
    assert examples["arrays"]["small"] == sorted(examples["arrays"]["small"])
    assert examples["arrays"]["medium"] == sorted(examples["arrays"]["medium"])
    assert examples["arrays"]["large"] == sorted(examples["arrays"]["large"])


def test_executor_can_use_examples_in_search() -> None:
    executor = Executor()
    executor.execute("data = EXAMPLES['arrays']['small']")
    executor.execute("search('linear', data, 5)")

    pending = executor.pop_pending_algorithm()
    assert pending is not None
