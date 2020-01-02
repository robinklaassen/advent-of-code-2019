from enum import Enum


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
TURN_LEFT = {
    Direction.NORTH: Direction.WEST,
    Direction.SOUTH: Direction.EAST,
    Direction.WEST: Direction.SOUTH,
    Direction.EAST: Direction.NORTH,
}
TURN_RIGHT = {
    Direction.NORTH: Direction.EAST,
    Direction.SOUTH: Direction.WEST,
    Direction.WEST: Direction.NORTH,
    Direction.EAST: Direction.SOUTH,
}