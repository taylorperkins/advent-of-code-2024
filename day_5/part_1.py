from __future__ import annotations

from utils import time_it, read_input, input_path


class Node:
    def __init__(self, value: int):
        self.value = value
        self.lt = set()
        self.gt = set()

    def __eq__(self, other: Node):
        return self.value == other.value

    def __ne__(self, other: Node):
        return not self == other

    def __hash__(self):
        return self.value

    def __repr__(self):
        return f'Node({self.value})'

    def __lt__(self, other: Node):
        return other in self.lt

    def __gt__(self, other):
        return other in self.gt


@time_it
def main(data: str) -> int:
    """Parse the input into rules and pages.
    The value ordering within each page is determined
    by the initial rules. Determine if the raw page is
    sorted correctly based on the rules.

    Solve through creating a pseudo-graph of the rules.
    Each rule has two parts, like: `47|31`.
    In this rule, 47 comes before 31.
    Create a "node" of each side, and keep track of
    this comparison. For node 47, note that it is lt node 31,
    and vice-versa. Each node supports comparison operators
    for measuring equality/lt/gt, etc. This makes it so that
    if you have a list of nodes, you can just use the base-python
    sorting to put them in the right order.

    :param data:
    :return int: the sum of the "middle" value for each correct page
    """

    rules_raw, pages_raw = data.split("\n\n")

    graph = {}
    for line in rules_raw.splitlines():
        left, right = map(int, line.split("|"))
        if left not in graph:
            graph[left] = Node(left)

        if right not in graph:
            graph[right] = Node(right)

        graph[left].lt.add(graph[right])
        graph[right].gt.add(graph[left])

    total = 0
    for line in pages_raw.splitlines():
        page = [int(v) for v in line.split(",")]
        nodes = [graph[n] for n in page]

        s = [n.value for n in sorted(nodes)]

        if s == page:
            total += page[len(page) // 2]

    return total


if __name__ == "__main__":
    print(main(read_input(input_path(__file__).replace(".txt", "_practice.txt"))))
    print(main(read_input(input_path(__file__))))
