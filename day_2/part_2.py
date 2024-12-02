from collections import Counter
from typing import List

from utils import time_it, read_input, input_path


def differ(l: int, r: int) -> bool: return 1 <= abs(l - r) <= 3


def check(record: List[int], tolerance: bool = True) -> bool:
    """Checks whether a record is 'safe' (true) or 'unsafe' (false).
    Ability to apply a single level of "tolerance" to the record, effectively
    removing a "bad level", attempting to determine success after it is removed.

    Iterate through the record, checking adjacent levels.
    If the "distance" between all levels pass and if all directionality is the same,
    then the record is good.

    Otherwise, check if the directionality or distance is the issue.

    1. Determine the "popular direction" of the vector. Find the first "unpopular"
    direction, and attempt to swap both of the tagged levels.
    2. Find the first incorrect distance, and attempt to swap both of the tagged levels.
    """
    directions = []
    distances = []

    for i in range(len(record) - 1):
        l, r = record[i], record[i + 1]
        directions.append(l < r)
        distances.append(differ(l, r))

    valid_directions = len(set(directions)) == 1
    valid_distances = all(distances)

    if valid_directions and valid_distances:
        return True

    if not tolerance:
        return False

    if not valid_directions:
        c = Counter(directions)
        least_popular = not c.most_common(1)[0][0]
        i = directions.index(least_popular)

    # distances must be invalid
    else:
        i = distances.index(False)

    return (
        check(record[:i] + record[i + 1:], False)
        or check(record[:i + 1] + record[i + 2:], False)
    )


@time_it
def main(data: str) -> int:
    safe = 0
    for line in data.splitlines():
        level = [int(v) for v in line.split(" ")]
        safe += check(level)

    return safe


if __name__ == "__main__":
    print(main(read_input(input_path(__file__).replace(".txt", "_practice.txt"))))
    print(main(read_input(input_path(__file__).replace(".txt", "_practice_unsafe.txt"))))
    print(main(read_input(input_path(__file__).replace(".txt", "_practice_safe.txt"))))
    print(main(read_input(input_path(__file__).replace(".txt", "_practice_safe_v2.txt"))))
    print(main(read_input(input_path(__file__))))
