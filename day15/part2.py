from day11.intcode_computer import IntcodeComputer
from day15.explorable_grid import ExplorableGrid
from day15.mutable_node import MutableNode
from day15.node import State
from day15.part1 import explore_by_left_wall
from day15.puzzle_input import REPAIR_DROID_PROGRAM


def main():
    # Set up initial grid from part 1
    computer = IntcodeComputer(REPAIR_DROID_PROGRAM)
    computer.start()

    grid = ExplorableGrid()

    explore_by_left_wall(computer, grid)

    mutable_nodes = list(map(lambda n: MutableNode.from_node(n), grid.nodes))

    # Find target and make it oxygenated
    for node in mutable_nodes:
        if node.state == State.TARGET:
            node.state = State.OXYGENATED

    for t in range(10000):
        oxygenated_nodes = [n for n in mutable_nodes if n.state == State.OXYGENATED]
        oxygenation_counter = 0

        for on in oxygenated_nodes:
            for x, y in [(on.x+1, on.y), (on.x-1, on.y), (on.x, on.y-1), (on.x, on.y+1)]:
                tn = next(filter(lambda mn: mn.x == x and mn.y == y, mutable_nodes), None)
                if tn and tn.state == State.EMPTY:
                    tn.state = State.OXYGENATED
                    oxygenation_counter += 1

        if oxygenation_counter == 0:
            break

    print(t)


if __name__ == "__main__":
    main()
