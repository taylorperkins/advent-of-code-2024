from __future__ import annotations

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

    @property
    def op_id(self):
        d1, d2 = sorted(self.depends)
        return self.op, d1, d2,


def print_dependents(gate: Gate, gates: Dict[str, Gate], level: int = 0, n: int = -1):
    if n < 0:
        return

    print("\t" * level, f"{gate.id} - {gate.op} ({gate.output})")

    if not gate.depends:
        return

    for d in gate.depends:
        print_dependents(gates[d], gates, level+1, n-1)


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


def get_bits(prefix: str, gates: Dict[str, Gate]) -> str:
    bits = []
    for wire in sorted((k for k in gates if k.startswith(prefix)), reverse=True):
        bits.append(get_output(wire, gates))

    return "".join(map(str, bits))


def validator(gates: Dict[str, Gate]):
    output_keys = sorted(k for k in gates if k.startswith("z"))

    # some caching support for cascading adder
    prev_half_adder = []
    expected_cascade_key = ...
    prev_step = ""

    for i, ok in enumerate(output_keys):

        print(f"\n\nValidating {ok}")
        print_dependents(gates[ok], gates, n=5)

        try:
            i = ok[1:]

            if i == "00":
                assert sorted(gates[ok].depends) == ["x00", "y00"]
                prev_step = i

            # half-adder
            elif i == "01":
                _AND, _XOR = sorted(
                    gates[ok].depends,
                    key=lambda g: gates[g].op
                )

                assert gates[_AND].op == "AND"
                assert sorted(gates[_AND].depends) == ["x00", "y00"]

                assert gates[_XOR].op == "XOR"
                assert sorted(gates[_XOR].depends) == ["x01", "y01"]

                prev_half_adder = [_AND, _XOR]
                prev_step = i

            # first full-adder
            elif i == "02":
                _OR, _XOR = sorted(
                    gates[ok].depends,
                    key=lambda g: gates[g].op
                )

                assert gates[_XOR].op == "XOR"
                assert sorted(gates[_XOR].depends) == ["x02", "y02"]

                assert gates[_OR].op == "OR"

                # the OR gate should be followed by two ANDs. One of them
                # being the root, and the other being the prev half-adder.
                cascade, root = sorted(
                    gates[_OR].depends,
                    key=lambda d: gates[d].op_id == ("AND", "x01", "y01",)
                )

                assert gates[cascade].op_id == ("AND", prev_half_adder[0], prev_half_adder[1],)

                a, b = sorted([_XOR, _OR])
                expected_cascade_key = ("AND", a, b,)
                prev_step = i

            # the remaining adders - with cascading carry
            else:
                if i == "45":
                    continue
                else:
                    assert gates[ok].op == "XOR"

                _OR, _XOR = sorted(
                    gates[ok].depends,
                    key=lambda g: gates[g].op
                )

                assert gates[_OR].op == "OR"

                # the OR gate should be followed by two ANDs. One of them
                # being the root, and the other being the prev half-adder.
                cascade, root = sorted(
                    gates[_OR].depends,
                    key=lambda d: gates[d].op_id == ("AND", "x" + prev_step, "y" + prev_step,)
                )

                assert gates[root].op_id == ("AND", "x" + prev_step, "y" + prev_step,)

                assert gates[cascade].op_id == expected_cascade_key, \
                    f"Invalid cascade key. Expected {expected_cascade_key}, got {gates[cascade].op_id}"

                a, b = sorted([_XOR, _OR])
                expected_cascade_key = ("AND", a, b,)
                prev_step = i
        except:
            raise


@time_it
def main(data: str) -> str:
    hot_gates_raw, cold_gates_raw = data.split("\n\n")

    gates = {}
    for line in hot_gates_raw.splitlines():
        _id, output = line.split(": ")
        gates[_id] = Gate(_id=_id, output=int(output))

    for line in cold_gates_raw.splitlines():
        l, op, r, _id = PTRN.match(line).groups()
        gates[_id] = Gate(_id=_id, op=op, depends=[l, r])

    x = get_bits("x", gates)
    y = get_bits("y", gates)
    z = get_bits("z", gates)

    print(f"{x} | {int(x, 2)}")
    print(f"{y} | {int(y, 2)}")
    print(f"{z} | {int(z, 2)}")

    expected = int(x, 2) + int(y, 2)
    expected_bin = bin(expected)[2:].rjust(len(x))

    print(f"{expected_bin} | {expected}")

    validator(gates)
    manual_swaps = sorted([
        "fgc", "z12",
        "mtj", "z29",
        "vvm", "dgr",
        "dtv", "z37"
    ])

    return ",".join(manual_swaps)


if __name__ == "__main__":
    # print(main(read_input(input_path(__file__))))
    print(main(read_input(input_path(__file__).replace(".txt", "_fixed.txt"))))
