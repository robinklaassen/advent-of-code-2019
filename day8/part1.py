from typing import List

from day8.puzzle_input import PUZZLE_INPUT


def get_slices(string: str, size: int) -> List[str]:
    offset = 0
    output: List[str] = []
    while True:
        slice_ = string[offset:offset+size]
        if len(slice_) == 0:
            break
        output.append(slice_)
        offset += size

    return output


def main():
    slice_list = get_slices(PUZZLE_INPUT, 25 * 6)
    zero_counts = list(map(lambda s: s.count("0"), slice_list))
    print(zero_counts)
    target_index = zero_counts.index(min(zero_counts))
    target_string = slice_list[target_index]
    output = target_string.count("1") * target_string.count("2")
    print(f"Submit value: {output}")


if __name__ == "__main__":
    main()
