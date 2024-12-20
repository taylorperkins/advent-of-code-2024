from typing import List, Generator

from utils import time_it, read_input, input_path


def match_gen(patterns: List[str], desired: str) -> Generator[bool, None, None]:
    if not desired:
        yield True

    for p in patterns:
        if desired.startswith(p):
            yield from match_gen(patterns, desired[len(p):])


def match(patterns: List[str], desired: str) -> bool:
    g = match_gen(patterns, desired)
    try:
        return next(g)
    except StopIteration:
        return False


@time_it
def main(data: str) -> int:
    raw_patterns, raw_desired = data.split("\n\n")

    patterns = sorted(raw_patterns.split(", "), key=lambda p: -len(p))
    desired_patterns = raw_desired.splitlines()

    total = 0
    for d in desired_patterns:
        possible = match(
            [p for p in patterns if p in d],
             d
        )
        # print(d, possible)
        total += possible


    return total


if __name__ == "__main__":
    print(main(read_input(input_path(__file__).replace(".txt", "_practice.txt"))))
    # 228 too low
    print(main(read_input(input_path(__file__))))
