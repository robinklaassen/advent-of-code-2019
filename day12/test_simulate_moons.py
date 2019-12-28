import unittest

from day12.moon import Moon
from day12.part1 import simulate_moons


class SimulateMoonsTestSuite(unittest.TestCase):

    def test_simulate_moons(self):
        moons = [
            Moon(-1, 0, 2),
            Moon(2, -10, -7),
            Moon(4, -8, 8),
            Moon(3, 5, -1),
        ]

        simulated_moons = simulate_moons(moons, 10)
        self.assertEqual(179, sum([m.total_energy for m in simulated_moons]))
