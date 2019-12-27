from typing import Tuple, List

from day10.parser import parse_input
from day10.asteroid import Asteroid


def find_highest_count(asteroids: List[Asteroid]) -> Tuple[Asteroid, int]:
    counts = list(map(lambda a: a.get_visible_asteroids_count(asteroids), asteroids))
    target_index = counts.index(max(counts))
    return asteroids[target_index], counts[target_index]


def test_find_highest():
    asteroids = parse_input('test_input_2.txt')
    target_asteroid, count = find_highest_count(asteroids)
    assert target_asteroid == Asteroid(5, 8)
    assert count == 33


def main():
    test_find_highest()

    asteroids = parse_input('puzzle_input.txt')
    target_asteroid, count = find_highest_count(asteroids)
    print(f"Target asteroid is {target_asteroid} with view count {count}")


if __name__ == "__main__":
    main()
