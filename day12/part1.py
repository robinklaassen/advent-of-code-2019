from typing import List

from day12.moon import Moon
from day12.puzzle_input import INITIAL_MOONS_STATE


def simulate_moons(moons: List[Moon], steps: int = 100) -> List[Moon]:
    moons = moons.copy()
    for _ in range(steps):
        [moon.apply_gravity(moons) for moon in moons]
        [moon.apply_velocity() for moon in moons]
    return moons


def main():
    simulated_moons = simulate_moons(INITIAL_MOONS_STATE, 1000)
    total_energy = sum([m.total_energy for m in simulated_moons])
    print(f"Total energy of all moons combined after 1000 steps: {total_energy}")


if __name__ == "__main__":
    main()
