from day14.nanofactory import Nanofactory
from day14.parse_input import parse_input


def main():

    one_trillion = 1000000000000

    recipes = parse_input('puzzle_input.txt')
    factory = Nanofactory(recipes)

    fuel_amount = int(2e6)

    increments = [10 ** i for i in range(6, -1, -1)]

    for increment in increments:
        for _ in range(9):
            factory.reset()
            factory.place_order('FUEL', fuel_amount + increment)
            factory.start()
            ore_amount = factory.get_ore_amount()
            if ore_amount <= one_trillion:
                fuel_amount += increment
            else:
                break

    print(f"You can make {fuel_amount} FUEL")


if __name__ == "__main__":
    main()
