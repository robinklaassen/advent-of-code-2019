from enum import Enum, auto
from typing import List

from dataclasses import dataclass

from day11.puzzle_input import PAINTING_PROGRAM
from day11.intcode_computer import IntcodeComputer


@dataclass
class Panel:
    x: int
    y: int
    color: bool = False

    def __eq__(self, other: 'Panel'):
        return (self.x == other.x) and (self.y == other.y)


class Direction(Enum):
    NORTH = auto()
    SOUTH = auto()
    EAST = auto()
    WEST = auto()


MOVEMENT_HANDLER = {
    Direction.NORTH: lambda x, y: (x, y+1),
    Direction.SOUTH: lambda x, y: (x, y-1),
    Direction.EAST: lambda x, y: (x+1, y),
    Direction.WEST: lambda x, y: (x-1, y),
}

TURN_LEFT = {
    Direction.NORTH: Direction.WEST,
    Direction.SOUTH: Direction.EAST,
    Direction.EAST: Direction.NORTH,
    Direction.WEST: Direction.SOUTH,
}


TURN_RIGHT = {
    Direction.NORTH: Direction.EAST,
    Direction.SOUTH: Direction.WEST,
    Direction.EAST: Direction.SOUTH,
    Direction.WEST: Direction.NORTH,
}


def paint(starting_color: bool = False) -> List[Panel]:
    robot_x = 0
    robot_y = 0
    robot_direction = Direction.NORTH
    robot_path: List[Panel] = []

    if starting_color:
        robot_path.append(Panel(robot_x, robot_y, True))

    computer = IntcodeComputer(PAINTING_PROGRAM)
    computer.start()

    while not computer.is_halted():
        # Get current panel from list, if it's there
        current_panel = None
        for p in robot_path:
            if p == Panel(robot_x, robot_y):
                current_panel = p
                break

        current_panel_color = current_panel.color if current_panel else False

        # Get computer output values
        computer.pass_input(int(current_panel_color))
        output = computer.read_output()
        assert len(output) == 2
        new_color, turn_direction = output

        # Paint hull
        if current_panel:
            current_panel.color = new_color
        else:
            robot_path.append(Panel(robot_x, robot_y, new_color))

        # Turn
        turn_dict = TURN_RIGHT if turn_direction == 1 else TURN_LEFT
        robot_direction = turn_dict[robot_direction]

        # Move forward
        robot_x, robot_y = MOVEMENT_HANDLER[robot_direction](robot_x, robot_y)

    return robot_path


def main():
    robot_path = paint(starting_color=False)
    print(f"Robot path length: {len(robot_path)}")


if __name__ == "__main__":
    main()
