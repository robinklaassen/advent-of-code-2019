from typing import Set, List, Tuple, Dict, Optional

from day15.direction import Direction, POSITION_MODIFIER
from day15.node import Node, State

PRINT_CHARACTER_FOR_STATE = {
    State.UNKNOWN: ' ',
    State.EMPTY: '.',
    State.WALL: '#',
    State.TARGET: 'T'
}


class ExplorableGrid:
    """
    An x,y grid of variable size, increasing from top-left.
    Initializes with an unknown state and a single agent at the center.
    """

    def __init__(self):
        self.agent_position = (0, 0)
        self.nodes: Set[Node] = set()
        self.nodes.add(Node(x=0, y=0, state=State.EMPTY, value=None))

    def add_node_in_direction(self, direction: Direction, state: State, value: Optional[int] = None):
        x, y = self._get_modified_position(direction)
        self.nodes.add(Node(x, y, state, value))

    def move_agent(self, direction: Direction):
        self.agent_position = self._get_modified_position(direction)

    def get_adjacent_nodes(self) -> Dict[Direction, Node]:
        output = {}
        for direction in list(Direction):
            output[direction] = self._get_node(position=self._get_modified_position(direction))
        return output

    def transform_coordinates_to_topleft_origin(self, position: Tuple[int, int]) -> Tuple[int, int]:
        x, y = position
        x_values = [n.x for n in self.nodes]
        y_values = [n.y for n in self.nodes]
        x_min, y_min = min(x_values), min(y_values)

        return x - x_min, y - y_min

    def _get_modified_position(self, direction: Direction) -> Tuple[int, int]:
        return POSITION_MODIFIER[direction](*self.agent_position)

    def _get_node(self, position: Tuple[int, int]) -> Node:
        x, y = position
        nodes = [n for n in self.nodes if n.x == x and n.y == y]
        if len(nodes) == 0:
            return Node(x=x, y=y, state=State.UNKNOWN, value=None)
        elif len(nodes) == 1:
            return nodes[0]
        else:
            raise Exception(f"Found {len(nodes)} nodes in set for position {(x, y)}, expected max 1")

    def _nodes_to_list(self) -> List[List[Node]]:
        x_values = [n.x for n in self.nodes]
        y_values = [n.y for n in self.nodes]
        x_min, x_max, y_min, y_max = min(x_values), max(x_values), min(y_values), max(y_values)

        output = []
        for y in range(y_min, y_max + 1):
            line = []
            for x in range(x_min, x_max + 1):
                node = self._get_node((x, y))
                line.append(node)
            output.append(line)

        return output

    def print(self):
        for row in self._nodes_to_list():
            line = ""
            for node in row:
                if (node.x, node.y) == self.agent_position:
                    char = 'X'
                elif node.x == 0 and node.y == 0:
                    char = 'O'
                else:
                    char = PRINT_CHARACTER_FOR_STATE[node.state]
                line += char
            print(line)
