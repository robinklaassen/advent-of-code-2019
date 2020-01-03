from typing import List, Tuple

from day11.intcode_computer import IntcodeComputer
from day17.puzzle_input import ASCII_PROGRAM


def map_output_to_grid(output: List[int]) -> List[List[int]]:
    grid = []
    row = []
    for i in output[0:-1]:  # output ends on 2x 10
        if i == 10:
            grid.append(row)
            row = []
        else:
            row.append(i)
    return grid


def get_intersections(grid: List[List[int]]) -> List[Tuple[int, int]]:
    intersections = []
    for y, row in enumerate(grid):
        if y == 0 or y == len(grid) - 1:
            continue
        for x, i in enumerate(row):
            if x == 0 or x == len(row) - 1 or i != 35:
                continue
            if is_intersection(grid, x, y):
                print(f"Found intersection at: {(x, y)}")
                intersections.append((x, y))
    return intersections


def is_intersection(grid: List[List[int]], x: int, y: int) -> bool:
    # Code for a scaffold is 35
    if grid[y - 1][x] != 35:
        return False
    elif grid[y + 1][x] != 35:
        return False
    elif grid[y][x - 1] != 35:
        return False
    elif grid[y][x + 1] != 35:
        return False
    return True


def main():
    computer = IntcodeComputer(ASCII_PROGRAM)
    computer.start()
    output = computer.read_output()
    print(f"Length of output: {len(output)}")
    print(f"Last 5 ints: {output[-1:-6:-1]}")

    output_chars = list(map(lambda x: chr(x), output))
    print("".join(output_chars))

    grid = map_output_to_grid(output)
    print(f"Grid size is {len(grid)} rows by {len(grid[0])} columns")
    intersections = get_intersections(grid)

    alignment_params = [x * y for x, y in intersections]
    print(f"Submit value: {sum(alignment_params)}")


if __name__ == "__main__":
    main()
