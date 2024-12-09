from collections import defaultdict
from itertools import permutations

from utils import time_it, read_input, input_path


@time_it
def main(data: str) -> int:
    data = data.splitlines()
    shape = len(data), len(data[0])

    # holds all coordinates of known antennas,
    # organized by frequencies
    antenna_frequencies = defaultdict(set)

    for y, row in enumerate(data):
        for x, value in enumerate(row):
            if value != ".":
                antenna_frequencies[value].add((x, y))

    # all coordinates for "antinodes"
    antinodes = set()

    for frequency, coords in antenna_frequencies.items():
        # permutations as to recognize inverse pairs
        for (ax, ay), (bx, by) in permutations(coords, 2):
            x = ax + (ax - bx)
            y = ay + (ay - by)

            if 0 <= y < shape[0] and 0 <= x < shape[1]:
                antinodes.add((x, y))

    return len(antinodes)


if __name__ == "__main__":
    print(main(read_input(input_path(__file__).replace(".txt", "_practice.txt"))))
    print(main(read_input(input_path(__file__))))
