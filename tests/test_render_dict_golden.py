from dsa_visualizer.data_structures.render.hashmap import render_hashmap


def test_render_hashmap_empty() -> None:
    expected = (
        "Index\n"
        " 0 ──▶ NULL\n"
        " 1 ──▶ NULL\n"
        " 2 ──▶ NULL\n"
        " 3 ──▶ NULL\n"
        " 4 ──▶ NULL\n"
        "\n"
        "Node Structure\n"
        "┌────────┬────────┬────────┐\n"
        "│  key   │ value  │  next  │\n"
        "└────────┴────────┴────────┘\n"
        "                     NULL  "
    )
    assert render_hashmap({}) == expected


def test_render_hashmap_single() -> None:
    expected = (
        "Index\n"
        " 0 ──▶ NULL\n"
        " 1 ──▶ ┌─────┬───────┐ ──▶ NULL\n"
        "       │ a   │ 1     │\n"
        "       └─────┴───────┘\n"
        " 2 ──▶ NULL\n"
        " 3 ──▶ NULL\n"
        " 4 ──▶ NULL\n"
        "\n"
        "Node Structure\n"
        "┌────────┬────────┬────────┐\n"
        "│  key   │ value  │  next  │\n"
        "└────────┴────────┴────────┘\n"
        "    a        1       NULL  "
    )
    assert render_hashmap({"a": 1}) == expected


def test_render_hashmap_two() -> None:
    expected = (
        "Index\n"
        " 0 ──▶ ┌─────┬───────┐ ──▶ NULL\n"
        "       │ b   │ 2     │\n"
        "       └─────┴───────┘\n"
        " 1 ──▶ ┌─────┬───────┐ ──▶ NULL\n"
        "       │ a   │ 1     │\n"
        "       └─────┴───────┘\n"
        " 2 ──▶ NULL\n"
        " 3 ──▶ NULL\n"
        " 4 ──▶ NULL\n"
        "\n"
        "Node Structure\n"
        "┌────────┬────────┬────────┐\n"
        "│  key   │ value  │  next  │\n"
        "└────────┴────────┴────────┘\n"
        "    b        2       NULL  "
    )
    assert render_hashmap({"a": 1, "b": 2}) == expected


def test_render_hashmap_mutation_updates() -> None:
    values = {"a": 1}
    first = render_hashmap(values)
    values["b"] = 2
    second = render_hashmap(values)
    assert first != second
    assert second == render_hashmap({"a": 1, "b": 2})
