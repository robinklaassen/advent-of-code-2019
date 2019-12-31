from typing import List

from day14.nanofactory import Nanofactory, Order
from day14.recipe import Recipe


def parse_input(filename: str) -> List[Recipe]:
    recipes = []
    with open(filename, 'r') as fp:
        for _, line in enumerate(fp):
            recipe = Recipe.from_string(line.rstrip())
            recipes.append(recipe)
    return recipes


def main():
    recipes = parse_input('test_input_small.txt')
    factory = Nanofactory(recipes=recipes)
    factory.place_order(Order(name='FUEL', qty=1))
    used_ore = factory.get_used_ore_count()
    print(f"Used {used_ore} ORE")


if __name__ == "__main__":
    main()
