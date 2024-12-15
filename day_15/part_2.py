from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Generator

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
        for y in range(self.shape[0]):
            for x in range(self.shape[1]):
                c = Coord(x, y)
                yield c, self[c]

    def get_target_coords(self, coord: Coord, direction: Coord) -> Generator[Coord]:
        value = self[coord]

        match value:
            case "#": raise HitBoundaryException()
            case "@":
                yield coord
                yield from self.get_target_coords(coord.move(direction), direction)
            case "[" | "]":
                yield coord
                if direction.x != 0:
                    close = coord.move(direction)
                    yield close
                    yield from self.get_target_coords(close.move(direction), direction)

                else:
                    close = coord.move(Coord(x=1, y=0) if value == "[" else Coord(-1, 0))
                    yield close
                    yield from self.get_target_coords(coord.move(direction), direction)
                    yield from self.get_target_coords(close.move(direction), direction)

    def print(self):
        for line in self.data:
            print("".join(line))


directions = {
    "^": Coord(x=0, y=-1),
    ">": Coord(x=1, y=0),
    "v": Coord(x=0, y=1),
    "<": Coord(x=-1, y=0),
}


def move(robot: Coord, movement: str, warehouse: Plane) -> Coord:
    direction = directions[movement]

    try:
        # use a set here to combat against duplicate paths b/c I am bad at this
        target_coords = list(set(warehouse.get_target_coords(
            coord=robot,
            direction=direction
        )))
    except HitBoundaryException:
        return robot
    else:
        # sorts in ASC by default
        # moving down or right, reverse to DESC
        if direction.x != 0:
            target_coords.sort(
                key=lambda c: c.x,
                reverse=direction.x == 1
            )
        else:
            target_coords.sort(
                key=lambda c: c.y,
                reverse=direction.y == 1
            )

        for coord in target_coords:
            warehouse.swap(coord, coord.move(direction))

        return robot.move(direction)


def expand(row: str):
    for v in row:
        match v:
            case "#": values = ["#", "#"]
            case "O": values = ["[", "]"]
            case ".": values = [".", "."]
            case _:   values = ["@", "."]
        yield from values


@time_it
def main(data: str) -> int:
    raw_warehouse, movements = data.split("\n\n")
    warehouse = Plane([list(expand(row)) for row in raw_warehouse.splitlines()])

    robot = next(c for c, v in warehouse if v == "@")

    for m in movements.replace("\n", ""):
        robot = move(robot=robot, movement=m, warehouse=warehouse)

    warehouse.print()

    return sum([
        100 * c.y + c.x
        for c, v in warehouse
        if v == "["
    ])


if __name__ == "__main__":
    print(main(read_input(input_path(__file__).replace(".txt", "_practice.txt"))))
    print(main(read_input(input_path(__file__).replace(".txt", "_practice_2.txt"))))
    print(main(read_input(input_path(__file__).replace(".txt", "_practice_3.txt"))))
    print(main(read_input(input_path(__file__))))
