from dsa_visualizer.render.graph import render_graph


def test_render_undirected_graph() -> None:
    adjacency = {"A": ["B", "C"], "B": ["A"], "C": ["A"]}
    expected = (
        "Edges: AB, AC\n"
        "\n"
        "Adjacency list:\n"
        "\n"
        "A ──▶ B, C\n"
        "B ──▶ A\n"
        "C ──▶ A"
    )
    assert render_graph(adjacency, directed=False) == expected


def test_render_directed_graph() -> None:
    adjacency = {"A": ["B"], "B": ["C"], "C": []}
    expected = (
        "Directed Edges: A→B, B→C\n"
        "\n"
        "Adjacency list:\n"
        "\n"
        "A ──▶ B\n"
        "B ──▶ C\n"
        "C ──▶ (none)"
    )
    assert render_graph(adjacency, directed=True) == expected
