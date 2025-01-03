from typing import List, Callable

from utils import time_it, read_input, input_path


operators = [
    lambda l, r: l + r,
    lambda l, r: l * r,
    lambda l, r: int(str(l) + str(r)),
]


def solve(
        test_value: int,
        calibration_equations: List[int],
        calibration_accumulations: List[int],
        ops: List[Callable[[int, int], int]]
) -> int:
    """Implement a BFS against all remaining calibration equations.

    Per layer, pull from calibration equations as the "right" side of any equation.
    For each calibration accumulation (left side), apply each operator to the left
    and right.
        If any equal the test value, you're done.
        If any exceed the test value, exclude it from remaining searches.
        If the result is less than the test value, recurse.
    """
    try:
        right = calibration_equations[0]
    # you went through all possibles without solving
    except IndexError:
        return 0
    else:
        new_accumulations = []
        for acc in sorted(calibration_accumulations, reverse=True):
            for op in ops:
                result = op(acc, right)
                if result == test_value:
                    return test_value
                if result < test_value:
                    new_accumulations.append(result)

        return solve(test_value, calibration_equations[1:], new_accumulations, ops=ops)


@time_it
def main(data: str) -> int:
    total = 0

    for line in data.splitlines():
        test_value, rest = line.split(":")
        start, *calibration_equations = map(int, rest.strip().split(" "))

        result = solve(
            int(test_value),
            calibration_equations=calibration_equations,
            calibration_accumulations=[start],
            ops=operators[:2]
        )

        if result == 0:
            result = solve(
                int(test_value),
                calibration_equations=calibration_equations,
                calibration_accumulations=[start],
                ops=operators[:3]
            )

        total += result

    return total


if __name__ == "__main__":
    print(main(read_input(input_path(__file__).replace(".txt", "_practice.txt"))))
    print(main(read_input(input_path(__file__))))
