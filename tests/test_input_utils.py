from dsa_visualizer.ui.input_utils import clamp_input_height
from dsa_visualizer.ui.input_utils import indent_for_newline


def test_clamp_input_height_minimum() -> None:
    assert clamp_input_height("", 3, 10) == 3
    assert clamp_input_height("one line", 3, 10) == 3


def test_clamp_input_height_expands_with_lines() -> None:
    assert clamp_input_height("a\nb\nc", 3, 10) == 3
    assert clamp_input_height("a\nb\nc\nd", 3, 10) == 4
    assert clamp_input_height("a\n", 3, 10) == 3


def test_clamp_input_height_caps_at_max() -> None:
    text = "\n".join(str(index) for index in range(20))
    assert clamp_input_height(text, 3, 10) == 10


def test_indent_for_newline_on_block_start() -> None:
    assert indent_for_newline("for i in range(3):") == "    "
    assert indent_for_newline("    if True:") == "        "


def test_indent_for_newline_none_for_non_block() -> None:
    assert indent_for_newline("print('hi')") is None
