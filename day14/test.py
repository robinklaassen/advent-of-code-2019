import unittest

from day14.nanofactory import Nanofactory
from day14.parse_input import parse_input
from day14.recipe import Recipe


class TestSuite(unittest.TestCase):

    def test_parse_input(self):
        recipes = parse_input('test_input_small.txt')
        self.assertEqual(6, len(recipes))
        self.assertTrue(recipes[0].requires('ORE'))
        self.assertTrue(recipes[0].results_in('A'))

    def test_sort_chemicals(self):
        recipes = parse_input('test_input_small.txt')
        factory = Nanofactory(recipes)
        sorted_chemicals = factory._sort_chemicals()
        self.assertEqual(['FUEL', 'E', 'D', 'C', 'A', 'B', 'ORE'], sorted_chemicals)

    def test_can_make(self):
        recipe = Recipe(ingredients={'A': 25}, results={'B': 1})
        factory = Nanofactory(recipes=[recipe])
        self.assertFalse(factory._can_make(recipe))

        factory._stock['A'] += 50
        self.assertTrue(factory._can_make(recipe))
        self.assertFalse(factory._can_make(recipe, 10))

    def test_handle_orders(self):
        factory = Nanofactory([])
        factory._handle_orders()
