from __future__ import annotations

from collections import defaultdict
from copy import deepcopy
from dataclasses import (dataclass)
from typing import List, Optional, Set, Dict

from utils import time_it, read_input, input_path


@dataclass
class Coord:
    x: int
    y: int

    def __hash__(self):
        return hash((self.x, self.y))

    def move(self, direction: Coord) -> Coord:
        return Coord(x=self.x + direction.x, y=self.y + direction.y)


class Plane:
    def __init__(self, data: List[List[str]]):
        self.data = data
        self.shape = len(data), len(data[0])

    def _exists(self, c: Coord):
        return 0 <= c.y < self.shape[0] and 0 <= c.x < self.shape[1]

    def __getitem__(self, item: Coord) -> Optional[str]:
        if not self._exists(item):
            raise IndexError()

        return self.data[item.y][item.x]

    def with_obstruction(self, at: Coord) -> Plane:
        copy = deepcopy(self.data)
        copy[at.y][at.x] = "#"
        return Plane(copy)


@dataclass
class SecurityGuard:
    position: Coord
    direction: Coord

    def pivot(self):
        """Turn right, in place :sad-panda:
        This is the inverse of a traditional pivot, since
        increasing y goes down (list-indexing)
        """
        self.direction = Coord(x=-self.direction.y, y=self.direction.x)

    def front(self) -> Coord:
        return self.position.move(self.direction)

    def step(self):
        self.position = self.front()


class InfiniteLoopException(Exception): pass


def emulate(plane: Plane, guard: SecurityGuard) -> List[Coord]:
    visited: Dict[Coord, Set[Coord]] = defaultdict(set)
    visited[guard.position].add(guard.direction)

    while True:
        try:
            value = plane[guard.front()]
        # no longer in the map, you're done
        except IndexError:
            return list(visited.keys())
        else:
            match value:
                case ".":
                    guard.step()
                case "#":
                    guard.pivot()

            if guard.direction in visited[guard.position]:
                raise InfiniteLoopException()

            visited[guard.position].add(guard.direction)


@time_it
def main(data: str) -> int:
    grid = []
    guard: SecurityGuard = ...
    pointer: (Coord, Coord) = ...

    # parsing. Determine the map/layout and the pointer (security guard)
    for y, line in enumerate(data.splitlines()):
        row = []
        for x, value in enumerate(line):
            match value:
                case "." | "#": row.append(value)
                case _:
                    row.append(".")
                    c = Coord(x=x, y=y)
                    match value:
                        case "^": d = Coord(x=0, y=-1)
                        case ">": d = Coord(x=1, y=0)
                        case "v": d = Coord(x=0, y=1)
                        case "<": d = Coord(x=-1, y=0)
                        case _: raise Exception("Bad match")
                    pointer = c, d
        grid.append(row)

    plane = Plane(grid)
    original_positions = emulate(plane, SecurityGuard(position=pointer[0], direction=pointer[1]))

    loops = 0
    for position in original_positions:
        if position != pointer[0]:
            other_plane = plane.with_obstruction(at=position)
            try:
                _ = emulate(other_plane, SecurityGuard(position=pointer[0], direction=pointer[1]))
            except InfiniteLoopException:
                loops += 1

    return loops


if __name__ == "__main__":
    print(main(read_input(input_path(__file__).replace(".txt", "_practice.txt"))))
    print(main(read_input(input_path(__file__))))
