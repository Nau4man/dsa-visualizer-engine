from dsa_visualizer.core.snapshotter import Snapshotter, diff_snapshots


def test_aliasing_preserves_identity() -> None:
    snapshotter = Snapshotter()
    values: dict[str, object] = {}
    values["a"] = []
    values["b"] = values["a"]
    snapshot = snapshotter.snapshot(values)
    assert snapshot.names["a"] == snapshot.names["b"]
    record = snapshot.objects[snapshot.names["a"]]
    assert record.address == hex(id(values["a"]))


def test_rebinding_creates_new_identity() -> None:
    snapshotter = Snapshotter()
    values: dict[str, object] = {}
    values["a"] = []
    first = snapshotter.snapshot(values)
    values["a"] = []
    second = snapshotter.snapshot(values)
    assert first.names["a"] != second.names["a"]


def test_primitive_capture() -> None:
    snapshotter = Snapshotter()
    values: dict[str, object] = {"x": 3}
    snapshot = snapshotter.snapshot(values)
    assert snapshot.names["x"] == 3


def test_diff_snapshots_tracks_changes() -> None:
    snapshotter = Snapshotter()
    values: dict[str, object] = {"x": 1}
    before = snapshotter.snapshot(values)
    values["x"] = 2
    values["y"] = []
    after = snapshotter.snapshot(values)
    delta = diff_snapshots(before, after)
    assert delta.names["x"] == 2
    assert "y" in delta.names
