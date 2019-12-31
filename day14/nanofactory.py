from collections import Counter
from typing import List

import math
import networkx as nx

from day14.recipe import Recipe


class Nanofactory:

    def __init__(self, recipes: List[Recipe]):
        self.recipes = recipes
        self._orders = Counter()
        self._stock = Counter()

        self._ore_start_count = int(1e10)  # should simulate infinite amount, increase if causing errors
        self._stock['ORE'] = self._ore_start_count

        self._sorted_chemicals = self._sort_chemicals()

    def place_order(self, name: str, qty: int):
        print(f"An order was placed for {qty} {name}")
        self._orders[name] += qty
        self._handle_orders()

    def get_used_ore_count(self) -> int:
        return self._ore_start_count - self._stock['ORE']

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

    def _can_make(self, recipe: Recipe, multiplier: int = 1) -> bool:
        can_make = True
        for ing, qty in recipe.ingredients.items():
            if self._stock[ing] < qty * multiplier:
                can_make = False
                break
        return can_make

    def _process_recipe(self, recipe: Recipe, multiplier: int = 1):
        ...

    def _handle_orders(self):

        while any(self._orders.values()):

            chemical_to_make = next(filter(lambda name: self._orders[name] > 0, self._sorted_chemicals))
            recipe = next(filter(lambda x: x.results_in(chemical_to_make), self.recipes))
            multiplier = math.ceil(self._orders[chemical_to_make] / recipe.results[chemical_to_make])

            # Check if this can be made with the current stock, else place orders for items that are short
            can_make = True
            for ingredient_name, ingredient_qty in recipe.ingredients.items():
                amount_short = (ingredient_qty * multiplier) - self._stock[ingredient_name]
                if amount_short > 0:
                    self.place_order(name=ingredient_name, qty=amount_short)
                    can_make = False

            if can_make:
                self._process_recipe(recipe, multiplier)

        # while True:
        #
        #     if len(self._order_queue) == 0:
        #         break
        #
        #     order = self._order_queue[-1]
        #     recipe = next(filter(lambda x: x.results_in(order.name), self.recipes))
        #     multiplier = math.ceil(order.qty / recipe.results[order.name])
        #
        #     # Check if this can be made with the current stock, else place orders for items that are short
        #     can_make = True
        #     for ingredient_name, ingredient_qty in recipe.ingredients.items():
        #         amount_short = (ingredient_qty * multiplier) - self._stock[ingredient_name]
        #         if amount_short > 0:
        #             self.place_order(Order(name=ingredient_name, qty=amount_short))
        #             can_make = False
        #
        #     if can_make:
        #         # Remove the ingredients
        #         for ingredient_name, ingredient_qty in recipe.ingredients.items():
        #             self._stock[ingredient_name] -= (ingredient_qty * multiplier)
        #
        #         # Add the results
        #         for result_name, result_qty in recipe.results.items():
        #             self._stock[result_name] += (result_qty * multiplier)
        #
        #         # Remove the order
        #         self._order_queue.remove(order)
