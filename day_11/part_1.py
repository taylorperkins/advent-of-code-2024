from typing import Generator

from utils import time_it, read_input, input_path


def blink(stone: str, n: int) -> Generator[int, None, None]:
    if n == 0:
        yield stone

    elif stone == "0":
        yield from blink("1", n-1)

    else:
        size = len(stone)
        if size % 2 == 0:
            mid = size // 2
            left, right = int(stone[:mid]), int(stone[mid:])
            yield from blink(str(left),   n-1)
            yield from blink(str(right),  n-1)

        else:
            yield from blink(str(int(stone)*2024), n-1)


@time_it
def main(data: str) -> int:
    total = 0

    for stone in data.split(" "):
        for _ in blink(stone, 25):
            total += 1

    return total


if __name__ == "__main__":
    print(main(read_input(input_path(__file__).replace(".txt", "_practice.txt"))))
    print(main(read_input(input_path(__file__))))
