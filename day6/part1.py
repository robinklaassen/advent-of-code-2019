import networkx as nx


def construct_graph(filename: str) -> nx.DiGraph:
    graph = nx.DiGraph()
    with open(filename, 'r') as fp:
        for count, line in enumerate(fp):
            items = line.rstrip().split(")")
            orbitee = items[0]  # the one being orbited
            orbiter = items[1]  # the one doing the orbiting

            # Add nodes to graph
            for space_object in [orbitee, orbiter]:
                if space_object not in graph:
                    graph.add_node(space_object)

            # Add edge to graph
            graph.add_edge(orbiter, orbitee)

    return graph


def get_orbits_for_object(graph: nx.Graph, space_object: str) -> int:
    ...


def get_total_orbits(graph: nx.Graph) -> int:
    ...


def test_case():
    print("---TEST CASE---")
    test_graph = construct_graph('test_input.txt')
    print(f"Space objects in test case: {test_graph.nodes}")
    assert len(test_graph.nodes) == 12
    assert get_orbits_for_object(test_graph, "COM") == 0
    assert get_orbits_for_object(test_graph, "D") == 3
    assert get_orbits_for_object(test_graph, "L") == 7
    assert get_total_orbits(test_graph) == 42


def main():
    test_case()


if __name__ == "__main__":
    main()
