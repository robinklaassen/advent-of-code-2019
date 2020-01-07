import unittest
import networkx as nx

from day18.parse import parse_input
from day18.util import get_entrance_node, get_keys_blocked_by_door


class Day18TestSuite(unittest.TestCase):

    def test_parse_input(self):
        graph = parse_input('test_input.txt')
        self.assertEqual(7, graph.number_of_nodes())
        self.assertTrue(nx.is_connected(graph))
        self.assertEqual((5, 1), get_entrance_node(graph))
        self.assertEqual(2, nx.shortest_path_length(graph, (4, 1), (6, 1)))

    def test_keys_blocked_by_door(self):
        graph = parse_input('test_input.txt')
        self.assertEqual(['b'], get_keys_blocked_by_door(graph, 'a'))
