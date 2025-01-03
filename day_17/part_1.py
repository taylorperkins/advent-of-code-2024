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

    def adv(self, opcode: int, operand: int):
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
        self.B = self.B ^ operand

    def bst(self, operand: int):
        self.B = self.combo(operand) % 8

    def jnz(self, operand: int) -> bool:
        if self.A != 0:
            self.instruction_pointer = operand
            return False
        return True

    def bxc(self, operand: int):
        self.B = self.B ^ self.C

    def out(self, operand: int):
        return self.combo(operand) % 8

    def process(self, program: List[int]) -> Generator[int, None, None]:
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


@time_it
def main(data: str) -> str:
    A, B, C, program = PTRN.match(data).groups()
    program = list(map(int, program.split(",")))

    computer = Computer(int(A), int(B), int(C))

    out = ",".join(map(str, computer.process(program)))

    return out


if __name__ == "__main__":
    print(main(read_input(input_path(__file__).replace(".txt", "_practice.txt"))))
    print(main(read_input(input_path(__file__))))
