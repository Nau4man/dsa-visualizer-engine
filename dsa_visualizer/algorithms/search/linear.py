"""Linear Search algorithm visualization.

Linear Search: O(n) time complexity
- Simplest search algorithm
- Checks each element sequentially
- Works on unsorted arrays
- Best for small datasets or unsorted data
"""

from __future__ import annotations

from collections.abc import Iterator

from dsa_visualizer.algorithms.types import AlgorithmStep, HighlightContext


def linear_search(arr: list, target: object) -> Iterator[AlgorithmStep]:
    """Generate steps for linear search visualization.

    Searches for target in arr by checking each element sequentially.
    Yields a step for each element examined.

    Args:
        arr: The array to search in.
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

    visited: set[int] = set()
    step_num = 0

    for i, value in enumerate(arr):
        step_num += 1

        # Step: Examine current element
        yield AlgorithmStep(
            step_number=step_num,
            action=f"Examine index {i}: arr[{i}] = {value!r}",
            highlights=HighlightContext(
                current=frozenset({i}),
                visited=frozenset(visited),
            ),
            data=list(arr),
        )

        step_num += 1

        # Step: Compare with target
        if value == target:
            # Found!
            visited.add(i)
            yield AlgorithmStep(
                step_number=step_num,
                action=f"Found {target!r} at index {i}!",
                highlights=HighlightContext(
                    found=frozenset({i}),
                    visited=frozenset(visited),
                ),
                data=list(arr),
                is_complete=True,
                result=i,
            )
            return
        else:
            # Not a match, continue
            visited.add(i)
            yield AlgorithmStep(
                step_number=step_num,
                action=f"Compare: {value!r} != {target!r}, continue",
                highlights=HighlightContext(
                    current=frozenset({i}),
                    comparing=frozenset({i}),
                    visited=frozenset(visited),
                ),
                data=list(arr),
            )

    # Not found after checking all elements
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
