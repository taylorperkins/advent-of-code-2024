from __future__ import annotations

import bisect
from dataclasses import dataclass
from typing import List, Optional, Set

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

    def distance(self, other: Coord):
        return abs(self.x - other.x) + abs(self.y - other.y)


class Plane:
    def __init__(self, shape: Coord):
        self.shape = shape

    def exists(self, c: Coord):
        return 0 <= c.y < self.shape.y and 0 <= c.x < self.shape.x

    def print(self, masks: List[(List[Coord], str)] = None):
        masks = masks or []
        mask = {}
        for path, value in masks:
            for coord in path:
                mask[coord] = value

        for y in range(self.shape.y):
            print("".join([
                mask.get(Coord(x, y), ".")
                for x in range(self.shape.x)
            ]))


@dataclass
class Path:
    position: Coord
    direction: Coord
    path: Set[Coord]
    steps: int = 0


def search(falling_bytes: List[Coord], start: Coord, stop: Coord, shape: Coord) -> Path:
    plane = Plane(shape=shape)
    falling_bytes = set(falling_bytes)

    paths = [
        Path(position=start, direction=Coord(1, 0), path={start})
    ]

    visited = {start}

    while True:
        next_paths = []

        for path in paths:
            if path.position == stop:
                return path

            for d in (
                path.direction,
                path.direction.pivot_left,
                path.direction.pivot_right
            ):
                position = path.position.move(d)
                if (
                    plane.exists(position)
                    and position not in visited
                    and position not in path.path
                    and (path.path | {position}).isdisjoint(falling_bytes)
                ):
                    visited.add(position)
                    next_paths.append(
                        Path(
                            position=position,
                            direction=d,
                            path=path.path | {position},
                            steps=path.steps + 1
                        )
                    )

        paths = next_paths


@time_it
def main(data: str, stop: Coord, n_bytes: int) -> int:

    falling_bytes: List[Coord] = []
    for line in data.splitlines():
        x, y = line.split(",")
        falling_bytes.append(Coord(int(x), int(y)))

    best_path = search(
        falling_bytes=falling_bytes[:n_bytes],
        start=Coord(0, 0),
        stop=stop,
        shape=Coord(stop.x+1, stop.y+1)
    )

    (
        Plane(Coord(stop.x + 1, stop.y + 1))
        .print(
            masks=[
                (best_path.path, "O",),
                (falling_bytes[:n_bytes], "#",)
            ]
        )
    )

    return best_path.steps


if __name__ == "__main__":
    print(main(read_input(input_path(__file__).replace(".txt", "_practice.txt")), stop=Coord(6, 6), n_bytes=12))
    print(main(read_input(input_path(__file__)), stop=Coord(70, 70), n_bytes=1024))
