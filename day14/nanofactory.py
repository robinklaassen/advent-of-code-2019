from collections import deque, Counter
from typing import List

import math
from dataclasses import dataclass

from day14.recipe import Recipe


@dataclass
class Order:
    name: str
    qty: int


class Nanofactory:

    def __init__(self, recipes: List[Recipe]):
        self.recipes = recipes
        self._order_queue = deque()
        self._stock = Counter()

        self._ore_start_count = int(1e10)
        self._stock['ORE'] = self._ore_start_count

        self._sort_recipes()

    def place_order(self, order: Order):
        print(f"An order was placed for {order.qty} {order.name}")
        self._order_queue.append(order)
        self._handle_orders()

    def get_used_ore_count(self) -> int:
        return self._ore_start_count - self._stock['ORE']

    def _sort_recipes(self):
        # TODO
        pass

    def _handle_orders(self):

        while True:

            if len(self._order_queue) == 0:
                break

            order = self._order_queue[-1]
            recipe = next(filter(lambda x: x.results_in(order.name), self.recipes))
            multiplier = math.ceil(order.qty / recipe.results[order.name])

            # Check if this can be made with the current stock, else place orders for items that are short
            can_make = True
            for ingredient_name, ingredient_qty in recipe.ingredients.items():
                amount_short = (ingredient_qty * multiplier) - self._stock[ingredient_name]
                if amount_short > 0:
                    self.place_order(Order(name=ingredient_name, qty=amount_short))
                    can_make = False

            if can_make:
                # Remove the ingredients
                for ingredient_name, ingredient_qty in recipe.ingredients.items():
                    self._stock[ingredient_name] -= (ingredient_qty * multiplier)

                # Add the results
                for result_name, result_qty in recipe.results.items():
                    self._stock[result_name] += (result_qty * multiplier)

                # Remove the order
                self._order_queue.remove(order)
