from typing import List

from utils import time_it, read_input, input_path


operators = [
    lambda l, r: l + r,
    lambda l, r: l * r,
    lambda l, r: int(str(l) + str(r)),
]


def solve(
        test_value: int,
        calibration_equations: List[int],
        calibration_accumulations: List[int]
) -> int:
    """Implement a BFS against all remaining calibration equations.

    Per layer, pull from calibration equations as the "right" side of any equation.
    For each calibration accumulation (left side), apply each operator to the left
    and right.
        If any equal the test value, you're done.
        If any exceed the test value, exclude it from remaining searches.
        If the result is less than the test value, recurse.
    """
    # you went through all possibles without solving
    if not calibration_equations:
        return 0

    right = calibration_equations.pop(0)

    new_accumulations = []
    for acc in calibration_accumulations:
        for op in operators:
            result = op(acc, right)
            if result == test_value:
                return test_value
            if result < test_value:
                new_accumulations.append(result)

    return solve(test_value, calibration_equations, new_accumulations)


@time_it
def main(data: str) -> int:
    total = 0

    for line in data.splitlines():
        test_value, rest = line.split(":")
        calibration_equations = list(map(int, rest.strip().split(" ")))

        start = calibration_equations.pop(0)

        total += solve(
            int(test_value),
            calibration_equations=calibration_equations,
            calibration_accumulations=[start]
        )

    return total


if __name__ == "__main__":
    print(main(read_input(input_path(__file__).replace(".txt", "_practice.txt"))))
    print(main(read_input(input_path(__file__))))
