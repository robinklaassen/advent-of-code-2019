from day1.part1 import get_input_masses, get_fuel_cost


total_fuel_cost = 0
for input_mass in get_input_masses('input.txt'):
    module_fuel_cost = 0

    added_fuel = get_fuel_cost(input_mass)
    while True:
        module_fuel_cost += added_fuel
        added_fuel = get_fuel_cost(added_fuel)
        if added_fuel <= 0:
            break

    print(f"Module input mass {input_mass} requires total fuel: {module_fuel_cost}")
    total_fuel_cost += module_fuel_cost

print(f"Total fuel cost: {total_fuel_cost}")
