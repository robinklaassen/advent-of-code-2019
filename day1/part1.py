from typing import List

import math


def get_fuel_cost(mass: int) -> int:
    return int(math.floor(mass / 3) - 2)


def get_input_masses(file_path: str) -> List[int]:
    input_masses: List[int] = []
    with open(file_path) as fp:
        for count, line in enumerate(fp):
            input_masses.append(int(line))
    return input_masses


assert get_fuel_cost(1969) == 654

total_fuel = 0
for mass in get_input_masses('input.txt'):
    fuel_cost = get_fuel_cost(mass)
    print(f"Mass {mass} requires fuel: {fuel_cost}")
    total_fuel += fuel_cost

print(f"Total fuel cost: {total_fuel}")
