import numpy as np
import re

from typing import List

from day4.part1 import (
    PUZZLE_INPUT_RANGE,
    number_to_digits,
    check_never_decrease,
)


def check_adjacent_not_part_of_larger_group(digits: List[int]):
    first_diff = np.diff(digits)
    if 0 not in first_diff:
        # No adjacent digits found
        return False

    # Okay, let's fall back on some brute forcing :')
    number_string = "".join(map(lambda x: str(x), digits))

    for target in ['00', '11', '22', '33', '44', '55', '66', '77', '88', '99']:
        occurrences = [m.start() for m in re.finditer(f'(?={target})', number_string)]
        num_occurrences = len(occurrences)
        if num_occurrences == 1:
            return True

    return False


def check_number(number: int) -> bool:
    digits = number_to_digits(number)
    return True if check_adjacent_not_part_of_larger_group(digits) and check_never_decrease(digits) else False


assert check_number(112233)
assert not check_number(123444)
assert check_number(111122)


def main():
    valid_passwords_counter = 0
    for number in PUZZLE_INPUT_RANGE:
        if check_number(number):
            print(number)
            valid_passwords_counter += 1

    print(f"Total number of valid passwords: {valid_passwords_counter}")


if __name__ == "__main__":
    main()
