"""Jump Search algorithm visualization.

Jump Search: O(√n) time complexity
- Requires sorted array
- Jumps ahead by √n blocks, then does linear search within block
- Better than linear search, simpler than binary search
- Good for systems where jumping back is costly
"""

from __future__ import annotations

import math
from collections.abc import Iterator

from dsa_visualizer.algorithms.types import AlgorithmStep, HighlightContext


def jump_search(arr: list, target: object) -> Iterator[AlgorithmStep]:
    """Generate steps for jump search visualization.

    Searches for target in a sorted array by jumping ahead by √n steps,
    then performing linear search within the identified block.

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

    # Calculate optimal jump size
    jump_size = int(math.sqrt(n))
    step_num = 0
    visited: set[int] = set()

    step_num += 1
    yield AlgorithmStep(
        step_number=step_num,
        action=f"Array size: {n}, jump size: √{n} = {jump_size}",
        highlights=HighlightContext(),
        data=list(arr),
    )

    # Find the block where element may be present
    prev = 0
    curr = 0

    # Jump phase: find the block containing target
    while curr < n and arr[curr] < target:
        step_num += 1
        visited.add(curr)

        yield AlgorithmStep(
            step_number=step_num,
            action=f"Jump to index {curr}: arr[{curr}]={arr[curr]!r} < {target!r}",
            highlights=HighlightContext(
                current=frozenset({curr}),
                visited=frozenset(visited),
                boundaries=(prev, min(curr + jump_size - 1, n - 1)),
            ),
            data=list(arr),
        )

        prev = curr
        curr = min(curr + jump_size, n)

    # Determine block boundaries for linear search
    # If we never jumped (target <= arr[0]), search from 0 to jump_size
    if prev == curr:
        block_start = 0
        block_end = min(jump_size, n) - 1
    else:
        block_start = prev
        block_end = min(curr, n) - 1

    step_num += 1
    yield AlgorithmStep(
        step_number=step_num,
        action=f"Target may be in block [{block_start}..{block_end}], linear search",
        highlights=HighlightContext(
            visited=frozenset(visited),
            boundaries=(block_start, block_end),
        ),
        data=list(arr),
    )

    # Linear search within the block
    for i in range(block_start, block_end + 1):
        step_num += 1
        visited.add(i)

        yield AlgorithmStep(
            step_number=step_num,
            action=f"Check index {i}: arr[{i}]={arr[i]!r}",
            highlights=HighlightContext(
                current=frozenset({i}),
                comparing=frozenset({i}),
                visited=frozenset(visited),
                boundaries=(block_start, block_end),
            ),
            data=list(arr),
        )

        if arr[i] == target:
            step_num += 1
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

        if arr[i] > target:
            # Passed the target, not found
            break

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
