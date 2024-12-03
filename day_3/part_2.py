import re

from utils import time_it, read_input, input_path


pattern = re.compile(r'(mul\(\d+,\d+\)|do\(\)|don\'t\(\))')


@time_it
def main(data: str) -> int:
    """Iterate through all the input data, capturing `mul`
    commands and applying them to the running total.

    Has the ability to "toggle" the dot product process
    as it finds 'do()' or 'don't()' k/w within the input.
    """
    allow = True
    total = 0
    for line in data.splitlines():
        for m in pattern.findall(line):
            match m:
                case "do()":
                    allow = True
                case "don't()":
                    allow = False
                case _:
                    if allow:
                        l, r = m.replace("mul(", "").replace(")", "").split(",")
                        total += int(l) * int(r)

    return total


if __name__ == "__main__":
    print(main(read_input(input_path(__file__).replace(".txt", "_practice.txt"))))
    print(main(read_input(input_path(__file__))))
