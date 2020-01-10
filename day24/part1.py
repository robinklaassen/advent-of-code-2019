import numpy as np

from day24.parse_input import parse_input, print_grid


def step(grid: np.array) -> np.array:
    new_grid = np.zeros(grid.shape, dtype=np.bool)
    for y, row in enumerate(grid):
        for x, bug in enumerate(row):
            num_adj_bugs = get_num_adj_bugs(grid, x, y)
            # print(f"Number of adjacent bugs for (x, y) = {(x, y)}: {num_adj_bugs}")
            if (bug and num_adj_bugs == 1) or (not bug and num_adj_bugs in [1, 2]):
                new_grid[y][x] = 1
    return new_grid


def get_num_adj_bugs(grid: np.array, x: int, y: int) -> int:
    y_size, x_size = grid.shape
    counter = 0
    if x != 0 and grid[y][x - 1]:  # left
        counter += 1
    if x != x_size - 1 and grid[y][x + 1]:  # right
        counter += 1
    if y != 0 and grid[y - 1][x]:  # up
        counter += 1
    if y != y_size - 1 and grid[y + 1][x]:  # down
        counter += 1

    return counter


def calculate_biodiversity_rating(grid: np.array) -> int:
    idx = np.argwhere(grid.flatten())
    values = list(map(lambda x: 2 ** x, idx))
    return int(sum(values))


def main():
    grid = parse_input('puzzle_input.txt')
    grid_history = [grid]

    print("Initial grid:")
    print_grid(grid)

    for i in range(1_000_000):
        grid = step(grid)

        print(f"After {i + 1} minutes:")
        print_grid(grid)

        for earlier_grid in grid_history:
            if np.array_equal(grid, earlier_grid):
                print("Grid matches earlier variant, stopping")
                print(f"The biodiversity rating is: {calculate_biodiversity_rating(grid)}")
                break
        else:
            grid_history.append(grid)
            continue

        break


if __name__ == "__main__":
    main()
