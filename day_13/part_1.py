import math
import re

from utils import time_it, read_input, input_path


BUTTON_A_PTRN = re.compile(r'Button A: X\+(\d+), Y\+(\d+)')
BUTTON_B_PTRN = re.compile(r'Button B: X\+(\d+), Y\+(\d+)')
PRIZE_PTRN = re.compile(r'Prize: X=(\d+), Y=(\d+)')


@time_it
def main(data: str) -> int:
    total = 0

    for (a, b, p) in zip(
        BUTTON_A_PTRN.findall(data),
        BUTTON_B_PTRN.findall(data),
        PRIZE_PTRN.findall(data)
    ):
        ax, ay = list(map(int, a))
        bx, by = list(map(int, b))
        px, py = list(map(int, p))

        # system of equations to try and solve for n and m
        """
        1: n(ax) + m(bx) = px
        2: n(ay) + m(by) = py
        
        2 ->:
        3: n = (py - m(by)) / ay
        
        1 ->:
        4: ((py - m(by)) / ay)(ax) + m(bx) = px
        5: (ax(py - m(by)) / ay) + m(bx) = px
        6. ax(py - m(by)) + m(bx)(ay) = px(ay)
        7. ax(py) - m(by)(ax) + m(bx)(ay) = px(ay)
        8. m(bx)(ay) - m(by)(ax) = px(ay) - ax(py)
        9. m = (px*ay - ax*py) / (bx*ay - by*ax)
        
        Sub back into 3 and solve
        """
        m = (px*ay - ax*py) / (bx*ay - by*ax)
        n = (py - m*by) / ay

        # if either m and n are decimals.. Fail
        if not (m.is_integer() and n.is_integer()):
            continue

        # if either m or n are greater than 100.. Fail
        if m > 100 or n > 100:
            continue

        tokens = n*3 + m
        total += tokens
        # print(a, b, p)
        # print(m, n, tokens)

    return total


if __name__ == "__main__":
    print(main(read_input(input_path(__file__).replace(".txt", "_practice.txt"))))
    print(main(read_input(input_path(__file__))))
