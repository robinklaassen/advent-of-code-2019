import itertools

from typing import Tuple

from day7.intcode_program import IntcodeProgram
from day7.puzzle_input import AMPLIFIER_CONTROLLER_SOFTWARE


def run_amplifiers(program: IntcodeProgram, phases: Tuple[int, int, int, int, int]) -> int:
    input_value = 0
    output = 0
    for i in range(5):
        output = program.run([phases[i], input_value])
        # print(f"Output value after amplifier {i}: {output}")
        input_value = output
    return output


def find_max_output(program: IntcodeProgram) -> int:
    attempts = itertools.permutations(range(5), 5)
    outputs = []
    for attempted_phases in attempts:
        outputs.append(run_amplifiers(program, attempted_phases))  # type: ignore
    return max(outputs)


def main():
    assert find_max_output(IntcodeProgram([3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0])) == 43210
    assert find_max_output(IntcodeProgram([3, 23, 3, 24, 1002, 24, 10, 24, 1002, 23, -1, 23,
                                           101, 5, 23, 23, 1, 24, 23, 23, 4, 23, 99, 0, 0])) == 54321
    assert find_max_output(IntcodeProgram([3, 31, 3, 32, 1002, 32, 10, 32, 1001, 31, -2, 31, 1007, 31, 0, 33,
                                           1002, 33, 7, 33, 1, 33, 31, 31, 1, 32, 31, 31, 4, 31, 99, 0, 0, 0])) == 65210

    output = find_max_output(IntcodeProgram(AMPLIFIER_CONTROLLER_SOFTWARE))
    print(f"Submit value: {output}")


if __name__ == "__main__":
    main()
