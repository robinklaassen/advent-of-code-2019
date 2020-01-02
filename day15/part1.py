import random

from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

from day11.intcode_computer import IntcodeComputer
from day15.direction import Direction, TURN_RIGHT, TURN_LEFT
from day15.explorable_grid import ExplorableGrid
from day15.node import State
from day15.puzzle_input import REPAIR_DROID_PROGRAM

MAX_ITERATIONS = 10000

COMPUTER_OUTPUT_TO_STATE_MAP = {
    0: State.WALL,
    1: State.EMPTY,
    2: State.TARGET,
}


def main():
    computer = IntcodeComputer(REPAIR_DROID_PROGRAM)
    computer.start()

    grid = ExplorableGrid()

    explore_by_left_wall(computer, grid)

    grid.print()

    find_path_length_to_target(grid)


def explore_by_left_wall(computer: IntcodeComputer, grid: ExplorableGrid):

    agent_facing = Direction.NORTH

    for t in range(MAX_ITERATIONS):
        computer.pass_input(agent_facing.value)
        output = computer.read_output()
        assert len(output) == 1
        output = output[0]

        found_state = COMPUTER_OUTPUT_TO_STATE_MAP[output]
        grid.add_node_in_direction(agent_facing, found_state)
        if found_state is State.WALL:
            agent_facing = TURN_RIGHT[agent_facing]
        else:
            grid.move_agent(agent_facing)
            agent_facing = TURN_LEFT[agent_facing]

        if t > 5 and grid.agent_position == (0, 0):
            break


def find_path_length_to_target(explorable_grid: ExplorableGrid):
    node_matrix = explorable_grid._nodes_to_list()
    grid_matrix = []
    for node_row in node_matrix:
        grid_row = list(map(lambda n: 0 if n.state == State.WALL else 1, node_row))
        grid_matrix.append(grid_row)

    pathfinding_grid = Grid(matrix=grid_matrix)

    target_node = [n for n in explorable_grid.nodes if n.state == State.TARGET]
    assert len(target_node) == 1
    target_node = target_node[0]

    start_coords = explorable_grid.transform_coordinates_to_topleft_origin((0, 0))
    target_coords = explorable_grid.transform_coordinates_to_topleft_origin((target_node.x, target_node.y))

    start = pathfinding_grid.node(*start_coords)
    end = pathfinding_grid.node(*target_coords)

    finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
    path, runs = finder.find_path(start, end, pathfinding_grid)

    print(pathfinding_grid.grid_str(path=path, start=start, end=end))

    print(f"Number of steps required: {len(path) - 1}")


def explore_randomly(computer, grid):
    step_counter = 0
    for _ in range(MAX_ITERATIONS):  # TODO when does this loop end?
        adj_nodes = grid.get_adjacent_nodes()

        # Pick a direction and put into computer
        # If there are unknowns, pick one of them. If there are no unknowns, pick an empty.
        unknown_nodes = {k: v for k, v in adj_nodes.items() if v.state == State.UNKNOWN}
        if len(unknown_nodes) > 0:
            direction = random.choice(list(unknown_nodes.keys()))
        else:
            moveable_nodes = {k: v for k, v in adj_nodes.items() if v.state != State.WALL}
            direction = random.choice(list(moveable_nodes.keys()))

        computer.pass_input(direction.value)
        output = computer.read_output()
        assert len(output) == 1
        output = output[0]

        # Handle output
        found_state = COMPUTER_OUTPUT_TO_STATE_MAP[output]
        value = step_counter if found_state is not State.WALL else None
        grid.add_node_in_direction(direction, found_state, value)
        if found_state is not State.WALL:
            grid.move_agent(direction)


if __name__ == "__main__":
    main()
