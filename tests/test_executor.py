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
