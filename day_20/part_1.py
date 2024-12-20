from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import List, Optional, Generator, Dict

from utils import time_it, read_input, input_path


@dataclass
class Coord:
    x: int
    y: int

    def __hash__(self):
        return hash((self.x, self.y))

    def move(self, direction: Coord, n: int = 1) -> Coord:
        return Coord(x=self.x + (direction.x*n), y=self.y + (direction.y*n))

    @property
    def pivot(self) -> Coord:
        # always around 0,0
        return Coord(x=-self.y, y=self.x)

    @property
    def pivot_right(self) -> Coord: return self.pivot

    @property
    def pivot_left(self) -> Coord: return self.pivot_right.inverse

    @property
    def inverse(self) -> Coord:
        return Coord(x=-self.x, y=-self.y)

    def distance(self, other: Coord):
        return abs(self.x - other.x) + abs(self.y - other.y)

    def neighbors(self, n: int = 1):
        for d in directions:
            yield self.move(d, n=n)


directions = (
    Coord(0, 1),
    Coord(1, 0),
    Coord(0, -1),
    Coord(-1, 0),
)

class Plane:
    def __init__(self, data: List[List[str]]):
        self.data = data
        self.shape = Coord(len(data[0]), len(data))

    def exists(self, c: Coord):
        return 0 <= c.y < self.shape.y and 0 <= c.x < self.shape.x

    def get(self, item: Coord, default = None) -> Optional[str]:
        if self.exists(item):
            return self.data[item.y][item.x]
        return default

    def __getitem__(self, item: Coord) -> str:
        assert self.exists(item)
        return self.data[item.y][item.x]

    def __iter__(self) -> Generator[(Coord, Optional[str]), None, None]:
        # reading order
        for y in range(self.shape.y):
            for x in range(self.shape.x):
                c = Coord(x, y)
                yield c, self.get(c)


def get_racetrack(plane: Plane) -> Dict[Coord, int]:
    start: Coord = next(c for c, v in plane if v == "S")
    end: Coord = next(c for c, v in plane if v == "E")

    path = {}
    prev = None
    current = start
    i = 0
    while current != end:
        path[current] = i
        for neighbor in current.neighbors():
            if neighbor == end:
                path[neighbor] = i+1
                return path

            if plane.get(neighbor) == "." and neighbor != prev:
                i += 1
                prev = current
                current = neighbor
                break

    return path


@dataclass
class Cheat:
    start: Coord
    end: Coord
    picoseconds: int


def get_cheats(racetrack: Dict[Coord, int]) -> Generator[Cheat, None, None]:
    for start, start_position in racetrack.items():
        for end in start.neighbors(n=2):
            end_position = racetrack.get(end, -1)
            cheat = Cheat(
                start, end,
                # exclude the positions themselves
                end_position-start_position - 2
            )
            if cheat.picoseconds > 0:
                yield cheat


@time_it
def main(data: str) -> int:
    plane = Plane([list(line) for line in data.splitlines()])
    racetrack = get_racetrack(plane)
    cheats = get_cheats(racetrack)
    best_cheats = (c for c in cheats if c.picoseconds >= 100)
    return len(list(best_cheats))


if __name__ == "__main__":
    print(main(read_input(input_path(__file__).replace(".txt", "_practice.txt"))))
    print(main(read_input(input_path(__file__))))
