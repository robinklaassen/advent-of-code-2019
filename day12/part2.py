from day12.moon1d import Moon1d

from math import gcd
from copy import deepcopy


STARTING_COORDINATES = [
    (-6, -5, -8),
    (0, -3, -13),
    (-15, 10, -11),
    (-3, -8, 3),
]


def lcm(x, y):
    return x * y // gcd(x, y)


def main():

    transposed_coordinates = list(map(list, zip(*STARTING_COORDINATES)))
    output = []

    for i in range(3):
        initial_moons = [Moon1d(p) for p in transposed_coordinates[i]]
        moons = deepcopy(initial_moons)

        t = 0
        while True:
            t += 1
            [moon.apply_gravity(moons) for moon in moons]
            [moon.apply_velocity() for moon in moons]
            if moons == initial_moons:
                print(f"For axis {i}, initial state reached after {t} steps")
                output.append(t)
                break

    print(f"Submit value: {lcm(lcm(output[0], output[1]), output[2])}")


if __name__ == "__main__":
    main()
