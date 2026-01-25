"""Tests for highlighted array rendering."""

from dsa_visualizer.algorithms.types import HighlightContext
from dsa_visualizer.data_structures.render.array import render_array
from dsa_visualizer.algorithms.render.highlights import (
    MARKER_CURRENT,
    MARKER_VISITED,
    MARKER_FOUND,
    MARKER_COMPARING,
)


class TestArrayWithoutHighlights:
    """Tests that arrays without highlights render normally."""

    def test_no_highlights_unchanged(self):
        """Array without highlights parameter unchanged."""
        result = render_array([1, 2, 3])
        assert "Index" in result
        assert "Array" in result
        assert "│" in result

    def test_none_highlights_unchanged(self):
        """Array with highlights=None unchanged."""
        result1 = render_array([1, 2, 3])
        result2 = render_array([1, 2, 3], highlights=None)
        assert result1 == result2

    def test_empty_highlights_unchanged(self):
        """Array with empty HighlightContext unchanged."""
        result = render_array([1, 2, 3], highlights=HighlightContext())
        # Should have same structure as unhighlighted
        assert "Index" in result
        assert "Array" in result


class TestArrayWithCurrentHighlight:
    """Tests for current element highlighting."""

    def test_current_index_shows_marker(self):
        """Current index shows arrow marker."""
        ctx = HighlightContext(current=frozenset({1}))
        result = render_array([10, 20, 30], highlights=ctx)

        # Should contain the current marker before index 1
        assert f"{MARKER_CURRENT}1" in result

    def test_current_marker_not_on_other_indices(self):
        """Other indices don't have current marker."""
        ctx = HighlightContext(current=frozenset({1}))
        result = render_array([10, 20, 30], highlights=ctx)

        # Index 0 and 2 should not have arrow marker
        lines = result.split("\n")
        index_line = [line for line in lines if "Index" in line][0]
        # Should have →1 but not →0 or →2
        assert f"{MARKER_CURRENT}0" not in index_line
        assert f"{MARKER_CURRENT}2" not in index_line


class TestArrayWithVisitedHighlight:
    """Tests for visited element highlighting."""

    def test_visited_indices_show_markers(self):
        """Visited indices show dot markers."""
        ctx = HighlightContext(visited=frozenset({0, 1}))
        result = render_array([10, 20, 30], highlights=ctx)

        assert f"{MARKER_VISITED}0" in result
        assert f"{MARKER_VISITED}1" in result

    def test_unvisited_index_no_marker(self):
        """Unvisited indices have no marker."""
        ctx = HighlightContext(visited=frozenset({0}))
        result = render_array([10, 20, 30], highlights=ctx)

        # Index 2 should appear without marker
        lines = result.split("\n")
        index_line = [line for line in lines if "Index" in line][0]
        # Index 1 and 2 should not have visited marker
        assert f"{MARKER_VISITED}2" not in index_line


class TestArrayWithFoundHighlight:
    """Tests for found element highlighting."""

    def test_found_index_shows_marker(self):
        """Found index shows check marker."""
        ctx = HighlightContext(found=frozenset({2}))
        result = render_array([10, 20, 30], highlights=ctx)

        assert f"{MARKER_FOUND}2" in result


class TestArrayWithComparingHighlight:
    """Tests for comparing element highlighting."""

    def test_comparing_index_shows_marker(self):
        """Comparing index shows question marker."""
        ctx = HighlightContext(comparing=frozenset({1}))
        result = render_array([10, 20, 30], highlights=ctx)

        assert f"{MARKER_COMPARING}1" in result


class TestArrayWithBoundaries:
    """Tests for boundary markers."""

    def test_boundaries_show_brackets(self):
        """Boundaries show [ and ] markers."""
        ctx = HighlightContext(boundaries=(1, 3))
        result = render_array([10, 20, 30, 40, 50], highlights=ctx)

        # Should have [ at left boundary and ] at right boundary
        assert "[" in result
        assert "]" in result

    def test_full_range_boundaries(self):
        """Full array boundaries (0 to last)."""
        ctx = HighlightContext(boundaries=(0, 2))
        result = render_array([10, 20, 30], highlights=ctx)

        # First character should be [ and last should be ]
        lines = result.split("\n")
        top_line = lines[0].strip()
        assert top_line.startswith("[")
        assert top_line.endswith("]")


class TestArrayWithMultipleHighlights:
    """Tests for combining multiple highlight types."""

    def test_current_and_visited(self):
        """Shows both current and visited markers."""
        ctx = HighlightContext(
            current=frozenset({2}),
            visited=frozenset({0, 1}),
        )
        result = render_array([10, 20, 30], highlights=ctx)

        assert f"{MARKER_CURRENT}2" in result
        assert f"{MARKER_VISITED}0" in result
        assert f"{MARKER_VISITED}1" in result

    def test_found_with_visited(self):
        """Shows found and visited markers together."""
        ctx = HighlightContext(
            found=frozenset({2}),
            visited=frozenset({0, 1, 2}),
        )
        result = render_array([10, 20, 30], highlights=ctx)

        # Found takes priority over visited for index 2
        assert f"{MARKER_FOUND}2" in result
        assert f"{MARKER_VISITED}0" in result
        assert f"{MARKER_VISITED}1" in result

    def test_boundaries_with_current(self):
        """Shows boundaries and current marker together."""
        ctx = HighlightContext(
            current=frozenset({2}),
            boundaries=(1, 4),
        )
        result = render_array([10, 20, 30, 40, 50], highlights=ctx)

        assert f"{MARKER_CURRENT}2" in result
        assert "[" in result
        assert "]" in result


class TestArrayHighlightCellWidth:
    """Tests that cell width adjusts for markers."""

    def test_marker_included_in_width_calculation(self):
        """Cell width accounts for marker character."""
        ctx = HighlightContext(current=frozenset({0}))
        result = render_array([1], highlights=ctx)

        # Should have proper alignment with marker
        lines = result.split("\n")
        # All lines should have consistent width (proper table structure)
        assert "│" in lines[1]  # Index row
        assert "│" in lines[3]  # Value row
