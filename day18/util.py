from typing import Tuple, List

import networkx as nx


def get_entrance_node(graph: nx.Graph) -> Tuple[int, int]:
    nodes = [n for n, entrance in graph.nodes(data='entrance') if entrance is True]
    assert len(nodes) == 1
    return nodes[0]


def get_keys_blocked_by_door(graph: nx.Graph, door_key: chr) -> List[chr]:
    subgraph = graph.subgraph([n for n, door in graph.nodes(data='door') if door != door_key]).copy()
    assert nx.number_connected_components(subgraph) == 2
    separated_graphs = [subgraph.subgraph(c).copy() for c in nx.connected_components(subgraph)]

    # Get the separated graph wich does NOT contain the entrance node
    entrance_node = get_entrance_node(graph)
    target_graph = next(filter(lambda g: entrance_node not in g.nodes, separated_graphs))

    # Return all the keys in this target graph
    output = [key for n, key in target_graph.nodes(data='key') if key is not None]

    return output
