"""Exponential Search algorithm visualization.

Exponential Search: O(log n) time complexity
- Requires sorted array
- Useful for unbounded/infinite arrays
- First finds a range by exponentially increasing bound
- Then performs binary search within that range
- Particularly efficient when target is near the beginning
"""

from __future__ import annotations

from collections.abc import Iterator

from dsa_visualizer.algorithms.types import AlgorithmStep, HighlightContext


def exponential_search(arr: list, target: object) -> Iterator[AlgorithmStep]:
    """Generate steps for exponential search visualization.

    Searches for target by exponentially increasing the range until
    a bound is found, then performs binary search within that range.

    Args:
        arr: A sorted array to search in.
        target: The value to find.

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

    step_num = 0
    visited: set[int] = set()

    # Check first element
    step_num += 1
    visited.add(0)
    yield AlgorithmStep(
        step_number=step_num,
        action=f"Check index 0: arr[0]={arr[0]!r}",
        highlights=HighlightContext(
            current=frozenset({0}),
            visited=frozenset(visited),
        ),
        data=list(arr),
    )

    if arr[0] == target:
        step_num += 1
        yield AlgorithmStep(
            step_number=step_num,
            action=f"Found {target!r} at index 0!",
            highlights=HighlightContext(
                found=frozenset({0}),
                visited=frozenset(visited),
            ),
            data=list(arr),
            is_complete=True,
            result=0,
        )
        return

    # Find range by exponential jumping
    bound = 1
    step_num += 1
    yield AlgorithmStep(
        step_number=step_num,
        action="Starting exponential range expansion",
        highlights=HighlightContext(
            visited=frozenset(visited),
        ),
        data=list(arr),
    )

    while bound < n and arr[bound] < target:
        step_num += 1
        visited.add(bound)

        yield AlgorithmStep(
            step_number=step_num,
            action=f"Expand: bound={bound}, arr[{bound}]={arr[bound]!r} < {target!r}",
            highlights=HighlightContext(
                current=frozenset({bound}),
                visited=frozenset(visited),
                boundaries=(bound // 2, min(bound, n - 1)),
            ),
            data=list(arr),
        )

        bound *= 2

    # Binary search in range [bound/2, min(bound, n-1)]
    low = bound // 2
    high = min(bound, n - 1)

    step_num += 1
    yield AlgorithmStep(
        step_number=step_num,
        action=f"Binary search in range [{low}..{high}]",
        highlights=HighlightContext(
            visited=frozenset(visited),
            boundaries=(low, high),
        ),
        data=list(arr),
    )

    # Binary search phase
    while low <= high:
        mid = (low + high) // 2
        step_num += 1
        visited.add(mid)

        yield AlgorithmStep(
            step_number=step_num,
            action=f"Binary: range [{low}..{high}], mid={mid}",
            highlights=HighlightContext(
                current=frozenset({mid}),
                visited=frozenset(visited),
                boundaries=(low, high),
            ),
            data=list(arr),
        )

        step_num += 1
        mid_value = arr[mid]

        if mid_value == target:
            yield AlgorithmStep(
                step_number=step_num,
                action=f"Found {target!r} at index {mid}!",
                highlights=HighlightContext(
                    found=frozenset({mid}),
                    visited=frozenset(visited),
                    boundaries=(low, high),
                ),
                data=list(arr),
                is_complete=True,
                result=mid,
            )
            return

        elif mid_value < target:
            yield AlgorithmStep(
                step_number=step_num,
                action=f"arr[{mid}]={mid_value!r} < {target!r}, search right",
                highlights=HighlightContext(
                    current=frozenset({mid}),
                    comparing=frozenset({mid}),
                    visited=frozenset(visited),
                    boundaries=(low, high),
                ),
                data=list(arr),
            )
            low = mid + 1

        else:
            yield AlgorithmStep(
                step_number=step_num,
                action=f"arr[{mid}]={mid_value!r} > {target!r}, search left",
                highlights=HighlightContext(
                    current=frozenset({mid}),
                    comparing=frozenset({mid}),
                    visited=frozenset(visited),
                    boundaries=(low, high),
                ),
                data=list(arr),
            )
            high = mid - 1

    # Not found
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
