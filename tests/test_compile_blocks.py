from dsa_visualizer.core.input_accumulator import classify_buffer


def test_complete_single_line() -> None:
    assert classify_buffer("arr=[0,1]").status == "complete"


def test_incomplete_for_loop() -> None:
    assert classify_buffer("for i in range(3):").status == "incomplete"


def test_complete_for_loop_with_body() -> None:
    result = classify_buffer("for i in range(3):\n    pass")
    assert result.status == "complete"


def test_incomplete_while_loop() -> None:
    assert classify_buffer("while True:").status == "incomplete"


def test_complete_while_loop_with_body() -> None:
    result = classify_buffer("while True:\n    break")
    assert result.status == "complete"


def test_incomplete_if_block() -> None:
    assert classify_buffer("if True:").status == "incomplete"


def test_complete_if_block_with_body() -> None:
    result = classify_buffer("if True:\n    pass")
    assert result.status == "complete"


def test_incomplete_function_def() -> None:
    assert classify_buffer("def greet():").status == "incomplete"


def test_complete_function_def_with_body() -> None:
    result = classify_buffer("def greet():\n    return 'hi'")
    assert result.status == "complete"


def test_incomplete_with_block() -> None:
    assert classify_buffer("with open('a') as f:").status == "incomplete"


def test_complete_with_block_with_body() -> None:
    result = classify_buffer("with open('a') as f:\n    pass")
    assert result.status == "complete"


def test_incomplete_try_block() -> None:
    assert classify_buffer("try:").status == "incomplete"


def test_complete_try_except_block() -> None:
    result = classify_buffer("try:\n    pass\nexcept Exception:\n    pass")
    assert result.status == "complete"


def test_incomplete_paren() -> None:
    assert classify_buffer("x = (").status == "incomplete"


def test_complete_paren() -> None:
    assert classify_buffer("x = (1+2)").status == "complete"


def test_syntax_error_returns_error_text() -> None:
    result = classify_buffer("x = )")
    assert result.status == "error"
    assert result.error


def test_force_submit_incomplete_is_error() -> None:
    result = classify_buffer("for i in range(3):", force_submit=True)
    assert result.status == "error"
    assert result.error
