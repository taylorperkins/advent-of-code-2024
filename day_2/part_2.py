from typing import Callable, List

from utils import time_it, read_input, input_path


def ascending(a: int, b: int) -> bool: return a < b
def descending(a: int, b: int) -> bool: return a > b
def differ(l: int, r: int) -> bool: return 1 <= abs(l - r) <= 3


def check(level: List[int], tolerance: bool = True) -> bool:
    """Checks whether a level is 'safe' (true) or 'unsafe' (false)"""
    direction = level[0] < level[1]

    for i in range(len(level) - 1):
        l, r = level[i], level[i + 1]

        same_direction = (l < r) == direction
        valid_distance = differ(l, r)

        if not (same_direction and valid_distance):
            if not tolerance:
                return False

            return check(level[:i] + [l] + level[i+2:], False) or check(level[:i] + [r] + level[i+2:], False)

    return True


@time_it
def main(data: str) -> int:
    safe = 0
    for line in data.splitlines():
        level = [int(v) for v in line.split(" ")]
        # 339 too low
        is_safe = check(level)
        if not is_safe:
            print(level)

        safe += is_safe

    return safe


if __name__ == "__main__":
    # print(main(read_input(input_path(__file__).replace(".txt", "_practice.txt"))))
    # print(main(read_input(input_path(__file__).replace(".txt", "_practice_unsafe.txt"))))
    # print(main(read_input(input_path(__file__).replace(".txt", "_practice_safe.txt"))))
    print(main(read_input(input_path(__file__).replace(".txt", "_practice_safe_v2.txt"))))
    # print(main(read_input(input_path(__file__))))
