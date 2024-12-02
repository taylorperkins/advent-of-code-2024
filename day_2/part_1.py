from typing import Callable, List

from utils import time_it, read_input, input_path


def ascending(a: int, b: int) -> bool: return b > a
def descending(a: int, b: int) -> bool: return a > b
def differ(l: int, r: int) -> bool: return 1 <= abs(l - r) <= 3


def check(level: List[int]) -> bool:
    """Checks whether a level is 'safe' (true) or 'unsafe' (false)"""
    direction = ascending if level[0] < level[1] else descending

    for i in range(len(level) - 1):
        l, r = level[i], level[i+1]
        if not (direction(l, r) and differ(l, r)):
            return False
    return True


@time_it
def main(data: str) -> int:
    safe = 0
    for line in data.splitlines():
        level = [int(v) for v in line.split(" ")]
        safe += check(level)

    return safe


if __name__ == "__main__":
    print(main(read_input(input_path(__file__).replace(".txt", "_practice.txt"))))
    print(main(read_input(input_path(__file__))))
