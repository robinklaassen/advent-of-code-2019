from day12.moon import Moon
from day12.puzzle_input import INITIAL_MOONS_STATE

from copy import deepcopy


def main():
    moons = deepcopy(INITIAL_MOONS_STATE)
    t = 0
    while True:
        t += 1
        [moon.apply_gravity(moons) for moon in moons]
        [moon.apply_velocity() for moon in moons]
        if moons == INITIAL_MOONS_STATE:
            print(f"Initial state reached after {t} steps")
            break


if __name__ == "__main__":
    main()
