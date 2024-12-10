from __future__ import annotations

from dataclasses import dataclass
from typing import List, Generator

from utils import time_it, read_input, input_path


class TopoMap:
    def __init__(self, data: List[List[int]]):
        self.shape = len(data[0]), len(data)
        self.data = data

    def contains(self, coord: Coord):
        return 0 <= coord.x < self.shape[0] and 0 <= coord.y < self.shape[1]

    def __getitem__(self, coord: Coord):
        if not self.contains(coord):
            raise IndexError()
        return self.data[coord.y][coord.x]

    def __iter__(self):
        # reading order
        for y in range(self.shape[1]):
            for x in range(self.shape[0]):
                c = Coord(x, y)
                yield c, self[c]

    def trailheads(self):
        for (c, v) in self:
            if v == 0:
                yield c


@dataclass
class Coord:
    x: int
    y: int

    def __hash__(self):
        return hash((self.x, self.y))

    def move(self, direction: Coord):
        return Coord(
            x=self.x + direction.x,
            y=self.y + direction.y,
        )


directions = (
    Coord(0, -1),
    Coord(1, 0),
    Coord(0, 1),
    Coord(-1, 0),
)


def count_optimal_trails(tmap: TopoMap, position: Coord) -> Generator[Coord]:
    # raise if not found, always expecting a result
    v = tmap[position]

    if v == 9:
        yield position

    else:
        for d in directions:
            _next = position.move(d)
            try:
                nv = tmap[_next]
            except IndexError:
                pass
            else:
                if nv == (v + 1):
                    yield from count_optimal_trails(tmap, _next)


@time_it
def main(data: str) -> int:
    tmap = TopoMap([list(map(int, row)) for row in data.splitlines()])

    total = 0
    for thead in tmap.trailheads():
        result = set(count_optimal_trails(tmap, thead))
        total += len(result)

    return total


if __name__ == "__main__":
    print(main(read_input(input_path(__file__).replace(".txt", "_practice.txt"))))
    print(main(read_input(input_path(__file__))))
