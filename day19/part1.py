from typing import List

from day11.intcode_computer import IntcodeComputer
from day19.puzzle_input import DRONE_PROGRAM

PRINT_MAP = {
    0: '.',
    1: '#',
}


def print_grid(grid: List[List[int]]):
    for row in grid:
        chars = list(map(lambda x: PRINT_MAP[x], row))
        line = "".join(chars)
        print(line)


def main():
    program = DRONE_PROGRAM.copy()
    computer = IntcodeComputer(program)

    counter = 0
    grid = []
    for y in range(50):
        row = []
        for x in range(50):
            computer.reset()
            computer.start()
            computer.pass_input(x)
            computer.pass_input(y)
            output = computer.read_output()
            assert len(output) == 1
            row.append(output[0])
            if output[0] == 1:
                counter += 1
        grid.append(row)

    print_grid(grid)
    print(f"Number of points affected by tractor beam: {counter}")


if __name__ == "__main__":
    main()
