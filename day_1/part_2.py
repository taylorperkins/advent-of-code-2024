from collections import Counter
import re

from utils import time_it, read_input, input_path


pattern = re.compile(r'^(?P<n1>\d+)\s+(?P<n2>\d+)?$')


@time_it
def main(data: str) -> str:

    # Each line in the input is like: `123   456`
    # Treat it like a matrix having two columns (vectors), v1 and v2
    v1, v2 = [], []
    for line in data.splitlines():
        m = pattern.match(line)
        if not m:
            raise Exception("Bad Pattern, ", line)

        n1, n2 = m.group("n1"), m.group("n2")
        v1.append(int(n1)), v2.append(int(n2))

    # Instantiate a counter for v2
    # Accumulate the v1*times it appears in v2
    # take advantage of Counter defaulting to zero
    c = Counter(v2)
    distance = 0
    for k in v1:
        distance += (k * c[k])

    return distance


if __name__ == "__main__":
    print(main(read_input(input_path(__file__).replace(".txt", "_practice.txt"))))
    print(main(read_input(input_path(__file__))))
