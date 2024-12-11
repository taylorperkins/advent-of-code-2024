from collections import Counter
from typing import Dict

from utils import time_it, read_input, input_path


def blink(stones: Dict[str, int]) -> Dict[str, int]:
    c = Counter()

    for stone, count in stones.items():
        if stone == "0":
            c["1"] += count

        else:
            size = len(stone)
            if size % 2 == 0:
                mid = size // 2
                left, right = int(stone[:mid]), int(stone[mid:])
                c[str(left)] += count
                c[str(right)] += count

            else:
                c[str(int(stone)*2024)] += count

    return c


@time_it
def main(data: str) -> int:
    c = Counter(data.split(" "))
    for _ in range(75):
        c = blink(c)

    return sum(c.values())


if __name__ == "__main__":
    print(main(read_input(input_path(__file__).replace(".txt", "_practice.txt"))))
    print(main(read_input(input_path(__file__))))
