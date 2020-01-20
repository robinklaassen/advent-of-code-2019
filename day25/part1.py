from typing import List

from day11.intcode_computer import IntcodeComputer
from day25.puzzle_input import DROID_ASCII_PROGRAM


def print_computer_output(output: List[int]):
    chars = list(map(lambda x: chr(x), output))
    print("".join(chars))


def command_to_computer_input(command: str) -> List[int]:
    result = []
    for c in command:
        result.append(ord(c))
    result.append(10)
    return result


def main():
    computer = IntcodeComputer(DROID_ASCII_PROGRAM)
    computer.start()

    while True:
        output = computer.read_output()
        print_computer_output(output)

        s = input("-->")
        computer_input = command_to_computer_input(s)
        for i in computer_input:
            computer.pass_input(i)


if __name__ == "__main__":
    main()
