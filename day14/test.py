import unittest

from day14.part1 import parse_input


class TestSuite(unittest.TestCase):

    def test_parse_input(self):
        recipes = parse_input('test_input_small.txt')
        self.assertEqual(6, len(recipes))
        self.assertTrue(recipes[0].requires('ORE'))
        self.assertTrue(recipes[0].results_in('A'))
