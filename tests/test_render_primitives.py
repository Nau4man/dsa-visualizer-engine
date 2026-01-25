from dsa_visualizer.data_structures.render.primitive import render_primitive


def test_render_int_includes_value() -> None:
    text = render_primitive("x", 42)
    assert "type: int" in text
    assert "value: 42" in text


def test_render_bool_includes_value() -> None:
    text = render_primitive("flag", True)
    assert "type: bool" in text
    assert "value: true" in text


def test_render_char_includes_codepoint() -> None:
    text = render_primitive("ch", "A")
    assert "type: char (ASCII)" in text
    assert "value: 'A' (65)" in text


def test_render_float_includes_value() -> None:
    text = render_primitive("pi", 3.5)
    assert "type: float32" in text
    assert "value: 3.5" in text


def test_render_null_includes_meaning() -> None:
    text = render_primitive("n", None)
    assert "type: NULL" in text
    assert "meaning: no object" in text


def test_render_string_includes_value() -> None:
    text = render_primitive("s", "hi")
    assert "type: string" in text
    assert "value: \"hi\"" in text
