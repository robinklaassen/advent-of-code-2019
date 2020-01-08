import unittest
import networkx as nx

from day20.parse_input import parse_input, _file_to_grid


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

    def test_parse_input(self):
        graph = parse_input('test_input.txt')
        start_node = (9, 2)
        end_node = (13, 16)
        self.assertEqual(23, nx.shortest_path_length(graph, start_node, end_node))
