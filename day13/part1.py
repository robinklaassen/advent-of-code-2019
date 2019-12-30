from day11.intcode_computer import IntcodeComputer
from day13.puzzle_input import GAME_PROGRAM

import numpy as np


ARCADE_CHARS = {
    0: ' ',
    1: 'X',
    2: '#',
    3: '=',
    4: 'O',
}


def print_grid(grid: np.ndarray):
    for y in range(grid.shape[0]):
        chars = [ARCADE_CHARS[x] for x in grid[y, :]]
        print("".join(chars))


def main():
    computer = IntcodeComputer(GAME_PROGRAM, memory_size=10240)
    computer.start()
    output = computer.read_output()
    print(f"Length of game output list: {len(output)}")
    x_size = max(output[::3]) + 1
    y_size = max(output[1::3]) + 1
    print(f"Game grid is {x_size} squares wide and {y_size} squares high")
    grid = np.zeros((y_size, x_size), dtype=np.int8)  # NOTE: numpy is col, row (y, x)

    for triplet in np.array_split(output, len(output) / 3):
        grid[triplet[1], triplet[0]] = triplet[2]

    print_grid(grid)

    print(f"Total number of blocks ('2' values): {np.count_nonzero(grid == 2)}")


if __name__ == "__main__":
    main()
