"""Tests for highlight marker utilities."""

from dsa_visualizer.algorithms.types import HighlightContext
from dsa_visualizer.algorithms.render.highlights import (
    MARKER_CURRENT,
    MARKER_VISITED,
    MARKER_FOUND,
    MARKER_COMPARING,
    MARKER_ELIMINATED,
    get_index_marker,
    is_at_left_boundary,
    is_at_right_boundary,
    is_in_search_range,
)


class TestGetIndexMarker:
    """Tests for get_index_marker function."""

    def test_no_highlight_returns_empty(self):
        """Returns empty string when index has no highlight."""
        ctx = HighlightContext()
        assert get_index_marker(0, ctx) == ""

    def test_current_returns_arrow(self):
        """Returns arrow marker for current index."""
        ctx = HighlightContext(current=frozenset({0}))
        assert get_index_marker(0, ctx) == MARKER_CURRENT
        assert get_index_marker(1, ctx) == ""

    def test_visited_returns_dot(self):
        """Returns dot marker for visited index."""
        ctx = HighlightContext(visited=frozenset({0, 1, 2}))
        assert get_index_marker(0, ctx) == MARKER_VISITED
        assert get_index_marker(1, ctx) == MARKER_VISITED
        assert get_index_marker(3, ctx) == ""

    def test_found_returns_check(self):
        """Returns check marker for found index."""
        ctx = HighlightContext(found=frozenset({2}))
        assert get_index_marker(2, ctx) == MARKER_FOUND

    def test_comparing_returns_question(self):
        """Returns question marker for comparing index."""
        ctx = HighlightContext(comparing=frozenset({1}))
        assert get_index_marker(1, ctx) == MARKER_COMPARING

    def test_eliminated_returns_x(self):
        """Returns x marker for eliminated index."""
        ctx = HighlightContext(eliminated=frozenset({0, 1}))
        assert get_index_marker(0, ctx) == MARKER_ELIMINATED

    def test_found_beats_current(self):
        """Found has higher priority than current."""
        ctx = HighlightContext(
            found=frozenset({0}),
            current=frozenset({0}),
        )
        assert get_index_marker(0, ctx) == MARKER_FOUND

    def test_current_beats_comparing(self):
        """Current has higher priority than comparing."""
        ctx = HighlightContext(
            current=frozenset({0}),
            comparing=frozenset({0}),
        )
        assert get_index_marker(0, ctx) == MARKER_CURRENT

    def test_comparing_beats_visited(self):
        """Comparing has higher priority than visited."""
        ctx = HighlightContext(
            comparing=frozenset({0}),
            visited=frozenset({0}),
        )
        assert get_index_marker(0, ctx) == MARKER_COMPARING

    def test_visited_beats_eliminated(self):
        """Visited has higher priority than eliminated."""
        ctx = HighlightContext(
            visited=frozenset({0}),
            eliminated=frozenset({0}),
        )
        assert get_index_marker(0, ctx) == MARKER_VISITED

    def test_full_priority_chain(self):
        """Tests complete priority: found > current > comparing > visited > eliminated."""
        # All states on same index - found wins
        ctx = HighlightContext(
            found=frozenset({0}),
            current=frozenset({0}),
            comparing=frozenset({0}),
            visited=frozenset({0}),
            eliminated=frozenset({0}),
        )
        assert get_index_marker(0, ctx) == MARKER_FOUND


class TestBoundaryHelpers:
    """Tests for boundary helper functions."""

    def test_is_at_left_boundary_true(self):
        """Returns True when index is at left boundary."""
        ctx = HighlightContext(boundaries=(2, 7))
        assert is_at_left_boundary(2, ctx) is True

    def test_is_at_left_boundary_false(self):
        """Returns False when index is not at left boundary."""
        ctx = HighlightContext(boundaries=(2, 7))
        assert is_at_left_boundary(0, ctx) is False
        assert is_at_left_boundary(7, ctx) is False

    def test_is_at_left_boundary_no_boundaries(self):
        """Returns False when no boundaries set."""
        ctx = HighlightContext()
        assert is_at_left_boundary(0, ctx) is False

    def test_is_at_right_boundary_true(self):
        """Returns True when index is at right boundary."""
        ctx = HighlightContext(boundaries=(2, 7))
        assert is_at_right_boundary(7, ctx) is True

    def test_is_at_right_boundary_false(self):
        """Returns False when index is not at right boundary."""
        ctx = HighlightContext(boundaries=(2, 7))
        assert is_at_right_boundary(2, ctx) is False
        assert is_at_right_boundary(5, ctx) is False

    def test_is_at_right_boundary_no_boundaries(self):
        """Returns False when no boundaries set."""
        ctx = HighlightContext()
        assert is_at_right_boundary(0, ctx) is False

    def test_is_in_search_range_inside(self):
        """Returns True for indices within boundaries."""
        ctx = HighlightContext(boundaries=(2, 7))
        assert is_in_search_range(2, ctx) is True
        assert is_in_search_range(5, ctx) is True
        assert is_in_search_range(7, ctx) is True

    def test_is_in_search_range_outside(self):
        """Returns False for indices outside boundaries."""
        ctx = HighlightContext(boundaries=(2, 7))
        assert is_in_search_range(0, ctx) is False
        assert is_in_search_range(1, ctx) is False
        assert is_in_search_range(8, ctx) is False

    def test_is_in_search_range_no_boundaries(self):
        """Returns True for any index when no boundaries."""
        ctx = HighlightContext()
        assert is_in_search_range(0, ctx) is True
        assert is_in_search_range(100, ctx) is True
