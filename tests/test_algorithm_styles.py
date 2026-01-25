"""Tests for algorithm style converter."""

from dsa_visualizer.algorithms.render.highlights import (
    MARKER_CURRENT,
    MARKER_VISITED,
    MARKER_FOUND,
    MARKER_COMPARING,
)
from dsa_visualizer.algorithms.ui.styles import (
    apply_algorithm_styles,
    style_index_cell,
    get_legend_text,
    MARKER_STYLES,
)


class TestApplyAlgorithmStyles:
    """Tests for apply_algorithm_styles function."""

    def test_plain_text_unchanged(self):
        """Plain text without markers passes through."""
        text = apply_algorithm_styles("Hello World")
        assert text.plain == "Hello World"

    def test_current_marker_styled(self):
        """Current marker gets styled."""
        text = apply_algorithm_styles(f"{MARKER_CURRENT}0")
        assert text.plain == f"{MARKER_CURRENT}0"
        # Check that style was applied (spans exist)
        assert len(text._spans) > 0

    def test_visited_marker_styled(self):
        """Visited marker gets styled."""
        text = apply_algorithm_styles(f"{MARKER_VISITED}1")
        assert text.plain == f"{MARKER_VISITED}1"

    def test_found_marker_styled(self):
        """Found marker gets styled."""
        text = apply_algorithm_styles(f"{MARKER_FOUND}2")
        assert text.plain == f"{MARKER_FOUND}2"

    def test_comparing_marker_styled(self):
        """Comparing marker gets styled."""
        text = apply_algorithm_styles(f"{MARKER_COMPARING}3")
        assert text.plain == f"{MARKER_COMPARING}3"

    def test_mixed_markers_styled(self):
        """Multiple different markers in same text."""
        input_text = f"│ {MARKER_VISITED}0 │ {MARKER_CURRENT}1 │ 2 │"
        text = apply_algorithm_styles(input_text)
        assert text.plain == input_text

    def test_multi_digit_index_styled(self):
        """Marker followed by multi-digit number."""
        text = apply_algorithm_styles(f"{MARKER_CURRENT}123")
        assert text.plain == f"{MARKER_CURRENT}123"

    def test_empty_string(self):
        """Empty string returns empty Text."""
        text = apply_algorithm_styles("")
        assert text.plain == ""


class TestStyleIndexCell:
    """Tests for style_index_cell function."""

    def test_no_marker(self):
        """Index without marker."""
        text = style_index_cell(5, "")
        assert text.plain == "5"

    def test_with_current_marker(self):
        """Index with current marker."""
        text = style_index_cell(3, MARKER_CURRENT)
        assert MARKER_CURRENT in text.plain
        assert "3" in text.plain

    def test_with_found_marker(self):
        """Index with found marker."""
        text = style_index_cell(7, MARKER_FOUND)
        assert MARKER_FOUND in text.plain
        assert "7" in text.plain


class TestGetLegendText:
    """Tests for get_legend_text function."""

    def test_contains_all_markers(self):
        """Legend contains all marker types."""
        text = get_legend_text()
        plain = text.plain

        assert MARKER_CURRENT in plain
        assert MARKER_COMPARING in plain
        assert MARKER_VISITED in plain
        assert MARKER_FOUND in plain
        assert "[" in plain
        assert "]" in plain

    def test_contains_explanations(self):
        """Legend contains explanations."""
        text = get_legend_text()
        plain = text.plain

        assert "current" in plain
        assert "comparing" in plain
        assert "visited" in plain
        assert "found" in plain
        assert "boundaries" in plain


class TestMarkerStyles:
    """Tests for MARKER_STYLES mapping."""

    def test_all_markers_have_styles(self):
        """All markers have defined styles."""
        assert MARKER_CURRENT in MARKER_STYLES
        assert MARKER_VISITED in MARKER_STYLES
        assert MARKER_FOUND in MARKER_STYLES
        assert MARKER_COMPARING in MARKER_STYLES

    def test_styles_are_strings(self):
        """All styles are non-empty strings."""
        for marker, style in MARKER_STYLES.items():
            assert isinstance(style, str)
            assert len(style) > 0
