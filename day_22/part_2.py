from collections import defaultdict
from typing import Generator, Tuple

from utils import time_it, read_input, input_path


PriceWindow = Tuple[int, int, int, int]


def get_secret_numbers(secret_number: int, n: int) -> Generator[int, None, None]:
    process = (
        lambda v: v * 64,
        lambda v: v // 32,
        lambda v: v * 2048,
    )

    yield secret_number

    for _ in range(n):
        for fn in process:
            out = fn(secret_number)
            secret_number = (secret_number ^ out) % 16777216

        yield secret_number


def rolling(prices: Generator[int, None, None]) -> Generator[Tuple[PriceWindow, int], None, None]:
    prices = list(prices)
    deltas = [prices[i] - prices[i-1] for i in range(1, len(prices))]

    seen = set()
    for i in range(4, len(prices)):
        _id = tuple(deltas[i-4:i])
        price = prices[i]
        if _id not in seen:
            seen.add(_id)
            yield _id, price


@time_it
def main(data: str) -> int:

    buyers = (int(line) for line in data.splitlines())

    delta_count = defaultdict(int)

    for i, sn in enumerate(buyers):
        secret_numbers = get_secret_numbers(sn, n=2000)
        prices = (n % 10 for n in secret_numbers)

        for _id, price in rolling(prices):
            delta_count[_id] += price

    return max(delta_count.values())


if __name__ == "__main__":
    print(main(read_input(input_path(__file__).replace(".txt", "_practice.txt"))))
    print(main(read_input(input_path(__file__))))
