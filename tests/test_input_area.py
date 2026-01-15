from textual.binding import Binding

from dsa_visualizer.ui.input_area import InputArea


def test_input_area_has_select_all_binding() -> None:
    bindings = [binding for binding in InputArea.BINDINGS if binding.key == "ctrl+a"]
    assert bindings
    assert any(
        binding.action == "select_all" and isinstance(binding, Binding)
        for binding in bindings
    )
