from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from functools import partial, reduce
import math
import re
from typing import Callable, Dict

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


def assign_quadrant(shape: Coord, coord: Coord) -> int:
    x_axis, y_axis = shape.x // 2, shape.y // 2

    if coord.x == x_axis or coord.y == y_axis:
        return -1

    match (coord.x > x_axis, coord.y > y_axis):
        case (True, False):  return 1
        case (False, False): return 2
        case (False, True):  return 3
        case (True, True):   return 4


@time_it
def main(data: str, shape: Coord) -> int:
    normalization_fn = partial(area_correction, shape)
    quadrant_fn = partial(assign_quadrant, shape)

    coord_counter: Dict[Coord, int] = Counter()
    quadrant_counter: Dict[int, int] = Counter()
    for line in data.splitlines():
        px, py, vx, vy = map(int, PTRN.match(line).groups())

        robot = (
            Robot(
                position=Coord(px, py),
                velocity=Coord(vx, vy)
            )
            .move(100)
            .normalize(normalization_fn)
        )

        coord_counter[robot.position] += 1
        quadrant_counter[quadrant_fn(robot.position)] += 1

    # debug support - just to print it out
    _map = [['.']*shape.x for _ in range(shape.y)]
    for k, v in coord_counter.items():
        _map[k.y][k.x] = str(v)
    for line in _map:
        print("".join(line))


    return reduce(
        lambda l, r: l * r,
        [v for k, v in quadrant_counter.items() if k != -1],
        1
    )


if __name__ == "__main__":
    print(main(read_input(input_path(__file__).replace(".txt", "_practice.txt")), shape=Coord(x=11, y=7)))
    print(main(read_input(input_path(__file__)), shape=Coord(x=101, y=103)))
