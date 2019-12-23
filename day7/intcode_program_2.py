import logging
from enum import Enum, auto
from typing import List, Tuple


_logger = logging.getLogger(__name__)


class ProgramState(Enum):
    READY = auto()
    WAITING_FOR_INPUT = auto()
    HALTED = auto()


class IntcodeProgram2:

    def __init__(self, program: List[int], max_iterations: int = 1_000_000):
        self.initial_program = program
        self.program = program
        self.max_iterations = max_iterations
        self.pointer = 0
        self.state = ProgramState.READY
        self.input_ = None
        self.output = None

    def start(self):
        """Start the program, running it until it halts or input is required"""
        if self.state is not ProgramState.READY:
            raise Exception("Cannot start program, it is not ready")
        ...
        self._run_to_break()

    def pass_input(self, input_: int):
        """Pass an integer to the program as input and continue its execution"""
        if self.state is not ProgramState.WAITING_FOR_INPUT:
            raise Exception("Program is not waiting for input, cannot pass it")
        self.input_ = input_
        self._run_to_break()

    def read_output(self) -> int:
        """Read the last output value of the program"""
        if self.output is None:
            raise Exception("Cannot read program output, there is none")
        return self.output

    def reset(self):
        """Reset the program to its initial state"""
        self.program = self.initial_program.copy()
        self.pointer = 0
        self.state = ProgramState.READY

    def _run_to_break(self):

        for _ in range(self.max_iterations):
            opcode, parameter_modes = self._parse_opcode(self.program[self.pointer])

            # Halt on opcode 99
            if opcode == 99:
                self.state = ProgramState.HALTED
                break

            # Validate opcode
            if opcode not in list(range(1, 9)):
                raise ValueError(f"Unexpected opcode: {opcode}")

            # Handle opcode
            if opcode in [1, 2]:  # addition, multiplication
                if parameter_modes[2] == 1:
                    raise ValueError(f"Write instruction cannot be in immediate mode")
                param1 = self._get_parameter(self.pointer + 1, parameter_modes[0])
                param2 = self._get_parameter(self.pointer + 2, parameter_modes[1])
                result = param1 + param2 if opcode == 1 else param1 * param2
                self._write_parameter(self.pointer + 3, result)
                self.pointer += 4
            elif opcode == 3:  # take input and write
                if self.input_ is None:
                    self.state = ProgramState.WAITING_FOR_INPUT
                    break
                else:
                    self._write_parameter(self.pointer + 1, self.input_)
                    self.input_ = None
                    self.pointer += 2
            elif opcode == 4:  # give output
                self.output = self._get_parameter(self.pointer + 1, parameter_modes[0])
                self.pointer += 2
            elif opcode in [5, 6]:  # jump if true/false
                param1 = self._get_parameter(self.pointer + 1, parameter_modes[0])
                if (opcode == 5 and param1 != 0) or (opcode == 6 and param1 == 0):
                    # make jump
                    self.pointer = self._get_parameter(self.pointer + 2, parameter_modes[1])
                else:
                    self.pointer += 3
            elif opcode in [7, 8]:  # less than / equals
                param1 = self._get_parameter(self.pointer + 1, parameter_modes[0])
                param2 = self._get_parameter(self.pointer + 2, parameter_modes[1])
                if opcode == 7:
                    result = 1 if param1 < param2 else 0
                else:
                    result = 1 if param1 == param2 else 0
                self._write_parameter(self.pointer + 3, result)
                self.pointer += 4
        else:
            raise Exception(f"Program reached {self.max_iterations} iterations without stopping, possible loop")

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
