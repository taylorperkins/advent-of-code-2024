from collections import deque, defaultdict
from typing import Generator, Tuple

from utils import time_it, read_input, input_path


def step_one(v: int) -> int:
    return v * 64

def step_two(v: int) -> int:
    return int(v / 32)

def step_three(v: int) -> int:
    return v * 2048

def mix(secret_number: int, v: int) -> int:
    return secret_number ^ v

def prune(secret_number: int):
    return secret_number % 16777216


def get_secret_numbers(secret_number):
    process = (
        step_one, step_two, step_three
    )

    while True:
        for step in process:
            result = step(secret_number)
            secret_number = mix(secret_number, result)
            secret_number = prune(secret_number)

        yield secret_number


def get_rolling_prices(
    secret_number: int,
    gen: Generator[int, None, None]
) -> Generator[Tuple[Tuple[int, int, int, int], int], None, None]:

    queue = deque(maxlen=4)
    prev_prices = set()

    current_price = int(str(secret_number)[-1])

    for sn in gen:
        next_price = int(str(sn)[-1])

        delta = next_price - current_price
        current_price = next_price

        queue.append(delta)

        if len(queue) == 4:
            _id = tuple(queue)
            if _id not in prev_prices:
                yield _id, current_price
            prev_prices.add(_id)


@time_it
def main(data: str) -> int:
    secret_numbers = [int(line) for line in data.splitlines()]

    best_prices = defaultdict(int)

    for sn in secret_numbers:
        gen = get_secret_numbers(sn)
        rolling_prices = get_rolling_prices(sn, gen)

        for _ in range(2000):
            _id, price = next(rolling_prices)
            best_prices[_id] += price

    return max(best_prices.values())


if __name__ == "__main__":
    print(main(read_input(input_path(__file__).replace(".txt", "_practice.txt"))))
    # 2168 -- too high
    print(main(read_input(input_path(__file__))))
