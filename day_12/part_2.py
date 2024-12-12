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
        horizontal_directions = (Coord(x=1, y=0), Coord(x=-1, y=0),)
        vertical_directions = (Coord(x=0, y=1), Coord(x=0, y=-1),)

        dmap = {
            d: defaultdict(list)
            for d in directions
        }

        # a single "neighbor" plot can represent 4 perimeters
        # so - keep track of the direction of the plot that the neighbor
        # is touching.
        # structure ends up like:
        # {
        #   <direction>: {
        #       0: [1, 2, 5, 6, 7],
        #       4: [5, 9, 10, 11],
        #       ...
        #   }, ...
        # }
        for neighbor in self.neighbors:
            for d in horizontal_directions:
                if neighbor.move(d) in self.plots:
                    dmap[d][neighbor.x].append(neighbor.y)

            for d in vertical_directions:
                if neighbor.move(d) in self.plots:
                    dmap[d][neighbor.y].append(neighbor.x)

        # for each direction/index combination, sort all the
        # axes that fall along the index. Count the "splits"
        # for that index, representing the perimeter
        perimeter = 0
        for _map in dmap.values():
            for axis, values in _map.items():
                s = sorted(values)
                n_sides = 1
                current = s[0]
                for v in s[1:]:
                    if v > current+1:
                        n_sides += 1
                    current = v

                perimeter += n_sides

        return perimeter

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

    # split the plane into "regions" by label
    regions: Dict[str, List[Region]] = {}
    for coord, plant in plane:

        # create a new "region" of 1 plot
        if plant not in regions:
            regions[plant] = [Region(label=plant, plots={coord})]
            continue

        # figure out if the plot can "merge" into an existing region
        neighboring_regions = []
        others = []
        for region in regions[plant]:
            if region.is_neighbor(coord):
                neighboring_regions.append(region)
            else:
                others.append(region)

        # can't merge, create a new one
        if not neighboring_regions:
            regions[plant].append(Region(label=plant, plots={coord}))
            continue

        # for all regions the plot is touching, add the plot to the
        # region and merge all the regions
        merged_regions = reduce(
            lambda l, r: l.merge(r.add(coord)),
            neighboring_regions,
            Region(label=plant, plots={coord})
        )

        regions[plant] = others + [merged_regions]

    total = 0
    for plant in regions:
        for region in regions[plant]:
            total += (region.area * region.perimeter)

    return total


if __name__ == "__main__":
    print(main(read_input(input_path(__file__).replace(".txt", "_practice.txt"))))
    print(main(read_input(input_path(__file__))))
