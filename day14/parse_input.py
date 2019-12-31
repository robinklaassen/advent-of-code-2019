from typing import List

from day14.recipe import Recipe


def parse_input(filename: str) -> List[Recipe]:
    recipes = []
    with open(filename, 'r') as fp:
        for _, line in enumerate(fp):
            recipe = Recipe.from_string(line.rstrip())
            recipes.append(recipe)
    return recipes