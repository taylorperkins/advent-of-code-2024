import re
from dataclasses import dataclass
from typing import List, Generator

from utils import time_it, read_input, input_path


PTRN = re.compile(r'.*A:\s(\d+)\n.*B:\s(\d+)\n.*C:\s(\d+)\n\nProgram:\s(.*)')


@dataclass
class Computer:
    A: int
    B: int
    C: int

    instruction_pointer: int = 0

    def combo(self, operand: int) -> int:
        match operand:
            case 0 | 1 | 2 | 3: return operand
            case 4: return self.A
            case 5: return self.B
            case 6: return self.C
            case _: raise Exception()

    def adv(self, opcode: int, operand: int):
        # print("adv ->", end=" ")
        numerator = self.A
        denominator = 2 ** self.combo(operand)
        result = int(numerator / denominator)

        if opcode == 0:
            self.A = result
        elif opcode == 6:
            self.B = result
        elif opcode == 7:
            self.C = result

    def bxl(self, operand: int):
        # print("bxl ->", end=" ")
        self.B = self.B ^ operand

    def bst(self, operand: int):
        # print("bst ->", end=" ")
        self.B = self.combo(operand) % 8

    def jnz(self, operand: int) -> bool:
        # print("jnz ->", end=" ")
        if self.A != 0:
            self.instruction_pointer = operand
            return False
        return True

    def bxc(self, operand: int):
        # print("bxc ->", end=" ")
        self.B = self.B ^ self.C

    def out(self, operand: int):
        # print("out ->", end=" ")
        return self.combo(operand) % 8

    def __hash__(self) -> int:
        return hash((self.instruction_pointer, self.A, self.B, self.C,))

    def process(self, program: List[int]) -> Generator[int, None, None]:
        history = []

        while True:
            try:
                opcode, operand = program[self.instruction_pointer:self.instruction_pointer + 2]
            except ValueError:
                return
            else:
                update_pointer = True

                match opcode:
                    case 0 | 6 | 7: self.adv(opcode, operand)
                    case 1: self.bxl(operand)
                    case 2: self.bst(operand)
                    case 3:
                        update_pointer = self.jnz(operand)
                    case 4: self.bxc(operand)
                    # out
                    case 5: yield self.out(operand)

                if update_pointer:
                    self.instruction_pointer += 2

                # found an infinite loop
                if self.__hash__() in history:
                    return

                history.append(self.__hash__())


def search(i: int, level: int, program: List[int]) -> Generator[int, None, None]:
    """Attempts to re-create the "program" through the outputs of the computer.
    Really only specific to the actual input for the part.

    Formula ends up being:
        Given A:
            1. B = (A % 8) ^ 1
            2. C = A // 2**B
            3. B = (B ^ C) ^ 4
            4. A = A // 2**3
            5. OUT[B % 8]

    The important bit is step 4, the A transformation. 2**3 == 8, so each iteration in the
    search will reverse this operation, multiplying A by 8. We can always count on A*8 being
    the lowest possible value for that level, so just while loop starting at that position,
    searching for the next possible base. Since the output is B%8, you can go up indefinitely
    starting at A*8.

    The first yield in the generator is the lowest possible A value.

    :return:
    """
    expected = program[-level:]

    j = 0
    while True:
        a = i + j
        c = Computer(a, 0, 0)
        out = list(c.process(program))

        # only ever really care about the initial value
        if out[1:] != expected[1:]:
            break

        if out == expected:
            if expected == program:
                yield a
            yield from search(a*8, level+1, program)

        j += 1


@time_it
def main(data: str) -> int:
    *_, program = PTRN.match(data).groups()
    program = list(map(int, program.split(",")))
    potentials = search(i=0, level=1, program=program)
    return next(potentials)


if __name__ == "__main__":
    # print(main(read_input(input_path(__file__).replace(".txt", "_practice.txt"))))
    # 88645542136664 too low
    # 202972175280682
    print(main(read_input(input_path(__file__))))
