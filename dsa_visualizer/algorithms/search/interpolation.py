"""Interpolation Search algorithm visualization.

Interpolation Search: O(log log n) average time complexity
- Requires sorted array with uniformly distributed numeric values
- Estimates position based on value distribution
- Better than binary search for uniform distributions
- Can degrade to O(n) for non-uniform distributions
"""

from __future__ import annotations

from collections.abc import Iterator

from dsa_visualizer.algorithms.types import AlgorithmStep, HighlightContext


def interpolation_search(arr: list, target: object) -> Iterator[AlgorithmStep]:
    """Generate steps for interpolation search visualization.

    Searches for target in a sorted array using interpolation formula
    to estimate the position based on value distribution.

    Args:
        arr: A sorted array of numeric values to search in.
        target: The numeric value to find.

    Yields:
        AlgorithmStep for each operation in the search.
    """
    n = len(arr)

    if n == 0:
        yield AlgorithmStep(
            step_number=1,
            action=f"Array is empty, {target!r} not found",
            highlights=HighlightContext(),
            data=list(arr),
            is_complete=True,
            result=-1,
        )
        return

    low = 0
    high = n - 1
    step_num = 0
    visited: set[int] = set()

    while low <= high and arr[low] <= target <= arr[high]:
        step_num += 1

        # Calculate interpolation position
        if arr[high] == arr[low]:
            pos = low
        else:
            # Interpolation formula: estimate position based on value
            pos = low + int(
                ((target - arr[low]) * (high - low)) / (arr[high] - arr[low])
            )

        # Clamp position to valid range
        pos = max(low, min(pos, high))

        yield AlgorithmStep(
            step_number=step_num,
            action=f"Range [{low}..{high}], interpolated pos = {pos}",
            highlights=HighlightContext(
                current=frozenset({pos}),
                visited=frozenset(visited),
                boundaries=(low, high),
            ),
            data=list(arr),
        )

        step_num += 1
        visited.add(pos)

        if arr[pos] == target:
            yield AlgorithmStep(
                step_number=step_num,
                action=f"Found {target!r} at index {pos}!",
                highlights=HighlightContext(
                    found=frozenset({pos}),
                    visited=frozenset(visited),
                    boundaries=(low, high),
                ),
                data=list(arr),
                is_complete=True,
                result=pos,
            )
            return

        elif arr[pos] < target:
            yield AlgorithmStep(
                step_number=step_num,
                action=f"arr[{pos}]={arr[pos]!r} < {target!r}, search right",
                highlights=HighlightContext(
                    current=frozenset({pos}),
                    comparing=frozenset({pos}),
                    visited=frozenset(visited),
                    boundaries=(low, high),
                ),
                data=list(arr),
            )
            low = pos + 1

        else:
            yield AlgorithmStep(
                step_number=step_num,
                action=f"arr[{pos}]={arr[pos]!r} > {target!r}, search left",
                highlights=HighlightContext(
                    current=frozenset({pos}),
                    comparing=frozenset({pos}),
                    visited=frozenset(visited),
                    boundaries=(low, high),
                ),
                data=list(arr),
            )
            high = pos - 1

    # Not found (target out of range or not present)
    step_num += 1
    yield AlgorithmStep(
        step_number=step_num,
        action=f"{target!r} not found in array",
        highlights=HighlightContext(
            visited=frozenset(visited),
        ),
        data=list(arr),
        is_complete=True,
        result=-1,
    )
