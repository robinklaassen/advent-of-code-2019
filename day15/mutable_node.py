from dataclasses import dataclass

from day15.node import State, Node


@dataclass
class MutableNode:
    x: int
    y: int
    state: State

    @staticmethod
    def from_node(node: Node) -> 'MutableNode':
        return MutableNode(x=node.x, y=node.y, state=node.state)
