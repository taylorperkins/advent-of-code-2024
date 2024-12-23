from __future__ import annotations

from collections import Counter
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
def main(data: str) -> str:
    graph = {}

    for line in data.splitlines():
        left, right = line.split("-")

        if left not in graph:
            graph[left] = Node(left)

        if right not in graph:
            graph[right] = Node(right)

        graph[left].connect(graph[right])

    networks = set()
    for node in graph.values():
        connection_count = Counter(node.neighbors)

        for neighbor in node.neighbors:
            connection_count.update(node.shared_connections(neighbor))

        max_count = max(connection_count.values())
        max_nodes = [n for n, c in connection_count.items() if c == max_count]
        if len(max_nodes) == max_count:
            networks.add(tuple(sorted([node] + max_nodes)))

    networks = sorted(list(networks), key=lambda n: -len(n))
    return ",".join([n.id for n in networks[0]])


if __name__ == "__main__":
    print(main(read_input(input_path(__file__).replace(".txt", "_practice.txt"))))
    print(main(read_input(input_path(__file__))))
