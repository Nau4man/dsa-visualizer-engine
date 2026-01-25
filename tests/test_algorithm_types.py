"""Tests for algorithm type definitions."""

import pytest
from dataclasses import FrozenInstanceError

from dsa_visualizer.algorithms.types import (
    HighlightContext,
    TreeHighlightContext,
    AlgorithmStep,
)


class TestHighlightContext:
    """Tests for HighlightContext dataclass."""

    def test_create_with_defaults(self):
        """HighlightContext can be created with all defaults."""
        ctx = HighlightContext()
        assert ctx.current == frozenset()
        assert ctx.comparing == frozenset()
        assert ctx.visited == frozenset()
        assert ctx.found == frozenset()
        assert ctx.eliminated == frozenset()
        assert ctx.boundaries is None

    def test_create_with_values(self):
        """HighlightContext can be created with specific values."""
        ctx = HighlightContext(
            current=frozenset({0}),
            comparing=frozenset({1, 2}),
            visited=frozenset({3, 4, 5}),
            found=frozenset({6}),
            eliminated=frozenset({7, 8}),
            boundaries=(0, 10),
        )
        assert ctx.current == frozenset({0})
        assert ctx.comparing == frozenset({1, 2})
        assert ctx.visited == frozenset({3, 4, 5})
        assert ctx.found == frozenset({6})
        assert ctx.eliminated == frozenset({7, 8})
        assert ctx.boundaries == (0, 10)

    def test_is_frozen(self):
        """HighlightContext is immutable."""
        ctx = HighlightContext()
        with pytest.raises(FrozenInstanceError):
            ctx.current = frozenset({1})


class TestTreeHighlightContext:
    """Tests for TreeHighlightContext dataclass."""

    def test_create_with_defaults(self):
        """TreeHighlightContext can be created with all defaults."""
        ctx = TreeHighlightContext()
        assert ctx.current_node is None
        assert ctx.visited_nodes == frozenset()
        assert ctx.found_node is None
        assert ctx.path_nodes == ()
        assert ctx.comparing_node is None

    def test_create_with_values(self):
        """TreeHighlightContext can be created with specific values."""
        ctx = TreeHighlightContext(
            current_node=123,
            visited_nodes=frozenset({456, 789}),
            found_node=123,
            path_nodes=(100, 200, 300),
            comparing_node=123,
        )
        assert ctx.current_node == 123
        assert ctx.visited_nodes == frozenset({456, 789})
        assert ctx.found_node == 123
        assert ctx.path_nodes == (100, 200, 300)
        assert ctx.comparing_node == 123

    def test_is_frozen(self):
        """TreeHighlightContext is immutable."""
        ctx = TreeHighlightContext()
        with pytest.raises(FrozenInstanceError):
            ctx.current_node = 123


class TestAlgorithmStep:
    """Tests for AlgorithmStep dataclass."""

    def test_create_with_required_fields(self):
        """AlgorithmStep can be created with required fields."""
        ctx = HighlightContext(current=frozenset({0}))
        step = AlgorithmStep(
            step_number=1,
            action="Examine index 0",
            highlights=ctx,
            data=[1, 2, 3],
        )
        assert step.step_number == 1
        assert step.action == "Examine index 0"
        assert step.highlights == ctx
        assert step.data == [1, 2, 3]
        assert step.is_complete is False
        assert step.result is None

    def test_create_complete_step(self):
        """AlgorithmStep can represent a completed algorithm."""
        ctx = HighlightContext(found=frozenset({2}))
        step = AlgorithmStep(
            step_number=5,
            action="Found target at index 2",
            highlights=ctx,
            data=[1, 2, 3, 4, 5],
            is_complete=True,
            result=2,
        )
        assert step.is_complete is True
        assert step.result == 2

    def test_is_frozen(self):
        """AlgorithmStep is immutable."""
        ctx = HighlightContext()
        step = AlgorithmStep(
            step_number=1,
            action="Test",
            highlights=ctx,
            data=[],
        )
        with pytest.raises(FrozenInstanceError):
            step.step_number = 2

    def test_data_can_be_any_object(self):
        """AlgorithmStep data field accepts any object type."""
        ctx = HighlightContext()

        # List
        step1 = AlgorithmStep(step_number=1, action="Test", highlights=ctx, data=[1, 2])
        assert step1.data == [1, 2]

        # Dict
        step2 = AlgorithmStep(
            step_number=1, action="Test", highlights=ctx, data={"a": 1}
        )
        assert step2.data == {"a": 1}

        # Custom object
        class Node:
            pass

        node = Node()
        step3 = AlgorithmStep(step_number=1, action="Test", highlights=ctx, data=node)
        assert step3.data is node
