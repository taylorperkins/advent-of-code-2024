from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from functools import reduce
from typing import List, Optional, Set, Dict

from utils import time_it, read_input, input_path


@dataclass
class Coord:
    x: int
    y: int

    @property
    def neighbors(self) -> Set[Coord]:
        return {
            self.move(d)
            for d in directions
        }

    def __hash__(self):
        return hash((self.x, self.y))

    def move(self, direction: Coord) -> Coord:
        return Coord(x=self.x + direction.x, y=self.y + direction.y)


directions = (
    Coord(0, -1),
    Coord(1, 0),
    Coord(0, 1),
    Coord(-1, 0),
)


class Region:
    def __init__(self, label: str, plots: Set[Coord]):
        self.label = label
        self.plots = plots
        self.neighbors: Set[Coord] = self._calculate_neighbors(self.plots)

    @staticmethod
    def _calculate_neighbors(plots: Set[Coord]) -> Set[Coord]:
        neighbors = {
            neighbor
            for plot in plots
            for neighbor in plot.neighbors
        }

        return neighbors - plots

    @property
    def area(self):
        return len(self.plots)

    @property
    def perimeter(self):
        return len([
            neighbor
            for plot in self.plots
            for neighbor in plot.neighbors
            if neighbor not in self.plots
        ])

    def is_neighbor(self, coord: Coord):
        return coord in self.neighbors

    def add(self, coord: Coord) -> Region:
        if coord not in self.neighbors:
            raise Exception("Cannot add coord, not a neighbor.")

        return Region(label=self.label, plots=self.plots | {coord})

    def merge(self, other: Region) -> Region:
        if other.label != self.label:
            raise Exception("Cannot merge regions of different labels.")

        if not self.plots & other.plots:
            raise Exception("Cannot merge. Regions do not share a common plot.")

        return Region(label=other.label, plots=other.plots | self.plots)


class Plane:
    def __init__(self, data: List[List[str]]):
        self.data = data
        self.shape = len(data), len(data[0])

    def _exists(self, c: Coord):
        return 0 <= c.y < self.shape[0] and 0 <= c.x < self.shape[1]

    def get(self, item: Coord) -> Optional[str]:
        if self._exists(item):
            return self.data[item.y][item.x]

    def __iter__(self):
        # reading order
        for y in range(self.shape[1]):
            for x in range(self.shape[0]):
                c = Coord(x, y)
                yield c, self.get(c)


@time_it
def main(data: str) -> int:
    plane = Plane([list(p) for p in data.splitlines()])

    regions: Dict[str, List[Region]] = {}

    for coord, plant in plane:
        if plant not in regions:
            regions[plant] = [Region(label=plant, plots={coord})]
            continue

        neighboring_regions = []
        others = []
        for region in regions[plant]:
            if region.is_neighbor(coord):
                neighboring_regions.append(region)
            else:
                others.append(region)

        if not neighboring_regions:
            regions[plant].append(Region(label=plant, plots={coord}))
            continue

        merged_regions = reduce(
            lambda l, r: l.merge(r.add(coord)),
            neighboring_regions,
            Region(label=plant, plots={coord})
        )

        regions[plant] = others + [merged_regions]

    total = 0
    for plant in regions:
        # print(plant)
        for region in regions[plant]:
            # print("\t", region.area, region.perimeter, region.neighbors)
            total += (region.area * region.perimeter)

    return total


if __name__ == "__main__":
    print(main(read_input(input_path(__file__).replace(".txt", "_practice.txt"))))
    print(main(read_input(input_path(__file__))))
