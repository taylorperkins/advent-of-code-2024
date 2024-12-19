import re
from collections import defaultdict

from typing import List, Dict, Set

from utils import time_it, read_input, input_path


def match(patterns: Set[str], desired_pattern: str) -> int:
    # start at the beginning
    idx = 0

    # keep track of stopping points to pick up on other patterns
    multipliers = defaultdict(int)
    multipliers[idx] = 1

    # indices to check along the way
    stops = {idx}

    while idx < len(desired_pattern):
        if idx in stops:
            stops.remove(idx)
            multiplier = multipliers[idx]

            for pattern in patterns:
                if desired_pattern[idx:].startswith(pattern):
                    _next = idx + len(pattern)
                    multipliers[_next] += multiplier
                    stops.add(_next)

            if idx == 0 and not stops:
                return 0

        idx += 1

    return multipliers[len(desired_pattern)]


@time_it
def main(data: str) -> int:
    raw_patterns, raw_desired = data.split("\n\n")

    patterns = set(raw_patterns.split(", "))
    desired_patterns = raw_desired.splitlines()

    total = 0
    for d in desired_patterns:
        total += match(
            {p for p in patterns if p in d},
            d
        )

    return total


if __name__ == "__main__":
    print(main(read_input(input_path(__file__).replace(".txt", "_practice.txt"))))
    print(main(read_input(input_path(__file__))))
