import random
from enum import Enum, auto
from typing import Tuple, Set

from dataclasses import dataclass

from day11.intcode_computer import IntcodeComputer
from day15.puzzle_input import REPAIR_DROID_PROGRAM

DROID_ITERATIONS = 100000


class Direction(Enum):
    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4


POSITION_MODIFIER = {
    Direction.NORTH: lambda x, y: (x, y - 1),
    Direction.SOUTH: lambda x, y: (x, y + 1),
    Direction.WEST: lambda x, y: (x - 1, y),
    Direction.EAST: lambda x, y: (x + 1, y),
}


class State(Enum):
    EMPTY = auto()
    WALL = auto()
    OXYGEN_SYSTEM = auto()


@dataclass(frozen=True)  # immutable
class PositionInfo:
    x: int
    y: int
    state: State


def new_pos(x: int, y: int, direction: Direction) -> Tuple[int, int]:
    return POSITION_MODIFIER[direction](x, y)


def print_map(infos: Set[PositionInfo]):
    x_list = [p.x for p in infos]
    y_list = [p.y for p in infos]
    x_min, x_max, y_min, y_max = min(x_list), max(x_list), min(y_list), max(y_list)

    for y in range(y_min, y_max + 1):
        line = ""
        for x in range(x_min, x_max + 1):
            try:
                pi = next(filter(lambda p: p.x == x and p.y == y, infos))
                if pi.state == State.EMPTY:
                    char = '.'
                elif pi.state == State.WALL:
                    char = '#'
                elif pi.state == State.OXYGEN_SYSTEM:
                    char = 'O'
            except StopIteration:
                char = ' '
            line += char
        print(line)




def main():
    computer = IntcodeComputer(REPAIR_DROID_PROGRAM)
    computer.start()

    droid_x = 0
    droid_y = 0

    infos = set()
    infos.add(PositionInfo(0, 0, State.EMPTY))

    for _ in range(DROID_ITERATIONS):
        direction: Direction = random.choice(list(Direction))  # randomize! we can find an algorithm later
        computer.pass_input(direction.value)
        output = computer.read_output()
        assert len(output) == 1
        output = output[0]

        new_x, new_y = new_pos(droid_x, droid_y, direction)

        if output == 0:  # hit a wall, didn't move
            infos.add(PositionInfo(new_x, new_y, State.WALL))
        elif output == 1:  # moved successfully
            infos.add(PositionInfo(new_x, new_y, State.EMPTY))
            droid_x, droid_y = new_x, new_y
        elif output == 2:  # moved and found oxygen system
            infos.add(PositionInfo(new_x, new_y, State.OXYGEN_SYSTEM))
            droid_x, droid_y = new_x, new_y

    print(f"Length of info set: {len(infos)}")
    print_map(infos)


if __name__ == "__main__":
    main()
