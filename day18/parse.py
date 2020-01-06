import networkx as nx


def parse_input(filename: str) -> nx.Graph:
    graph = nx.Graph()
    with open(filename, 'r') as fp:
        for y, line in enumerate(fp):
            for x, char in enumerate(line.rstrip()):
                if char == '#':
                    continue

                kwargs = {}
                if char == '@':
                    kwargs['entrance'] = True
                elif char.isupper():
                    kwargs['door'] = char.lower()
                elif char.islower():
                    kwargs['key'] = char

                graph.add_node((x, y), **kwargs)

                for other_x, other_y in [(x, y-1), (x-1, y)]:
                    if (other_x, other_y) in graph.nodes:
                        graph.add_edge((other_x, other_y), (x, y))

    return graph
