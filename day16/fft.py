from typing import List
from math import ceil

import numpy as np

base_pattern = [0, 1, 0, -1]


def fft(digits: List[int], num_phases: int) -> str:
    for i in range(num_phases):
        digits = apply_phase(digits)
        print(f"Finished phase {i}")
    output = digits_to_number(digits)
    return output


def apply_phase(digits: List[int]) -> List[int]:
    output = []
    np_digits = np.array(digits)
    for i in range(len(digits)):
        pattern = get_pattern(repeat_count=i + 1, pattern_length=len(digits))
        np_pattern = np.array(pattern)
        result = (np_digits * np_pattern).sum()
        output.append(abs(result) % 10)  # keep last digit

    return output


def get_pattern(repeat_count: int, pattern_length: int) -> List[int]:
    output = []
    for i in base_pattern:
        output.extend([i] * repeat_count)

    output = output * (ceil(pattern_length / len(output)) + 1)
    return output[1:pattern_length + 1]


def number_to_digits(number: int) -> List[int]:
    out = []
    for char in str(number):
        out.append(int(char))
    return out


def digits_to_number(digits: List[int]) -> str:
    digits_as_string = list(map(lambda d: str(d), digits))
    number_string = "".join(digits_as_string)
    return number_string
