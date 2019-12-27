from typing import Tuple, List
from math import inf


def parse_input(filename: str) -> Tuple[Tuple[int, int], List[Tuple[int, int]]]:
    line_length = None
    column_length = 0
    asteroids = []
    with open(filename) as fp:
        for y, line in enumerate(fp):
            column_length += 1

            line = line.rstrip()
            if not line_length:
                line_length = len(line)
            assert len(line) == line_length

            for x, char in enumerate(line):
                if char == '#':
                    asteroids.append((x, y))

    return (line_length, column_length), asteroids


def test_parser():
    grid_size, asteroids = parse_input('test_input.txt')
    assert grid_size == (3, 3)
    assert asteroids == [(2, 0), (0, 1), (2, 1), (0, 2), (1, 2)]


def get_linear_function_parameters(base: Tuple[int, int], target: Tuple[int, int]) -> Tuple[float, float]:
    if base == target:
        raise Exception("Base and target must be different points")
    if target[0] == base[0]:
        a = inf if target[1] > base[1] else -inf
        b = base[1]
    else:
        a = (target[1] - base[1]) / (target[0] - base[0])
        b = base[1] - a * base[0]
    return a, b


def test_get_linear_parameters():
    base = (2, 2)
    target = (4, 4)
    a, b = get_linear_function_parameters(base, target)
    assert a == 1.0
    assert b == 0.0

    base = (3, 1)
    target = (6, 3)
    a, b = get_linear_function_parameters(base, target)
    assert a == (2 / 3)
    assert b == -1.0


def count_visible_asteroids(base: Tuple[int, int], asteroids: List[Tuple[int, int]]) -> int:
    target_asteroids = [a for a in asteroids if a != base]
    params = map(lambda ta: get_linear_function_parameters(base=base, target=ta), target_asteroids)
    return len(set(params))


def test_count():
    base = (0, 0)
    asteroids = [(0, 0), (1, 0), (2, 0)]
    assert count_visible_asteroids(base=base, asteroids=asteroids) == 1

    asteroids = [(0, 0), (1, 1), (2, 2), (3, 2), (6, 4)]
    assert count_visible_asteroids(base=base, asteroids=asteroids) == 2

    asteroids = [(0, 0), (0, 1), (0, 2)]
    assert count_visible_asteroids(base=base, asteroids=asteroids) == 1


def find_highest_count(asteroids: List[Tuple[int, int]]) -> Tuple[Tuple[int, int], int]:
    counts = list(map(lambda a: count_visible_asteroids(base=a, asteroids=asteroids), asteroids))
    target_index = counts.index(max(counts))
    return asteroids[target_index], counts[target_index]


def test_find_highest():
    grid_size, asteroids = parse_input('test_input_2.txt')
    location, count = find_highest_count(asteroids)
    assert location == (5, 8)
    assert count == 33


def main():
    test_parser()
    test_get_linear_parameters()
    test_count()
    test_find_highest()

    grid_size, asteroids = parse_input('puzzle_input.txt')
    location, count = find_highest_count(asteroids)
    print(f"Submit value: {count}")


if __name__ == "__main__":
    main()
