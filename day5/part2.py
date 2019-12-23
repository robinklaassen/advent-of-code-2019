from typing import List, Tuple

from day5.puzzle_input import PUZZLE_INPUT


MAX_ITERATIONS = int(1e6)


def parse_opcode(number: int) -> Tuple[int, Tuple[int, ...]]:
    opcode = number % 100

    parameter_modes = []
    for i in [100, 1000, 10000]:
        parameter_modes.append((number // i) % 10)
    return opcode, tuple(parameter_modes)


assert parse_opcode(1002) == (2, (0, 1, 0))
assert parse_opcode(3) == (3, (0, 0, 0))


def get_parameter(program_state: List[int], pointer: int, mode: int) -> int:
    if mode == 0:
        return program_state[program_state[pointer]]
    elif mode == 1:
        return program_state[pointer]
    else:
        raise ValueError(f"Unexpected parameter mode: {mode}")


def run_program(initial_program_state: List[int], program_input: int) -> Tuple[List[int], int]:
    offset = 0
    program_state = initial_program_state.copy()
    output = None

    for _ in range(MAX_ITERATIONS):
        opcode, parameter_modes = parse_opcode(program_state[offset])
        if opcode == 99:
            break
        if opcode not in list(range(1, 9)):
            raise ValueError(f"Unexpected opcode: {opcode}")

        # Handle opcode
        if opcode in [1, 2]:  # addition, multiplication
            if parameter_modes[2] == 1:
                raise ValueError(f"Write instruction cannot be in immediate mode")
            param1 = get_parameter(program_state, offset + 1, parameter_modes[0])
            param2 = get_parameter(program_state, offset + 2, parameter_modes[1])
            result = param1 + param2 if opcode == 1 else param1 * param2
            program_state[program_state[offset + 3]] = result
            offset += 4
        elif opcode == 3:  # take input and write
            program_state[program_state[offset + 1]] = program_input
            offset += 2
        elif opcode == 4:  # give output
            # output = program_state[program_state[offset + 1]]
            output = get_parameter(program_state, offset + 1, parameter_modes[0])
            print(f"Output: {output}")
            offset += 2
        elif opcode in [5, 6]:  # jump if true/false
            param1 = get_parameter(program_state, offset + 1, parameter_modes[0])
            if (opcode == 5 and param1 != 0) or (opcode == 6 and param1 == 0):
                offset = get_parameter(program_state, offset + 2, parameter_modes[1])
            else:
                offset += 3
        elif opcode in [7, 8]:  # less than / equals
            param1 = get_parameter(program_state, offset + 1, parameter_modes[0])
            param2 = get_parameter(program_state, offset + 2, parameter_modes[1])
            if opcode == 7:
                result = 1 if param1 < param2 else 0
            else:
                result = 1 if param1 == param2 else 0
            program_state[program_state[offset + 3]] = result
            offset += 4
    else:
        raise Exception(f"Program not halted after {MAX_ITERATIONS} iterations")
    return program_state, output


def main():
    run_program(initial_program_state=PUZZLE_INPUT, program_input=5)


if __name__ == "__main__":
    main()
