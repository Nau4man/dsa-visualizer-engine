from __future__ import annotations


def render_graph(adjacency: dict[object, list[object]], *, directed: bool) -> str:
    nodes = sorted(adjacency.keys(), key=lambda item: str(item))
    edges = _collect_edges(adjacency, directed=directed)
    edge_label = "Edges" if not directed else "Directed Edges"
    lines: list[str] = []
    if edges:
        edge_text = ", ".join(edges)
        lines.append(f"{edge_label}: {edge_text}")
    else:
        lines.append(f"{edge_label}: (none)")
    lines.append("")
    lines.append("Adjacency list:")
    lines.append("")
    for node in nodes:
        neighbors = adjacency.get(node, [])
        neighbor_text = ", ".join(str(item) for item in neighbors) or "(none)"
        lines.append(f"{node} ──▶ {neighbor_text}")
    return "\n".join(lines)


def _collect_edges(
    adjacency: dict[object, list[object]], *, directed: bool
) -> list[str]:
    edges: list[str] = []
    seen: set[tuple[str, str]] = set()
    for node, neighbors in adjacency.items():
        for neighbor in neighbors:
            left = str(node)
            right = str(neighbor)
            if directed:
                edges.append(f"{left}→{right}")
            else:
                key = tuple(sorted((left, right)))
                if key in seen:
                    continue
                seen.add(key)
                edges.append(f"{key[0]}{key[1]}")
    return edges
