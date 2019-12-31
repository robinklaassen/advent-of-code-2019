from day14.nanofactory import Nanofactory
from day14.parse_input import parse_input


def main():
    recipes = parse_input('puzzle_input.txt')
    factory = Nanofactory(recipes=recipes)

    # print(factory._sorted_chemicals)

    factory.place_order(name='FUEL', qty=1)
    factory.start()

    print(f"Open orders: {factory._orders}")
    print(f"Stockpile: {factory._stockpile}")

    print(f"Submit value: {factory.get_ore_amount()}")


if __name__ == "__main__":
    main()
