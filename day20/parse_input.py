from typing import List

import networkx as nx


def parse_input(filename: str, with_donut_connections: bool = True) -> nx.Graph:
    graph = nx.Graph()
    grid = _file_to_grid(filename)

    # First, put all empty nodes in graph and connect them
    for y in range(len(grid)):
        row = grid[y]
        for x in range(len(row)):
            char = row[x]
            if char != '.':
                continue

            graph.add_node((x, y))
            for other_x, other_y in [(x, y - 1), (x - 1, y)]:
                if (other_x, other_y) in graph.nodes:
                    graph.add_edge((other_x, other_y), (x, y))

    # Then, mark all nodes with letters if present
    for x, y in graph.nodes:
        # Get surrounding nodes
        for ax, ay in [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]:
            char = grid[ay][ax]
            if char.isupper():
                break
        else:
            continue

        # print(f"{(x, y)} has a mark at {(ax, ay)}")
        if ax == x + 1:  # right
            char2 = grid[y][x+2]
            mark = char + char2
        elif ax == x - 1:  # left
            char2 = grid[y][x-2]
            mark = char2 + char
        elif ay == y + 1:  # down
            char2 = grid[y+2][x]
            mark = char + char2
        elif ay == y - 1:  # up
            char2 = grid[y-2][x]
            mark = char2 + char
        else:
            raise Exception

        graph.nodes[(x, y)]['mark'] = mark

    # If required, connect the marked nodes in the graph
    if with_donut_connections:
        marks = [mark for node, mark in graph.nodes(data='mark') if mark is not None]
        unique_marks = set(marks)
        for target_mark in unique_marks:
            marked_nodes = [node for node, mark in graph.nodes(data='mark') if mark == target_mark]
            if len(marked_nodes) != 2:
                continue
            graph.add_edge(*marked_nodes)

    return graph


def _file_to_grid(filename: str) -> List[List[str]]:
    grid = []
    with open(filename, 'r') as fp:
        for line in fp.readlines():
            row = []
            for char in line.rstrip('\n'):
                row.append(char)
            grid.append(row)
    return grid
