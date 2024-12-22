from __future__ import annotations

import abc
from dataclasses import dataclass
from functools import lru_cache
from typing import List, Dict, Optional

from utils import time_it, read_input, input_path


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


DIRECTION_TO_LABEL = {
    Coord(-1, 0): "<",
    Coord(0, -1): "^",
    Coord(1, 0):  ">",
    Coord(0, 1): "v",
}

LABEL_TO_DIRECTION = {
    "<": Coord(-1, 0),
    "^": Coord(0, -1),
    ">": Coord(1, 0),
    "v": Coord(0, 1),
}

DIRECTION_WEIGHTS = {
    "<": 3,
    "v": 2,
    "^": 1,
    ">": 1
}


class Keypad:
    def __init__(self, values: List[List[str]]):
        self.value_map: Dict[Coord, str] = {}
        # inverse of value_map
        self.coord_map: Dict[str, Coord] = {}

        for y, row in enumerate(values):
            for x, value in enumerate(row):
                if value is not None:
                    coord = Coord(x, y)
                    self.value_map[coord] = value
                    self.coord_map[value] = coord

    def __getitem__(self, item: str) -> Coord:
        return self.coord_map[item]

    def get_value(self, coord: Coord) -> Optional[str]:
        return self.value_map.get(coord)

    @lru_cache
    def shortest_path(self, start: Coord, end: Coord) -> List[str]:
        directions = []

        if start == end:
            return directions

        paths = self.get_paths(start, end)
        sorted_path = sorted(paths[0])

        weighted_paths = []

        for sp in (sorted_path, sorted_path[::-1]):
            if sp in paths:
                d_weight = DIRECTION_WEIGHTS[sp[0]]
                weighted_paths.append((d_weight, sp))

        if weighted_paths:
            weighted_paths = sorted(weighted_paths)
            directions = weighted_paths[0][1]

        else:
            weighted_paths = sorted([
                (
                    [DIRECTION_WEIGHTS[d] for d in path],
                    idx
                )
                for idx, path in enumerate(paths)
            ])

            directions = paths[weighted_paths[0][1]]

        print(f"Directions({self.get_value(start)}, {self.get_value(end)}): {directions}")
        return directions

    def get_paths(self, start: Coord, end: Coord) -> List[List[str]]:
        current_paths = [
            {
                "tail": start,
                "directions": []
            }
        ]

        final_paths = []
        while current_paths:
            path = current_paths.pop(0)
            coord = path["tail"]

            if coord == end:
                final_paths.append(path["directions"])
                continue

            distance = end.distance(coord)
            for direction, label in DIRECTION_TO_LABEL.items():
                neighbor = coord.move(direction)
                if end.distance(neighbor) < distance and self.get_value(neighbor) is not None:
                    current_paths.append({
                        "tail": neighbor,
                        "directions": path["directions"] + [label]
                    })

        return final_paths

    def is_valid_path(self, start: Coord, path: List[str]) -> bool:
        current = start
        for d in path:
            direction = LABEL_TO_DIRECTION[d]
            current = current.move(direction)
            if self.get_value(current) is None:
                return False
        return True


class Event(list):
    """Simple observer implementation.

    Publishers initialize an Event, and call the event as
    necessary.

    Subscribers add functions to the publishers event, which
    will get called as events occur.
    """
    def __call__(self, *args, **kwargs):
        for fn in self:
            fn(*args, **kwargs)


class Operator(metaclass=abc.ABCMeta):
    def __init__(self, keypad: Keypad, name: str):
        self.name = name
        self.keypad = keypad
        self.position = self.keypad["A"]

        self.press_event = Event()
        self.request_event = Event()

    def __repr__(self):
        return f"Operator({self.name}, {self.value})"

    @property
    def value(self):
        return self.keypad.get_value(self.position)

    @abc.abstractmethod
    def handle_request(self, command: str):
        pass


class Human(Operator):

    def handle_request(self, command: str):
        """Receive a request from a robot.
        The human doesn't actually have to do anything other
        than "press" the buttons received. So, this becomes
        a really simple handler.
        """
        self.press_event(command)


class Robot(Operator):

    def handle_request(self, command: str):
        """Goes through the process of requesting to move to
        command position, then requesting to press once has
        been moved.

        :param command:
        :return:
        """
        target = self.keypad[command]

        for direction in self.keypad.shortest_path(self.position, target):
            self.request_event(direction)

        assert self.value == command

        # now that we're at the position, request to press it.
        self.request_event("A")

    def handle_press(self, command):
        if command == "A":
            self.press_event(self.value)
            return

        match command:
            case "^": d = Coord(0, -1)
            case ">": d = Coord(1, 0)
            case "v": d = Coord(0, 1)
            case "<": d = Coord(-1, 0)
            case _: raise Exception("Unexpected direction")

        self.position = self.position.move(d)


class SequenceCounter:
    def __init__(self):
        self.total = 0

    def handle_press(self, _):
        self.total += 1


class PressAccumulator:
    def __init__(self):
        self.values = []

    def press_handler(self, value):
        self.values.append(value)

NUMERIC_KEYPAD = Keypad([
    ["7", "8", "9"],
    ["4", "5", "6"],
    ["1", "2", "3"],
    [None, "0", "A"],
])

DIRECTIONAL_KEYPAD = Keypad([
    [None, "^", "A"],
    ["<", "v", ">"],
])

@time_it
def main(data: str) -> int:

    total = 0
    for code in data.splitlines():
        sequence_counter = SequenceCounter()

        robot_1 = Robot(keypad=NUMERIC_KEYPAD, name="Robot 1")
        robot_2 = Robot(keypad=DIRECTIONAL_KEYPAD, name="Robot 2")
        robot_3 = Robot(keypad=DIRECTIONAL_KEYPAD, name="Robot 3")

        human = Human(keypad=DIRECTIONAL_KEYPAD, name="Human")

        r1_pa = PressAccumulator()
        r2_pa = PressAccumulator()
        r3_pa = PressAccumulator()
        h_pa = PressAccumulator()

        robot_1.press_event.append(r1_pa.press_handler)
        robot_2.press_event.append(r2_pa.press_handler)
        robot_3.press_event.append(r3_pa.press_handler)
        human.press_event.append(h_pa.press_handler)

        robot_1.request_event.append(robot_2.handle_request)
        robot_2.press_event.append(robot_1.handle_press)

        robot_2.request_event.append(robot_3.handle_request)
        robot_3.press_event.append(robot_2.handle_press)

        robot_3.request_event.append(human.handle_request)
        human.press_event.append(robot_3.handle_press)

        human.press_event.append(sequence_counter.handle_press)

        for value in code:
            robot_1.handle_request(value)

        # for label, pa in (
        #     ("Robot 1", r1_pa),
        #     ("Robot 2", r2_pa),
        #     ("Robot 3", r3_pa),
        #     ("Human", h_pa),
        # ):
        #     print(label)
        #     for i, d in enumerate(''.join(pa.values).split('A')):
        #         print(f"\t{i+1}: {d}")

        print(f"Robot 1: {''.join(r1_pa.values)}")
        print(f"Robot 2: {''.join(r2_pa.values)}")
        print(f"Robot 3: {''.join(r3_pa.values)}")
        print(f"Human: {''.join(h_pa.values)}")

        print("\n", sequence_counter.total, code[:-1])
        total += (sequence_counter.total * int(code[:-1]))

    return total


if __name__ == "__main__":
    print(main(read_input(input_path(__file__).replace(".txt", "_practice.txt"))))
    # 218300 - too high
    print("Real deal")
    print(main(read_input(input_path(__file__))))
