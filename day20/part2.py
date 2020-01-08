from typing import Tuple

import networkx as nx

from day20.parse_input import parse_input
from day20.part1 import get_node_by_unique_mark


def make_recursed_graph(graph: nx.Graph, num_recursions: int = 1) -> nx.Graph:
    original_graph = graph.copy()
    new_graph = original_graph.copy()

    unique_marks = set([mark for node, mark in original_graph.nodes(data='mark') if mark is not None])
    unique_marks.remove('AA')
    unique_marks.remove('ZZ')

    for i in range(1, num_recursions + 1):
        added_graph = original_graph.copy()
        added_graph = nx.relabel_nodes(added_graph, lambda n: (n[0] + 1000 * i, n[1] + 1000 * i))

        connected_nodes = []
        for mark in unique_marks:
            node1 = _get_node_by_typed_mark(new_graph, mark, 'inner')
            node2 = _get_node_by_typed_mark(added_graph, mark, 'outer')
            connected_nodes.append((node1, node2))

        new_graph.update(added_graph)

        for node1, node2 in connected_nodes:
            new_graph.add_edge(node1, node2)
            del new_graph.nodes[node1]['mark']
            del new_graph.nodes[node1]['mark_type']
            del new_graph.nodes[node2]['mark']
            del new_graph.nodes[node2]['mark_type']

        print(f"Recursion level {i} added")

    return new_graph


def _get_node_by_typed_mark(graph: nx.Graph, target_mark: str, target_mark_type: str) -> Tuple[int, int]:
    results = [node for node, ddict in graph.nodes(data=True) if
               ddict.get('mark', None) == target_mark and ddict.get('mark_type', None) == target_mark_type]
    assert len(results) == 1
    return results[0]


def main():
    graph = parse_input('puzzle_input.txt', with_donut_connections=False)
    start_node = get_node_by_unique_mark(graph, 'AA')
    end_node = get_node_by_unique_mark(graph, 'ZZ')

    graph = make_recursed_graph(graph, 50)

    path_length = nx.shortest_path_length(graph, start_node, end_node)
    print(f"Submit value: {path_length}")


if __name__ == "__main__":
    main()
