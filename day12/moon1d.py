from typing import List

from dataclasses import dataclass


def cmp(a, b):
    """Returns 1 if a > b, 0 if a == b and -1 if a < b"""
    return (a > b) - (a < b)


@dataclass
class Moon1d:
    x: int
    v_x: int = 0

    def apply_gravity(self, moons: List['Moon1d']):
        for moon in moons:
            if moon == self:
                continue
            self.v_x += cmp(moon.x, self.x)

    def apply_velocity(self):
        self.x += self.v_x
