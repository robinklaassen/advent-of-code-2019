import numpy as np


def parse_input(filename: str, grid_size: int = 5) -> np.array:
    grid = np.zeros((grid_size, grid_size), dtype=np.bool)
    with open(filename, 'r') as fp:
        for y, line in enumerate(fp):
            for x, char in enumerate(line.rstrip()):
                if char == '#':
                    grid[y][x] = 1

    return grid


def print_grid(grid: np.array):
    for row in grid:
        chars = list(map(lambda x: '#' if x else '.', row))
        line = "".join(chars)
        print(line)
