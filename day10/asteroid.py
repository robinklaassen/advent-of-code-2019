import math
from fractions import Fraction
from typing import Tuple, List

from dataclasses import dataclass


ANGLE_ACCURACY = 6


@dataclass
class Asteroid:
    x: int
    y: int

    @property
    def distance(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2)

    @property
    def relative_angle_in_radians(self) -> float:
        if self.x == 0 and self.y > 0:
            angle = math.pi / 2
        elif self.x == 0 and self.y < 0:
            angle = 3 * math.pi / 2
        else:
            angle = math.atan2(self.y, self.x)

        # correct for the fact that 'up' is -y
        angle = angle + math.pi / 2

        # reduce angle to 0..2pi (0 inclusive, 2pi exclusive)
        while angle < 0:
            angle += 2 * math.pi
        while angle >= 2 * math.pi:
            angle -= 2 * math.pi

        return round(angle, ndigits=ANGLE_ACCURACY)

    def get_linear_params(self, other: 'Asteroid') -> Tuple[Fraction, Fraction]:
        m = Fraction(other.y - self.y, other.x - self.x)
        b = self.y - m * self.x
        return m, b

    def get_visible_asteroids_count(self, others: List['Asteroid']) -> int:
        total_count = 0

        others = [a for a in others if a != self]
        vertical_others = [a for a in others if a.x == self.x]
        left_side_others = [a for a in others if a.x < self.x]
        right_side_others = [a for a in others if a.x > self.x]

        aboves = [a for a in vertical_others if a.y > self.y]
        belows = [a for a in vertical_others if a.y < self.y]

        if aboves:
            total_count += 1
        if belows:
            total_count += 1

        for others in [left_side_others, right_side_others]:
            linear_params = map(lambda a: self.get_linear_params(a), others)
            total_count += len(set(linear_params))

        return total_count

    def __eq__(self, other: 'Asteroid'):
        return (self.x == other.x) and (self.y == other.y)


# test get_linear_params
as1 = Asteroid(1, 1)
as2 = Asteroid(2, 3)
assert as1.get_linear_params(as2) == (2, -1)
assert as2.get_linear_params(as1) == (2, -1)

# test get_visible_asteroids_count
asteroids = []
for x in range(3):
    for y in range(3):
        asteroids.append(Asteroid(x, y))

assert asteroids[4].get_visible_asteroids_count(asteroids) == 8
