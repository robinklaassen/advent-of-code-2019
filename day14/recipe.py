from typing import Dict

from dataclasses import dataclass


@dataclass
class Recipe:
    ingredients: Dict[str, int]
    results: Dict[str, int]

    @staticmethod
    def from_string(recipe: str) -> 'Recipe':

        recipe_args = []
        for chemical_string in recipe.split(" => "):
            chemicals = {}
            for chemical in chemical_string.split(", "):
                qty, name = chemical.split(" ")
                chemicals[name] = int(qty)
            recipe_args.append(chemicals)

        return Recipe(*recipe_args)

    def requires(self, name: str) -> bool:
        return True if name in self.ingredients.keys() else False

    def results_in(self, name: str) -> bool:
        return True if name in self.results.keys() else False
