from typing import List

from dataclasses import dataclass


def cmp(a, b):
    """Returns 1 if a > b, 0 if a == b and -1 if a < b"""
    return (a > b) - (a < b)


@dataclass
class Moon:
    x: int
    y: int
    z: int
    v_x: int = 0
    v_y: int = 0
    v_z: int = 0

    @property
    def potential_energy(self) -> int:
        return abs(self.x) + abs(self.y) + abs(self.z)

    @property
    def kinetic_energy(self) -> int:
        return abs(self.v_x) + abs(self.v_y) + abs(self.v_z)

    @property
    def total_energy(self) -> int:
        return self.potential_energy * self.kinetic_energy

    def apply_gravity(self, moons: List['Moon']):
        for moon in moons:
            if moon == self:
                continue
            self.v_x += cmp(moon.x, self.x)
            self.v_y += cmp(moon.y, self.y)
            self.v_z += cmp(moon.z, self.z)

    def apply_velocity(self):
        self.x += self.v_x
        self.y += self.v_y
        self.z += self.v_z
