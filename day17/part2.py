from typing import List

# Found sequence from 'droid_path.py'
from day11.intcode_computer import IntcodeComputer
from day17.puzzle_input import ASCII_PROGRAM

total_sequence = ['L', 12, 'L', 8, 'R', 12, 'L', 10, 'L', 8, 'L', 12, 'R', 12, 'L', 12, 'L', 8, 'R', 12, 'R', 12,
                  'L', 8, 'L', 10, 'L', 12, 'L', 8, 'R', 12, 'L', 12, 'L', 8, 'R', 12, 'R', 12, 'L', 8, 'L', 10,
                  'L', 10, 'L', 8, 'L', 12, 'R', 12, 'R', 12, 'L', 8, 'L', 10, 'L', 10, 'L', 8, 'L', 12, 'R', 12]

A = ['L', 12, 'L', 8, 'R', 12]

B = ['L', 10, 'L', 8, 'L', 12, 'R', 12]

C = ['R', 12, 'L', 8, 'L', 10]

main_sequence = ['A', 'B', 'A', 'C', 'A', 'A', 'C', 'B', 'C', 'B']


def sequence_to_ascii(seq: list) -> List[int]:
    output = []
    for i in seq:
        for c in str(i):
            output.append(ord(c))
        output.append(ord(','))
    output[-1] = 10  # replace last comma with newline
    return output


def main():
    assert total_sequence == A + B + A + C + A + A + C + B + C + B

    program = ASCII_PROGRAM.copy()
    program[0] = 2
    computer = IntcodeComputer(program)
    computer.start()

    # Pass the functions
    for seq in [main_sequence, A, B, C]:
        input_ = sequence_to_ascii(seq)
        for i in input_:
            computer.pass_input(i)

    # Say no to the video feed
    computer.pass_input(ord('n'))
    computer.pass_input(10)

    # Read output
    output = computer.read_output()
    print(f"Submit value: {output[-1]}")


if __name__ == "__main__":
    main()
