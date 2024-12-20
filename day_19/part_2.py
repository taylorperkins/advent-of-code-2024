import re
from collections import defaultdict
from functools import reduce

from typing import Generator, Tuple

from utils import time_it, read_input, input_path


def match(patterns: Generator[Tuple[str, int], None, None], desired_pattern: str) -> int:

    index_starts = defaultdict(lambda : defaultdict(int))
    for p, size in patterns:
        for m in re.finditer(r'(?=(' + p + '))', desired_pattern):
            index_starts[m.start()][size] += 1

    if not index_starts[0]:
        return 0

    # start at the beginning
    idx = 0

    # keep track of stopping points to pick up on other patterns
    multipliers = defaultdict(int)
    multipliers[idx] = 1

    # indices to check along the way
    stops = {idx}
    desired_pattern_size = len(desired_pattern)

    while idx < desired_pattern_size:
        if idx in stops:
            stops.remove(idx)
            multiplier = multipliers[idx]

            for size, n in index_starts[idx].items():
                _next = idx + size
                multipliers[_next] += (multiplier*n)
                stops.add(_next)

        idx += 1

    return multipliers[len(desired_pattern)]


@time_it
def main(data: str) -> int:
    raw_patterns, raw_desired = data.split("\n\n")

    patterns = {p: len(p) for p in raw_patterns.split(", ")}
    desired_patterns = raw_desired.splitlines()

    return reduce(
        lambda acc, p: acc + match(
            ((k, v) for k, v in patterns.items() if k in p),
            p
        ),
        desired_patterns,
        0
    )


if __name__ == "__main__":
    print(main(read_input(input_path(__file__).replace(".txt", "_practice.txt"))))
    print(main(read_input(input_path(__file__))))
