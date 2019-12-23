import networkx as nx
from day6.part1 import construct_graph


def main():
    graph = construct_graph('puzzle_input.txt')
    length = nx.shortest_path_length(graph, "YOU", "SAN")
    print(f"Submit value: {length - 2}")


if __name__ == "__main__":
    main()
