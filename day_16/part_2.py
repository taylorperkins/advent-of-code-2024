from __future__ import annotations

import bisect
from copy import deepcopy
from dataclasses import dataclass
from typing import List, Optional, Dict, Set

from utils import time_it, read_input, input_path


@dataclass
class Coord:
    x: int
    y: int

    def __hash__(self):
        return hash((self.x, self.y))

    def move(self, direction: Coord) -> Coord:
        return Coord(x=self.x + direction.x, y=self.y + direction.y)

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


class HitBoundaryException(Exception):
    pass


class Plane:
    def __init__(self, data: List[List[str]]):
        self.data = data
        self.shape = len(data), len(data[0])

    def _exists(self, c: Coord):
        return 0 <= c.y < self.shape[0] and 0 <= c.x < self.shape[1]

    def get(self, item: Coord, default = None) -> Optional[str]:
        if self._exists(item):
            return self.data[item.y][item.x]
        return default

    def __getitem__(self, item: Coord) -> str:
        assert self._exists(item)
        return self.data[item.y][item.x]

    def __iter__(self):
        # reading order
        for y in range(self.shape[1]):
            for x in range(self.shape[0]):
                c = Coord(x, y)
                yield c, self.get(c)

    def print(self):
        for line in self.data:
            print("".join(line))


@dataclass
class Reindeer:
    position: Coord
    direction: Coord
    path: Set[Coord]
    score: int

    def __eq__(self, other: Reindeer):
        return self.position == other.position and self.score == other.score


def race(
    _map: Plane,
    start_position: Coord,
    start_direction: Coord,
) -> Reindeer:

    all_reindeer = [
        Reindeer(
            position=start_position,
            direction=start_direction,
            path={start_position},
            score=0
        )
    ]

    # Keep track by position/direction
    visited: Dict[(Coord, Coord), int] = {}

    while True:
        # always pull from the front, assuming ordered
        reindeer = all_reindeer.pop(0)

        # pruning
        if reindeer.score > visited.get((reindeer.position, reindeer.direction), reindeer.score):
            continue
        visited[(reindeer.position, reindeer.direction)] = reindeer.score

        # Pruning attempt
        # If reindeer are found at the same position with the same score,
        # converge their histories into one, and discard the extra reindeer
        while True:
            try:
                i = all_reindeer.index(reindeer)
            except ValueError:
                break
            else:
                other = all_reindeer.pop(i)
                reindeer.path |= other.path

        # This reindeer should have all the converged paths
        if _map[reindeer.position] == "E":
            return reindeer

        for d, s in [
            (reindeer.direction, 1,),
            (reindeer.direction.pivot_right, 1001,),
            (reindeer.direction.pivot_left, 1001,),
        ]:
            coord = reindeer.position.move(d)
            if _map.get(coord, default="#") != "#" and coord not in reindeer.path:
                bisect.insort_left(
                    all_reindeer,
                    Reindeer(
                        position=coord,
                        direction=d,
                        path=reindeer.path | {coord},
                        score=reindeer.score + s
                    ),
                    key=lambda r: r.score
                )


def get_best_reindeer():
    pass



@time_it
def main(data: str) -> int:
    plane = Plane([list(row) for row in data.splitlines()])
    start_position = next(c for c, v in plane if v == "S")
    start_direction = Coord(x=1, y=0)

    reindeer = race(plane, start_position=start_position, start_direction=start_direction)
    return len(set(reindeer.path))


if __name__ == "__main__":
    print(main(read_input(input_path(__file__).replace(".txt", "_practice.txt"))))
    print(main(read_input(input_path(__file__).replace(".txt", "_practice_2.txt"))))
    print(main(read_input(input_path(__file__))))
