import numpy as np

from day11.intcode_computer import IntcodeComputer
from day15.direction import Direction, TURN_RIGHT, TURN_LEFT
from day17.part1 import map_output_to_grid
from day17.puzzle_input import ASCII_PROGRAM

POSITION_MODIFIER = {  # Modified from day 15 to support numpy grid (y, x) instead of (x, y)
    Direction.NORTH: lambda y, x: (y - 1, x),
    Direction.SOUTH: lambda y, x: (y + 1, x),
    Direction.WEST: lambda y, x: (y, x - 1),
    Direction.EAST: lambda y, x: (y, x + 1),
}


def get_new_pos(current_pos: np.array, direction: Direction) -> np.array:
    return POSITION_MODIFIER[direction](*current_pos)


def get_tile_value(grid: np.array, pos: np.array):
    y, x = pos
    y_max, x_max = grid.shape
    if y < 0 or y >= y_max or x < 0 or x >= x_max:
        return 0
    else:
        return grid[pos]


def main():
    computer = IntcodeComputer(ASCII_PROGRAM)
    computer.start()
    output = computer.read_output()
    grid = map_output_to_grid(output)
    np_grid = np.array(grid)

    # Find droid
    droid_mask = np.isin(np_grid, [35, 46], invert=True)
    droid_pos = np.where(droid_mask)

    print(f"Initial droid position: {droid_pos}")

    # Determine necessary droid instructions for traversing entire path
    droid_instructions = []
    droid_direction = Direction.NORTH  # determined visually
    forward_step_counter = 0

    for _ in range(1000):

        # Try stepping forward
        forward_tile = get_tile_value(np_grid, get_new_pos(droid_pos, droid_direction))
        if forward_tile == 35:
            droid_pos = get_new_pos(droid_pos, droid_direction)
            forward_step_counter += 1
            print("Droid is stepping forward")
            continue

        # Try turning
        for turn in [TURN_LEFT, TURN_RIGHT]:
            new_direction = turn[droid_direction]
            tile = get_tile_value(np_grid, get_new_pos(droid_pos, new_direction))
            if tile == 35:
                # We have to turn now, so clear the forward steps counter
                droid_instructions.append(forward_step_counter)
                forward_step_counter = 0

                droid_direction = new_direction
                direction_letter = 'L' if turn == TURN_LEFT else 'R'
                droid_instructions.append(direction_letter)
                print(f"Droid is turning {direction_letter}")
                break
        else:
            # Turning didn't work, we must be done
            droid_instructions.append(forward_step_counter)
            print("Droid reached the end")
            break

    print(droid_instructions)


if __name__ == "__main__":
    main()
