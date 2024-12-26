from collections import Counter
from typing import List, Tuple, Dict

from utils import time_it, read_input, input_path


Matrix = List[List[str]]
FivePinSchematic = Tuple[int, int, int, int, int]


@time_it
def main(data: str) -> str:
    locks: Dict[FivePinSchematic, Counter] = {}
    keys: Dict[FivePinSchematic, Counter] = {}

    for raw_schematic in data.split("\n\n"):
        schematic = raw_schematic.splitlines()
        width = len(schematic[0])

        _id = tuple(
            "".join(line[i] for line in schematic).count("#") - 1
            for i in range(width)
        )

        c = Counter(
            (x, y)
            for y in range(width)
            for x in range(len(schematic))
            if schematic[x][y] == "#"
        )

        if schematic[0] == ("#"*width):
            locks[_id] = c
        else:
            keys[_id] = c

    n_fit = 0
    for lock_id, lock_c in locks.items():
        for key_id, key_c in keys.items():
            merged = lock_c + key_c
            if max(merged.values()) == 1:
                n_fit += 1

    return n_fit


if __name__ == "__main__":
    print(main(read_input(input_path(__file__).replace(".txt", "_practice.txt"))))
    print(main(read_input(input_path(__file__))))
