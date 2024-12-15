from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from utils import time_it, read_input, input_path


@dataclass
class Coord:
    x: int
    y: int

    def __hash__(self):
        return hash((self.x, self.y))

    def move(self, direction: Coord) -> Coord:
        return Coord(x=self.x + direction.x, y=self.y + direction.y)


class HitBoundaryException(Exception):
    pass


class Plane:
    def __init__(self, data: List[List[str]]):
        self.data = data
        self.shape = len(data), len(data[0])

    def _exists(self, c: Coord):
        return 0 <= c.y < self.shape[0] and 0 <= c.x < self.shape[1]

    def get(self, item: Coord) -> Optional[str]:
        if self._exists(item):
            return self.data[item.y][item.x]

    def __getitem__(self, item: Coord) -> str:
        assert self._exists(item)
        return self.data[item.y][item.x]

    def swap(self, this: Coord, that: Coord):
        this_value, that_value = self.get(this), self.get(that)

        if this_value is None or that_value is None:
            raise Exception("Can't do that, dumb-ass.")

        self.data[this.y][this.x] = that_value
        self.data[that.y][that.x] = this_value

    def __iter__(self):
        # reading order
        for y in range(self.shape[1]):
            for x in range(self.shape[0]):
                c = Coord(x, y)
                yield c, self.get(c)

    def get_path_to_space(self, start: Coord, direction: Coord) -> List[Coord]:
        path = [start]
        current = start
        while True:
            _next = current.move(direction)
            match self[_next]:
                case "#": return []
                case ".": return path
                case "O":
                    path.append(_next)
                    current = _next

    def print(self):
        for line in self.data:
            print("".join(line))


directions = {
    "^": Coord(x=0, y=-1),
    ">": Coord(x=1, y=0),
    "v": Coord(x=0, y=1),
    "<": Coord(x=-1, y=0),
}


def move(robot: Coord, direction: Coord, warehouse: Plane) -> Coord:
    path = warehouse.get_path_to_space(
        start=robot,
        direction=direction
    )

    if not path:
        return robot

    for coord in path[::-1]:
        warehouse.swap(coord, coord.move(direction))

    return robot.move(direction)


@time_it
def main(data: str) -> int:
    raw_warehouse, movements = data.split("\n\n")
    warehouse = Plane([list(row) for row in raw_warehouse.splitlines()])

    robot = next(c for c, v in warehouse if v == "@")

    for m in movements.replace("\n", ""):
        robot = move(robot=robot, direction=directions[m], warehouse=warehouse)

    warehouse.print()

    return sum([
        100 * c.y + c.x
        for c, v in warehouse
        if v == "O"
    ])


if __name__ == "__main__":
    print(main(read_input(input_path(__file__).replace(".txt", "_practice.txt"))))
    print(main(read_input(input_path(__file__).replace(".txt", "_practice_2.txt"))))
    print(main(read_input(input_path(__file__))))
