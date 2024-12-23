from __future__ import annotations

from typing import Set

from utils import time_it, read_input, input_path


class Node:
    def __init__(self, _id: str):
        self.id = _id
        self.neighbors: Set[Node] = set()

    def __repr__(self):
        return f"Node({self.id})"

    def __hash__(self):
        return hash(self.id)

    def __lt__(self, other: Node):
        return self.id < other.id

    def __gt__(self, other):
        return self.id > other.id

    def connect(self, other: Node):
        self.neighbors.add(other)
        other.neighbors.add(self)

    def is_connected(self, other: Node) -> bool:
        return other in self.neighbors

    def startswith(self, prefix: str = "") -> bool:
        return self.id.startswith(prefix)

    def shared_connections(self, other: Node) -> Set[Node]:
        return self.neighbors & other.neighbors


@time_it
def main(data: str) -> int:
    graph = {}

    for line in data.splitlines():
        left, right = line.split("-")

        if left not in graph:
            graph[left] = Node(left)

        if right not in graph:
            graph[right] = Node(right)

        graph[left].connect(graph[right])

    result = set()

    for node in graph.values():
        for neighbor in node.neighbors:
            for sc in node.shared_connections(neighbor):
                out = tuple(sorted([node, neighbor, sc]))
                if any(n.startswith("t") for n in out):
                    result.add(out)

    return len(result)


if __name__ == "__main__":
    print(main(read_input(input_path(__file__).replace(".txt", "_practice.txt"))))
    print(main(read_input(input_path(__file__))))
