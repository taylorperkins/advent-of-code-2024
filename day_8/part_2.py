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
        if len(coords) > 1:
            antinodes |= coords

            # permutations as to recognize inverse pairs
            for left, right in permutations(coords, 2):

                # determine the direction of right -> left
                x_offset = left[0] - right[0]
                y_offset = left[1] - right[1]

                # keep going in the direction (starting at left) until you
                # run off the map
                coord = left
                while True:
                    x = coord[0] + x_offset
                    y = coord[1] + y_offset

                    if not (0 <= y < shape[0] and 0 <= x < shape[1]):
                        break

                    coord = (x, y)
                    antinodes.add(coord)

    return len(antinodes)


if __name__ == "__main__":
    print(main(read_input(input_path(__file__).replace(".txt", "_practice.txt"))))
    print(main(read_input(input_path(__file__))))
