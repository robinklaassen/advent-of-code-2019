from day14.nanofactory import Nanofactory
from day14.parse_input import parse_input


def main():
    recipes = parse_input('puzzle_input.txt')
    factory = Nanofactory(recipes=recipes)

    print(factory._sorted_chemicals)

    # factory.place_order(name='FUEL', qty=1)
    # used_ore = factory.get_used_ore_count()
    # print(f"Used {used_ore} ORE")


if __name__ == "__main__":
    main()
