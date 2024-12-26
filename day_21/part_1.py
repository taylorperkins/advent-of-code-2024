from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache, partial, reduce
from itertools import pairwise, product
from typing import List, Dict, Callable

from utils import read_input, input_path, time_it


@dataclass
class Coord:
    x: int
    y: int

    def __hash__(self):
        return hash((self.x, self.y))

    def move(self, direction: Coord, n: int = 1) -> Coord:
        return Coord(x=self.x + (direction.x*n), y=self.y + (direction.y*n))

    def distance(self, other: Coord) -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)


DIRECTIONS = {
    Coord(1, 0): ">",
    Coord(0, 1): "v",
    Coord(-1, 0): "<",
    Coord(0, -1): "^",
}

class Keypad:
    def __init__(self, values: List[str], label: str):
        self.label = label

        self._coord_values: Dict[Coord, str] = {}
        self._value_coords: Dict[str, Coord] = {}

        for y, line in enumerate(values):
            for x, value in enumerate(line):
                self._coord_values[Coord(x, y)] = value
                self._value_coords[value] = Coord(x, y)

    def __getitem__(self, item):
        if isinstance(item, str):
            return self._value_coords.get(item, None)
        return self._coord_values.get(item, "#")

    def __repr__(self):
        return f"Keypad({self.label})"

    @lru_cache
    def get_paths(self, start: str, end: str) -> List[str]:
        if start == end:
            return []

        current_paths = [(self[start], "",)]
        final_paths = []

        while current_paths:
            coord, path = current_paths.pop(0)
            current_distance = self[end].distance(coord)

            for direction, label in DIRECTIONS.items():
                neighbor_coord = coord.move(direction)
                neighbor = self[neighbor_coord]

                if neighbor == end:
                    final_paths.append(path + label)
                elif neighbor != "#" and self[end].distance(neighbor_coord) < current_distance:
                    current_paths.append((self[neighbor], path + label))

        return final_paths


DIRECTIONAL_KEYPAD = Keypad([
    "#^A",
    "<v>",
], label="Directional")

NUMERIC_KEYPAD = Keypad([
    "789",
    "456",
    "123",
    "#0A",
], label="Numeric")


def append_submit(value: str) -> str:
    if not value.startswith("A"):
        value = "A" + value
    if not value.endswith("A"):
        value += "A"

    return value


@lru_cache
def output_layer(_input: str) -> int:
    """Just count all the directions that the previous layer requests"""
    weight = len(_input)
    return weight


@lru_cache
def input_layer(_input: str, keypad: Keypad, next_layer: Callable[[str], int]) -> int:
    """Calculates the "weight" of `_input`.

    Each `_input` represents "stops" within `keypad`. Implicitly, each `_input`
    starts at "A".

    `_inputs` represent stops along _any_ keypad, numeric or directional.
    For example:
        029A -> (A -> 0), (0 -> 2), (2 -> 9), (9 -> A)
        <A   -> (A -> <), (< -> A)
        ^A   -> (A -> ^), (^ -> A)
        ^>^A -> (A -> ^), (^ -> >), (> -> ^), (^ -> A)
        vvvA -> (A -> v), (v -> v), (v -> v), (v -> A)

    And so on. This layer is responsible for splitting `_input` into it's respective
    start/stop pairs, calculating the possible paths of each start/stop pair,
    gathering the weights of each of those paths (through passing along to `next_layer`),
    then sorting paths by sub-path weights. Return the weight of the smallest path.
    """
    weights = [0]

    for start, end in pairwise("A" + _input):
        current_path_weights = []

        if start == end:
            # just account for the "A" prefix
            current_path_weights.append(1)
        else:
            for path in keypad.get_paths(start, end):
                current_path_weights.append(next_layer(path + "A"))

        assert len(current_path_weights) >= 1

        # account for branching paths
        weights = [
            l + r
            for l, r in product(weights, current_path_weights)
        ]

    return min(weights)


@time_it
def main(data: str) -> int:
    layers = [
        partial(input_layer, keypad=NUMERIC_KEYPAD),
        partial(input_layer, keypad=DIRECTIONAL_KEYPAD),
        partial(input_layer, keypad=DIRECTIONAL_KEYPAD),
    ]

    process = reduce(
        lambda l, r: partial(r, next_layer=l),
        layers[::-1],
        output_layer
    )

    total = 0
    for line in data.splitlines():
        weight = process(_input=line)
        code_value = int(line[:-1])
        print(f"{line}: {weight} - {code_value}")
        total += (weight * code_value)

    return total


if __name__ == "__main__":
    out = main(read_input(input_path(__file__).replace(".txt", "_practice.txt")))
    assert out == 126384, f"Expected 126384, got {out}"
    # 213536
    print("Real deal")
    print(main(read_input(input_path(__file__))))
