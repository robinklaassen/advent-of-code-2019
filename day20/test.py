import unittest
import networkx as nx

from day20.parse_input import parse_input, _file_to_grid
from day20.part1 import get_node_by_unique_mark
from day20.part2 import make_recursed_graph


class Day20TestSuite(unittest.TestCase):

    def test_file_to_grid(self):
        grid = _file_to_grid('test_input.txt')
        self.assertEqual(list, type(grid))

    def test_parse_input_without_donut_connections(self):
        graph = parse_input('test_input.txt', with_donut_connections=False)
        start_node = (9, 2)
        end_node = (13, 16)
        self.assertEqual(26, nx.shortest_path_length(graph, start_node, end_node))

        marks = [mark for node, mark in graph.nodes(data='mark') if mark is not None]
        self.assertEqual(8, len(marks))

        nodes_with_data = [(node, ddict) for node, ddict in graph.nodes(data=True) if ddict != dict()]
        print(nodes_with_data)

    def test_parse_input(self):
        graph = parse_input('test_input.txt')
        start_node = (9, 2)
        end_node = (13, 16)
        self.assertEqual(23, nx.shortest_path_length(graph, start_node, end_node))

    def test_recursion(self):
        graph = parse_input('recursed_test_input.txt')
        recursed_graph = make_recursed_graph(graph, 10)
        start_node = get_node_by_unique_mark(graph, 'AA')
        end_node = get_node_by_unique_mark(graph, 'ZZ')
        self.assertEqual(396, nx.shortest_path_length(recursed_graph, start_node, end_node))
