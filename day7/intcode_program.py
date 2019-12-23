import logging
from typing import List, Tuple


_logger = logging.getLogger(__name__)


class IntcodeProgram:

    def __init__(self, program: List[int], max_iterations: int = 1_000_000):
        self.initial_program = program
        self.program = program
        self.max_iterations = max_iterations

    def reset_program(self):
        self.program = self.initial_program.copy()

    def run(self, inputs: List[int]) -> int:
        offset = 0
        inputs = inputs.copy()
        output = None

        for _ in range(self.max_iterations):
            opcode, parameter_modes = self._parse_opcode(self.program[offset])
            if opcode == 99:
                break
            if opcode not in list(range(1, 9)):
                raise ValueError(f"Unexpected opcode: {opcode}")

            # Handle opcode
            if opcode in [1, 2]:  # addition, multiplication
                if parameter_modes[2] == 1:
                    raise ValueError(f"Write instruction cannot be in immediate mode")
                param1 = self._get_parameter(offset + 1, parameter_modes[0])
                param2 = self._get_parameter(offset + 2, parameter_modes[1])
                result = param1 + param2 if opcode == 1 else param1 * param2
                self._write_parameter(offset + 3, result)
                offset += 4
            elif opcode == 3:  # take input and write
                result = inputs.pop(0)  # NOTE: raises IndexError if inputs is empty
                self._write_parameter(offset + 1, result)
                offset += 2
            elif opcode == 4:  # give output
                output = self._get_parameter(offset + 1, parameter_modes[0])
                _logger.debug(f"Program output: {output}")
                offset += 2
            elif opcode in [5, 6]:  # jump if true/false
                param1 = self._get_parameter(offset + 1, parameter_modes[0])
                if (opcode == 5 and param1 != 0) or (opcode == 6 and param1 == 0):
                    # make jump
                    offset = self._get_parameter(offset + 2, parameter_modes[1])
                else:
                    offset += 3
            elif opcode in [7, 8]:  # less than / equals
                param1 = self._get_parameter(offset + 1, parameter_modes[0])
                param2 = self._get_parameter(offset + 2, parameter_modes[1])
                if opcode == 7:
                    result = 1 if param1 < param2 else 0
                else:
                    result = 1 if param1 == param2 else 0
                self._write_parameter(offset + 3, result)
                offset += 4
        else:
            raise Exception(f"Program not halted after {self.max_iterations} iterations")
        return output

    def _parse_opcode(self, number: int) -> Tuple[int, Tuple[int, ...]]:
        opcode = number % 100

        parameter_modes = []
        for i in [100, 1000, 10000]:
            parameter_modes.append((number // i) % 10)
        return opcode, tuple(parameter_modes)

    def _get_parameter(self, pointer: int, mode: int) -> int:
        if mode == 0:
            return self.program[self.program[pointer]]
        elif mode == 1:
            return self.program[pointer]
        else:
            raise ValueError(f"Unexpected parameter mode: {mode}")

    def _write_parameter(self, pointer: int, value: int):
        # Writing is always in positional mode
        self.program[self.program[pointer]] = value
