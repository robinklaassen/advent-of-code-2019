from typing import Tuple

import networkx as nx

from day20.parse_input import parse_input


def get_node_by_unique_mark(graph: nx.Graph, unique_mark: str) -> Tuple[int, int]:
    nodes = [node for node, mark in graph.nodes(data='mark') if mark == unique_mark]
    assert len(nodes) == 1
    return nodes[0]


def main():
    graph = parse_input('puzzle_input.txt')

    start_node = get_node_by_unique_mark(graph, 'AA')
    end_node = get_node_by_unique_mark(graph, 'ZZ')

    path_length = nx.shortest_path_length(graph, start_node, end_node)
    print(f"Submit value: {path_length}")


if __name__ == "__main__":
    main()
