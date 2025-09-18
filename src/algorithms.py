# src/algorithms.py
# Generators that yield (array_state, meta_state) at each step.

from typing import Generator, List, Dict, Any

def _clone(arr: List[int]) -> List[int]:
    return list(arr)

def insertion_sort_states(values: List[int]) -> Generator:
    """Yield (array, state) pairs for insertion sort."""
    a = _clone(values)
    n = len(a)
    # Initial
    yield _clone(a), {"sorted": set(), "info": "start"}

    for i in range(1, n):
        key = a[i]
        j = i - 1
        # Show the key we are inserting
        yield _clone(a), {"sorted": set(range(i)), "active": [i], "info": f"pick key at i={i}"}

        while j >= 0 and a[j] > key:
            # Compare and shift
            a[j + 1] = a[j]
            yield _clone(a), {
                "sorted": set(range(i)),
                "active": [i],
                "compare": [j],
                "info": f"shift {a[j]} right"
            }
            j -= 1

        a[j + 1] = key
        # Key placed
        yield _clone(a), {"sorted": set(range(i + 1)), "active": [j + 1], "info": f"place key at {j + 1}"}

    yield _clone(a), {"sorted": set(range(n)), "info": "done"}

def selection_sort_states(values: List[int]) -> Generator:
    """Yield (array, state) pairs for selection sort."""
    a = _clone(values)
    n = len(a)
    yield _clone(a), {"sorted": set(), "info": "start"}

    for i in range(n):
        min_idx = i
        # Scan the rest to find the minimum
        for j in range(i + 1, n):
            yield _clone(a), {
                "sorted": set(range(i)),
                "min_idx": min_idx,
                "active": [j],
                "info": f"compare j={j} with min_idx={min_idx}"
            }
            if a[j] < a[min_idx]:
                min_idx = j
                yield _clone(a), {
                    "sorted": set(range(i)),
                    "min_idx": min_idx,
                    "active": [j],
                    "info": f"new min at j={j}"
                }

        # Swap min into place
        if min_idx != i:
            a[i], a[min_idx] = a[min_idx], a[i]
            yield _clone(a), {
                "sorted": set(range(i + 1)),
                "swap": (i, min_idx),
                "info": f"swap {i} and {min_idx}"
            }
        else:
            yield _clone(a), {"sorted": set(range(i + 1)), "info": "no swap"}

    yield _clone(a), {"sorted": set(range(n)), "info": "done"}
