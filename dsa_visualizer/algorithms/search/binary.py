"""Binary Search algorithm visualization.

Binary Search: O(log n) time complexity
- Requires sorted array
- Divides search space in half each iteration
- Much faster than linear search for large datasets
- Classic divide-and-conquer algorithm
"""

from __future__ import annotations

from collections.abc import Iterator

from dsa_visualizer.algorithms.types import AlgorithmStep, HighlightContext


def binary_search(arr: list, target: object) -> Iterator[AlgorithmStep]:
    """Generate steps for binary search visualization.

    Searches for target in a sorted array using binary search.
    Shows boundaries and mid-point calculations at each step.

    Args:
        arr: A sorted array to search in.
        target: The value to find.

    Yields:
        AlgorithmStep for each operation in the search.
    """
    if not arr:
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
    high = len(arr) - 1
    step_num = 0
    visited: set[int] = set()

    while low <= high:
        mid = (low + high) // 2
        step_num += 1

        # Step: Show current search range
        yield AlgorithmStep(
            step_number=step_num,
            action=f"Search range: [{low}..{high}], mid = {mid}",
            highlights=HighlightContext(
                current=frozenset({mid}),
                visited=frozenset(visited),
                boundaries=(low, high),
            ),
            data=list(arr),
        )

        step_num += 1
        mid_value = arr[mid]

        # Step: Compare mid with target
        if mid_value == target:
            visited.add(mid)
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
            # Target is in right half
            visited.add(mid)
            eliminated = frozenset(range(low, mid + 1))
            yield AlgorithmStep(
                step_number=step_num,
                action=f"arr[{mid}]={mid_value!r} < {target!r}, search right half",
                highlights=HighlightContext(
                    current=frozenset({mid}),
                    comparing=frozenset({mid}),
                    visited=frozenset(visited),
                    eliminated=eliminated,
                    boundaries=(low, high),
                ),
                data=list(arr),
            )
            low = mid + 1

        else:
            # Target is in left half
            visited.add(mid)
            eliminated = frozenset(range(mid, high + 1))
            yield AlgorithmStep(
                step_number=step_num,
                action=f"arr[{mid}]={mid_value!r} > {target!r}, search left half",
                highlights=HighlightContext(
                    current=frozenset({mid}),
                    comparing=frozenset({mid}),
                    visited=frozenset(visited),
                    eliminated=eliminated,
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
