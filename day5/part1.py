from typing import List, Tuple

from day5.puzzle_input import PUZZLE_INPUT


def parse_opcode(number: int) -> Tuple[int, Tuple[int, ...]]:
    opcode = number % 100

    parameter_modes = []
    for i in [100, 1000, 10000]:
        parameter_modes.append((number // i) % 10)
    return opcode, tuple(parameter_modes)


assert parse_opcode(1002) == (2, (0, 1, 0))
assert parse_opcode(3) == (3, (0, 0, 0))


def run_program(initial_program_state: List[int], program_input: int) -> Tuple[List[int], int]:
    offset = 0
    program_state = initial_program_state.copy()
    output = None

    while True:
        opcode, parameter_modes = parse_opcode(program_state[offset])
        if opcode == 99:
            break
        if opcode not in [1, 2, 3, 4]:
            raise ValueError(f"Unexpected opcode: {opcode}")

        # Handle opcode
        if opcode in [1, 2]:
            if parameter_modes[2] == 1:
                raise ValueError(f"Write instruction cannot be in immediate mode")
            value1 = program_state[program_state[offset + 1]] if parameter_modes[0] == 0 else program_state[offset + 1]
            value2 = program_state[program_state[offset + 2]] if parameter_modes[1] == 0 else program_state[offset + 2]
            result = value1 + value2 if opcode == 1 else value1 * value2
            program_state[program_state[offset + 3]] = result
        elif opcode == 3:
            program_state[program_state[offset + 1]] = program_input
        elif opcode == 4:
            output = program_state[program_state[offset + 1]]
            print(f"Output: {output}")

        # Increment offset by variable amount
        offset += 4 if opcode in [1, 2] else 2

    return program_state, output


def main():
    run_program(initial_program_state=PUZZLE_INPUT, program_input=1)


if __name__ == "__main__":
    main()
