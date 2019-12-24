from typing import List

from day8.part1 import get_slices
from day8.puzzle_input import PUZZLE_INPUT


def main():
    slices = get_slices(PUZZLE_INPUT, 25 * 6)
    reverse_slices = slices.copy()
    reverse_slices.reverse()
    output: List[str] = ['x'] * 25 * 6
    for slice_ in reverse_slices:  # start from bottom layer
        for ix, char in enumerate(slice_):
            if char != '2':
                output[ix] = char

    output_string = "".join(output)

    formatted_string = output_string.replace('0', ' ')

    for i in range(6):
        # assuming terminal is monospaced
        print(formatted_string[25*i:25*(i+1)])


if __name__ == "__main__":
    main()
