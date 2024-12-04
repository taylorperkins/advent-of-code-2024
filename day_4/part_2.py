from __future__ import annotations

from dataclasses import (dataclass)
from typing import List, Callable, Optional
from functools import partial

from utils import time_it, read_input, input_path


def left(c: Coord): return Coord(c.x - 1, c.y)
def right(c: Coord): return Coord(c.x + 1, c.y)
def up(c: Coord): return Coord(c.x, c.y - 1)
def down(c: Coord): return Coord(c.x, c.y + 1)


def move(c: Coord, fns: List[Callable[[Coord], Coord]]):
    if not fns:
        return c

    return move(fns[0](c), fns[1:])


@dataclass
class Coord:
    x: int
    y: int


class Plane:
    def __init__(self, data: List[List[str]]):
        self.data = data
        self.shape = len(data), len(data[0])

    def _exists(self, c: Coord):
        return 0 <= c.y < self.shape[0] and 0 <= c.x < self.shape[1]

    def __getitem__(self, item: Coord) -> Optional[str]:
        if self._exists(item):
            return self.data[item.y][item.x]

    def __iter__(self):
        for y in range(self.shape[0]):
            for x in range(self.shape[1]):
                yield Coord(x, y)

    def take(self, c: Coord, direction: Callable[[Coord], Coord], n: int) -> str:
        """Take n values of the plane in any given direction, starting at c"""
        if n == 1:
            return self[c] or ""
        return (self[c] or "") + self.take(direction(c), direction, n - 1)


diagonals = [
    partial(move, fns=[left, up]),
    partial(move, fns=[right, up]),
    partial(move, fns=[left, down]),
    partial(move, fns=[right, down]),
]


directions = [
    left, right, up, down,
]


def count_occurrences(plane: Plane, coord: Coord) -> int:
    """Check if the coord is a valid X-MAS

    Two diagonal MAS with A in the center
    """
    d1 = [
        plane[move(coord, fns=[left, up])] or "",
        plane[move(coord, fns=[right, down])] or "",
    ]

    d2 = [
        plane[move(coord, fns=[left, down])] or "",
        plane[move(coord, fns=[right, up])] or "",
    ]

    if ["M", "S"] == sorted(d1) == sorted(d2) and plane[coord] == "A":
        return 1
    return 0


@time_it
def main(data: str) -> int:
    plane = Plane([list(line) for line in data.splitlines()])

    count = 0
    for coord in plane:
        if plane[coord] == "A":
            count += count_occurrences(plane, coord)

    return count


if __name__ == "__main__":
    print(main(read_input(input_path(__file__).replace(".txt", "_practice.txt"))))
    print(main(read_input(input_path(__file__))))
