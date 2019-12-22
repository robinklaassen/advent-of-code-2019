import numpy as np

from typing import List

PUZZLE_INPUT_RANGE = range(130254, 678275 + 1)


def number_to_digits(number: int) -> List[int]:
    out = []
    for char in str(number):
        out.append(int(char))
    return out


assert number_to_digits(12) == [1, 2]


def check_adjacent(digits: List[int]) -> bool:
    return True if 0 in np.diff(digits) else False


def check_never_decrease(digits: List[int]) -> bool:
    for i in range(len(digits) - 1):
        if digits[i+1] < digits[i]:
            return False
    return True


def check_number(number: int) -> bool:
    digits = number_to_digits(number)
    return True if check_adjacent(digits) and check_never_decrease(digits) else False


assert check_number(111111)
assert not check_number(223450)
assert not check_number(123789)


def main():
    valid_passwords_counter = 0
    for number in PUZZLE_INPUT_RANGE:
        if check_number(number):
            print(number)
            valid_passwords_counter += 1

    print(f"Total number of valid passwords: {valid_passwords_counter}")


if __name__ == "__main__":
    main()

