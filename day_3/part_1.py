import re

from utils import time_it, read_input, input_path


pattern = re.compile(r'mul\((?P<n1>\d+),(?P<n2>\d+)\)')


@time_it
def main(data: str) -> int:
    total = 0
    for line in data.splitlines():
        total += sum(
            int(m[0]) * int(m[1])
            for m in pattern.findall(line)
        )

    return total


if __name__ == "__main__":
    print(main(read_input(input_path(__file__).replace(".txt", "_practice.txt"))))
    print(main(read_input(input_path(__file__))))
