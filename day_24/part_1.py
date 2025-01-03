import re
from typing import List, Dict
from queue import LifoQueue

from utils import time_it, read_input, input_path


PTRN = re.compile(r'(\w+)\s(\w+)\s(\w+)\s->\s(\w+)')

OPS = {
    "AND": lambda l, r: l and r,
    "OR": lambda l, r: l or r,
    "XOR": lambda l, r: l ^ r,
}


class Gate:
    def __init__(self, _id: str, op: str = "", depends: List[str] = None, output: int = None):
        self.id = _id
        self.output = output
        self.depends = depends or []
        self.op = op

    def __repr__(self):
        return f'Gate({self.id}, {self.output if self.output is not None else -1})'

    def flip(self, *args):
        self.output = OPS[self.op](*args)


def get_output(wire: str, gates: Dict[str, Gate]) -> int:
    queue = LifoQueue()
    queue.put(wire)

    while not queue.empty():
        w = queue.get()
        gate = gates[w]

        if gate.output is not None:
            continue

        queue.put(w)

        inputs = []
        for d in gate.depends:
            if gates[d].output is None:
                queue.put(d)
            else:
                inputs.append(gates[d].output)

        if len(inputs) == 2:
            gate.flip(*inputs)

    return gates[wire].output


@time_it
def main(data: str) -> int:
    hot_gates_raw, cold_gates_raw = data.split("\n\n")

    gates = {}
    for line in hot_gates_raw.splitlines():
        _id, output = line.split(": ")
        gates[_id] = Gate(_id=_id, output=int(output))

    for line in cold_gates_raw.splitlines():
        l, op, r, _id = PTRN.match(line).groups()
        gates[_id] = Gate(_id=_id, op=op, depends=[l, r])

    bits = []
    for wire in sorted((k for k in gates if k.startswith("z")), reverse=True):
        bits.append(get_output(wire, gates))

    return int("".join(map(str, bits)), 2)


if __name__ == "__main__":
    print(main(read_input(input_path(__file__).replace(".txt", "_practice.txt"))))
    print(main(read_input(input_path(__file__).replace(".txt", "_practice_2.txt"))))
    print(main(read_input(input_path(__file__))))
