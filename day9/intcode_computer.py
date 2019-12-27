import logging
from enum import Enum, auto
from typing import List, Tuple


_logger = logging.getLogger(__name__)


class ProgramState(Enum):
    READY = auto()
    WAITING_FOR_INPUT = auto()
    HALTED = auto()


class Opcode(Enum):
    ADDITION = 1
    MULTIPLICATION = 2
    INPUT = 3
    OUTPUT = 4
    JUMP_IF_TRUE = 5
    JUMP_IF_FALSE = 6
    LESS_THAN = 7
    EQUALS = 8
    ADJUST_RELATIVE_BASE = 9
    HALT = 99


class ParameterMode(Enum):
    POSITIONAL = 0
    IMMEDIATE = 1
    RELATIVE = 2


class IntcodeComputer:

    def __init__(self, program: List[int], max_iterations: int = 1_000_000, memory_size: int = 1024):
        memory = [0] * memory_size
        memory[:len(program)] = program
        self.initial_program = memory.copy()
        self.program = memory.copy()
        self.max_iterations = max_iterations
        self.pointer = 0
        self.relative_base = 0
        self.state = ProgramState.READY
        self.input_ = None
        self.output = []

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

    def read_output(self) -> List[int]:
        """Read the output value(s) of the program and resets the output list"""
        output = self.output.copy()
        self.output = []
        return output

    def reset(self):
        """Reset the program to its initial state"""
        self.program = self.initial_program.copy()
        self.pointer = 0
        self.relative_base = 0
        self.state = ProgramState.READY

    def _run_to_break(self):

        for _ in range(self.max_iterations):
            opcode, parameter_modes = self._parse_opcode(self.program[self.pointer])

            if opcode in [Opcode.ADDITION, Opcode.MULTIPLICATION]:
                param1 = self._get_parameter(self.pointer + 1, parameter_modes[0])
                param2 = self._get_parameter(self.pointer + 2, parameter_modes[1])
                result = param1 + param2 if opcode == Opcode.ADDITION else param1 * param2
                self._write_parameter(self.pointer + 3, parameter_modes[2], result)
                self.pointer += 4
            elif opcode == Opcode.INPUT:
                if self.input_ is None:
                    self.state = ProgramState.WAITING_FOR_INPUT
                    break
                else:
                    self._write_parameter(self.pointer + 1, parameter_modes[0], self.input_)
                    self.input_ = None
                    self.pointer += 2
            elif opcode == Opcode.OUTPUT:
                value = self._get_parameter(self.pointer + 1, parameter_modes[0])
                self.output.append(value)
                self.pointer += 2
            elif opcode in [Opcode.JUMP_IF_TRUE, Opcode.JUMP_IF_FALSE]:
                param1 = self._get_parameter(self.pointer + 1, parameter_modes[0])
                if (opcode == Opcode.JUMP_IF_TRUE and param1 != 0) or (opcode == Opcode.JUMP_IF_FALSE and param1 == 0):
                    self.pointer = self._get_parameter(self.pointer + 2, parameter_modes[1])
                else:
                    self.pointer += 3
            elif opcode in [Opcode.LESS_THAN, Opcode.EQUALS]:
                param1 = self._get_parameter(self.pointer + 1, parameter_modes[0])
                param2 = self._get_parameter(self.pointer + 2, parameter_modes[1])
                if opcode == Opcode.LESS_THAN:
                    result = 1 if param1 < param2 else 0
                else:
                    result = 1 if param1 == param2 else 0
                self._write_parameter(self.pointer + 3, parameter_modes[2], result)
                self.pointer += 4
            elif opcode == Opcode.ADJUST_RELATIVE_BASE:
                param = self._get_parameter(self.pointer + 1, parameter_modes[0])
                self.relative_base += param
                self.pointer += 2
            elif opcode == Opcode.HALT:
                self.state = ProgramState.HALTED
                break
        else:
            raise Exception(f"Program reached {self.max_iterations} iterations without stopping, possible loop")

    def _parse_opcode(self, number: int) -> Tuple[Opcode, Tuple[ParameterMode, ...]]:
        opcode = Opcode(number % 100)

        parameter_modes = []
        for i in [100, 1000, 10000]:
            parameter_mode = ParameterMode((number // i) % 10)
            parameter_modes.append(parameter_mode)
        return opcode, tuple(parameter_modes)

    def _get_parameter(self, pointer: int, mode: ParameterMode) -> int:
        if mode == ParameterMode.POSITIONAL:
            return self.program[self.program[pointer]]
        elif mode == ParameterMode.IMMEDIATE:
            return self.program[pointer]
        elif mode == ParameterMode.RELATIVE:
            return self.program[self.program[pointer] + self.relative_base]

    def _write_parameter(self, pointer: int, mode: ParameterMode, value: int):
        if mode == ParameterMode.POSITIONAL:
            self.program[self.program[pointer]] = value
        elif mode == ParameterMode.IMMEDIATE:
            raise ValueError("Writing is never in immediate mode")
        elif mode == ParameterMode.RELATIVE:
            self.program[self.program[pointer] + self.relative_base] = value
