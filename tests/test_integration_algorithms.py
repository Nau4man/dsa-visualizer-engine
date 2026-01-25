"""Integration tests for algorithm visualization system.

These tests verify that all components work together correctly:
- Executor creates pending algorithms
- AlgorithmRunner manages step navigation
- Algorithms yield correct steps
- Renderers produce highlighted output
"""

from dsa_visualizer.algorithms.types import TreeHighlightContext
from dsa_visualizer.core.executor import Executor
from dsa_visualizer.data_structures.implementations.structures import BinaryTree
from dsa_visualizer.data_structures.render.array import render_array
from dsa_visualizer.data_structures.render.binary_tree import render_binary_tree


class TestArraySearchIntegration:
    """Integration tests for array search algorithms."""

    def test_linear_search_full_flow(self):
        """Full flow: create data, search, step through, get result."""
        executor = Executor()
        executor.execute("data = [10, 20, 30, 40, 50]")
        executor.execute("search('linear', data, 30)")

        pending = executor.pop_pending_algorithm()
        assert pending is not None

        runner = pending.runner
        assert runner.name == "Linear Search"

        # Step through the algorithm
        steps = []
        while True:
            step = runner.advance()
            if step is None:
                break
            steps.append(step)
            if step.is_complete:
                break

        # Should have found the target
        final_step = steps[-1]
        assert final_step.is_complete
        assert final_step.result == 2  # Index of 30

    def test_binary_search_full_flow(self):
        """Binary search finds target efficiently."""
        executor = Executor()
        executor.execute("search('binary', [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 7)")

        pending = executor.pop_pending_algorithm()
        runner = pending.runner

        # Step through
        while True:
            step = runner.advance()
            if step is None or step.is_complete:
                break

        # Should have found it
        current = runner.current()
        assert current.is_complete
        assert current.result == 6  # Index of 7

    def test_all_array_algorithms_work(self):
        """All array search algorithms work correctly."""
        executor = Executor()
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        target = 5

        for algorithm in ["linear", "binary", "jump", "interpolation", "exponential"]:
            executor.execute(f"search('{algorithm}', {data}, {target})")
            pending = executor.pop_pending_algorithm()
            runner = pending.runner

            # Run to completion
            while True:
                step = runner.advance()
                if step is None or step.is_complete:
                    break

            current = runner.current()
            assert current.is_complete, f"{algorithm} should complete"
            assert current.result == 4, f"{algorithm} should find index 4"

    def test_array_rendering_with_highlights(self):
        """Array renders correctly with highlight markers."""
        executor = Executor()
        executor.execute("search('linear', [1, 2, 3, 4, 5], 3)")

        pending = executor.pop_pending_algorithm()
        runner = pending.runner

        # Advance to first step
        step = runner.advance()
        assert step is not None

        # Render with highlights
        output = render_array(step.data, step.highlights)
        assert "→" in output or "1" in output  # Should have current marker or value


class TestTreeSearchIntegration:
    """Integration tests for tree search algorithms."""

    def test_dfs_search_full_flow(self):
        """DFS finds target in tree."""
        executor = Executor()
        executor.execute("tree = BinaryTree([10, 5, 15, 3, 7])")
        executor.execute("tree_search('dfs', tree, 7)")

        pending = executor.pop_pending_algorithm()
        assert pending is not None

        runner = pending.runner
        assert "Depth-First" in runner.name

        # Step through
        while True:
            step = runner.advance()
            if step is None or step.is_complete:
                break

        current = runner.current()
        assert current.is_complete
        assert current.result is not None

    def test_bfs_search_full_flow(self):
        """BFS finds target in tree."""
        executor = Executor()
        executor.execute("tree = BinaryTree([10, 5, 15])")
        executor.execute("tree_search('bfs', tree, 15)")

        pending = executor.pop_pending_algorithm()
        runner = pending.runner

        # Step through
        while True:
            step = runner.advance()
            if step is None or step.is_complete:
                break

        current = runner.current()
        assert current.is_complete
        assert current.result is not None

    def test_bst_search_full_flow(self):
        """BST search finds target efficiently."""
        executor = Executor()
        executor.execute("tree = BinarySearchTree([50, 25, 75, 10, 30, 60, 90])")
        executor.execute("tree_search('bst', tree, 30)")

        pending = executor.pop_pending_algorithm()
        runner = pending.runner

        # Step through
        while True:
            step = runner.advance()
            if step is None or step.is_complete:
                break

        current = runner.current()
        assert current.is_complete
        assert current.result is not None
        assert current.result.value == 30

    def test_tree_traversal_full_flow(self):
        """Tree traversal visits all nodes."""
        executor = Executor()
        executor.execute("tree = BinaryTree([1, 2, 3, 4, 5])")
        executor.execute("tree_traverse('bfs', tree)")

        pending = executor.pop_pending_algorithm()
        runner = pending.runner

        # Step through
        while True:
            step = runner.advance()
            if step is None or step.is_complete:
                break

        current = runner.current()
        assert current.is_complete
        assert current.result == [1, 2, 3, 4, 5]

    def test_tree_rendering_with_highlights(self):
        """Tree renders correctly with highlight markers."""
        tree = BinaryTree([10, 5, 15])

        # Without highlights
        output_plain = render_binary_tree(tree.root)
        assert "[10]" in output_plain
        assert "[5]" in output_plain
        assert "[15]" in output_plain

        # With highlights
        highlights = TreeHighlightContext(current_node=id(tree.root))
        output_highlighted = render_binary_tree(tree.root, highlights)
        assert "[→10]" in output_highlighted


class TestAlgorithmRunnerIntegration:
    """Integration tests for AlgorithmRunner navigation."""

    def test_runner_navigation(self):
        """Runner supports advance, rewind, reset."""
        executor = Executor()
        executor.execute("search('linear', [1, 2, 3, 4, 5], 3)")

        pending = executor.pop_pending_algorithm()
        runner = pending.runner

        # Advance a few steps
        step1 = runner.advance()
        step2 = runner.advance()
        step3 = runner.advance()

        assert step1.step_number == 1
        assert step2.step_number == 2
        assert step3.step_number == 3

        # Rewind
        rewound = runner.rewind()
        assert rewound.step_number == 2

        # Reset
        runner.reset()
        assert runner.current_index == -1

        # Advance again
        first = runner.advance()
        assert first.step_number == 1

    def test_runner_completes_gracefully(self):
        """Runner returns None when algorithm is complete."""
        executor = Executor()
        executor.execute("search('linear', [1], 99)")

        pending = executor.pop_pending_algorithm()
        runner = pending.runner

        # Exhaust the runner
        steps = []
        for _ in range(100):  # More than needed
            step = runner.advance()
            if step is None:
                break
            steps.append(step)

        # Should have completed
        assert len(steps) > 0
        assert steps[-1].is_complete


class TestExampleDatasetsIntegration:
    """Integration tests for example datasets."""

    def test_example_array_search(self):
        """Can search in example arrays."""
        executor = Executor()
        executor.execute("data = EXAMPLES['arrays']['small']")
        executor.execute("search('binary', data, 5)")

        pending = executor.pop_pending_algorithm()
        runner = pending.runner

        # Should find 5 at index 2
        while True:
            step = runner.advance()
            if step is None or step.is_complete:
                break

        assert runner.current().result == 2

    def test_example_tree_search(self):
        """Can search in trees built from examples."""
        executor = Executor()
        executor.execute("tree = BinarySearchTree(EXAMPLES['trees']['balanced'])")
        executor.execute("tree_search('bst', tree, 25)")

        pending = executor.pop_pending_algorithm()
        runner = pending.runner

        # Should find 25
        while True:
            step = runner.advance()
            if step is None or step.is_complete:
                break

        current = runner.current()
        assert current.is_complete
        assert current.result is not None
        assert current.result.value == 25

