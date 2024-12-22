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


@time_it
def main(data: str) -> int:
    secret_numbers = [int(line) for line in data.splitlines()]

    total = 0
    for sn in secret_numbers:
        gen = get_secret_numbers(sn)
        new_sn = 0
        for _ in range(2000):
            new_sn = next(gen)
        total += new_sn
        print(f"{sn}: {new_sn}")

    return total


if __name__ == "__main__":
    print(main(read_input(input_path(__file__).replace(".txt", "_practice.txt"))))
    print(main(read_input(input_path(__file__))))
