from __future__ import annotations

from dataclasses import dataclass
from functools import partial
from itertools import cycle
import pickle
import re
from typing import Callable, Dict, List

import numpy as np

from utils import time_it, read_input, input_path


PTRN = re.compile(r'p=(.*),(.*)\sv=(.*),(.*)')


@dataclass
class Coord:
    x: int
    y: int

    def __hash__(self):
        return hash((self.x, self.y))

    def move(self, direction: Coord, n: int) -> Coord:
        return Coord(
            x=self.x + direction.x*n,
            y=self.y + direction.y*n
        )

    @property
    def neighbors(self) -> List[Coord]:
        return [
            self.move(d, 1)
            for d in [
                Coord(-1, -1),
                Coord(0, -1),
                Coord(1, -1),
                Coord(-1, 0),
                Coord(1, 0),
                Coord(-1, 1),
                Coord(0, 1),
                Coord(1, 1),
            ]
        ]


@dataclass
class Robot:
    position: Coord
    velocity: Coord

    def move(self, n: int) -> Robot:
        return Robot(self.position.move(self.velocity, n), self.velocity)

    def normalize(self, fn: Callable[[Coord], Coord]) -> Robot:
        return Robot(fn(self.position), self.velocity)


def area_correction(shape: Coord, position: Coord) -> Coord:
    xm = position.x // shape.x
    ym = position.y // shape.y

    return Coord(
        position.x - xm*shape.x,
        position.y - ym*shape.y
    )


def emulate(
    robots: List[Robot],
    shape: Coord,
    n: int
) -> Dict[int, np.array]:

    steps = cycle([
        iter(range(49, -10000, -2)),
        iter(range(54, 10000, 2))
    ])

    out = {}
    normalization_fn = partial(area_correction, shape)

    current = 28
    while True:
        if current > 8500:
            break

        try:
            current += next(next(steps))
        except StopIteration:
            break
        out[current] = np.zeros((shape.y, shape.x,))

        for robot in robots:
            robot = (
                robot
                .move(current)
                .normalize(normalization_fn)
            )

            out[current][robot.position.y][robot.position.x] += 1

    return out


@time_it
def main(data: str, shape: Coord):
    robots = []
    for line in data.splitlines():
        px, py, vx, vy = map(int, PTRN.match(line).groups())

        robots.append(Robot(
            position=Coord(px, py),
            velocity=Coord(vx, vy)
        ))

    out = emulate(robots, shape, n=50000)

    with open("out.pkl", "wb") as f:
        pickle.dump(out, f)


if __name__ == "__main__":
    # print(main(read_input(input_path(__file__).replace(".txt", "_practice.txt")), shape=Coord(x=11, y=7)))
    print(main(read_input(input_path(__file__)), shape=Coord(x=101, y=103)))
