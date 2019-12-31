from collections import Counter
from typing import List

import math
import networkx as nx

from day14.recipe import Recipe


class Nanofactory:

    def __init__(self, recipes: List[Recipe]):
        self.recipes = recipes
        self._orders = Counter()
        self._stockpile = Counter()

        self._sorted_chemicals = self._sort_chemicals()

    def place_order(self, name: str, qty: int):
        print(f"An order was placed for {qty} {name}")
        self._orders[name] += qty

    def start(self):
        self._handle_orders()

    def get_ore_amount(self) -> int:
        return self._orders['ORE']

    def reset(self):
        self._orders = Counter()
        self._stockpile = Counter()

    def _sort_chemicals(self) -> List[str]:
        """Topological sorting of the chemicals in all recipes, returns a sorted list with end result first"""
        graph = nx.DiGraph()
        for recipe in self.recipes:

            graph.add_nodes_from(recipe.ingredients.keys())
            graph.add_nodes_from(recipe.results.keys())

            for ing in recipe.ingredients.keys():
                for res in recipe.results.keys():
                    graph.add_edge(ing, res)

        return list(nx.topological_sort(graph))[::-1]

    def _handle_orders(self):
        while True:
            name = next(filter(lambda c: self._orders[c] > 0, self._sorted_chemicals))
            if name == 'ORE':
                break
            qty = self._orders[name]
            self._handle_single_order(name, qty)

    def _handle_single_order(self, name: str, qty: int):
        recipe = next(filter(lambda x: x.results_in(name), self.recipes))
        multiplier = math.ceil(qty / recipe.results[name])
        self._process_recipe(recipe, multiplier)

    def _process_recipe(self, recipe: Recipe, multiplier: int = 1):
        for res, qty in recipe.results.items():
            amount_made = qty * multiplier
            amount_ordered = self._orders[res]
            excess = amount_made - amount_ordered
            self._stockpile[res] += excess
            self._orders[res] = 0

        for ing, qty in recipe.ingredients.items():
            amount_to_make = qty * multiplier
            available_in_stockpile = self._stockpile[ing]
            amount_to_order = amount_to_make - available_in_stockpile
            self.place_order(ing, amount_to_order)
            self._stockpile[ing] = 0
