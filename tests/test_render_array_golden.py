from dsa_visualizer.data_structures.render.array import render_array


def test_render_array_empty() -> None:
    assert render_array([]) == "(empty)"


def test_render_array_single() -> None:
    expected = (
        "        ┌────┐\n"
        "Index → │ 0  │\n"
        "        ├────┤\n"
        "Array → │ 0  │\n"
        "        └────┘"
    )
    assert render_array([0]) == expected


def test_render_array_two() -> None:
    expected = (
        "        ┌────┬────┐\n"
        "Index → │ 0  │ 1  │\n"
        "        ├────┼────┤\n"
        "Array → │ 0  │ 1  │\n"
        "        └────┴────┘"
    )
    assert render_array([0, 1]) == expected


def test_render_array_three() -> None:
    expected = (
        "        ┌────┬────┬────┐\n"
        "Index → │ 0  │ 1  │ 2  │\n"
        "        ├────┼────┼────┤\n"
        "Array → │ 0  │ 1  │ 2  │\n"
        "        └────┴────┴────┘"
    )
    assert render_array([0, 1, 2]) == expected


def test_render_array_mutation_updates() -> None:
    values = [0, 1]
    first = render_array(values)
    values.append(2)
    second = render_array(values)
    assert first != second
    assert second == render_array([0, 1, 2])
