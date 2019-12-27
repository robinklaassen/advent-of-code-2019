from typing import List

from day10.asteroid import Asteroid


def parse_input(filename: str) -> List[Asteroid]:
    line_length = None
    asteroids = []
    with open(filename) as fp:
        for y, line in enumerate(fp):
            line = line.rstrip()
            if not line_length:
                line_length = len(line)
            assert len(line) == line_length

            for x, char in enumerate(line):
                if char == '#':
                    asteroids.append(Asteroid(x, y))

    return asteroids


asteroids = parse_input('test_input.txt')
expected_coords = [(2, 0), (0, 1), (2, 1), (0, 2), (1, 2)]
assert asteroids == [Asteroid(x, y) for x, y in expected_coords]
