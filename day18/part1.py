from itertools import permutations
from math import factorial

from day18.parse import parse_input
from day18.util import get_entrance_node, get_keys_blocked_by_door


def main():
    graph = parse_input('puzzle_input.txt')
    keys = [key for node, key in graph.nodes(data='key') if key is not None]
    doors = [door for node, door in graph.nodes(data='door') if door is not None]

    print(f"Graph has {len(keys)} keys and {len(doors)} doors")

    for door in doors:
        blocked_keys = get_keys_blocked_by_door(graph, door)
        print(f"Door {door} blocks keys {blocked_keys}")

    print(f"Total possible permutations of keys: {factorial(len(keys))}")


if __name__ == "__main__":
    main()
