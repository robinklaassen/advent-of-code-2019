import logging
from enum import Enum, auto
from typing import List, Tuple


_logger = logging.getLogger(__name__)


class ComputerState(Enum):
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


NUMBER_OF_INPUT_PARAMS_PER_OPCODE = {
    Opcode.ADDITION: 2,
    Opcode.MULTIPLICATION: 2,
    Opcode.INPUT: 0,
    Opcode.OUTPUT: 1,
    Opcode.JUMP_IF_TRUE: 2,
    Opcode.JUMP_IF_FALSE: 2,
    Opcode.LESS_THAN: 2,
    Opcode.EQUALS: 2,
    Opcode.ADJUST_RELATIVE_BASE: 1,
    Opcode.HALT: 0,
}


class IntcodeComputer:

    def __init__(self, program: List[int], max_iterations: int = 1_000_000, memory_size: int = 10240):
        self.initial_memory = [0] * memory_size
        self.initial_memory[:len(program)] = program
        self.memory = self.initial_memory.copy()
        self.max_iterations = max_iterations
        self.pointer = 0
        self.relative_base = 0
        self.state = ComputerState.READY
        self.input_ = None
        self.output = []

    def start(self):
        """Start the program, running it until it halts or input is required"""
        if self.state is not ComputerState.READY:
            raise Exception("Cannot start program, it is not ready")
        ...
        self._run_to_break()

    def pass_input(self, input_: int):
        """Pass an integer to the program as input and continue its execution"""
        if self.state is not ComputerState.WAITING_FOR_INPUT:
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
        self.memory = self.initial_memory.copy()
        self.pointer = 0
        self.relative_base = 0
        self.state = ComputerState.READY

    def is_halted(self):
        return self.state == ComputerState.HALTED

    def _run_to_break(self):
        for _ in range(self.max_iterations):
            opcode, parameter_modes = self._parse_opcode(self.memory[self.pointer])

            input_params = tuple((self._get_parameter(self.pointer + i + 1, parameter_modes[i])
                                  for i in range(NUMBER_OF_INPUT_PARAMS_PER_OPCODE[opcode])))

            handlers = {
                Opcode.ADDITION: self._handle_addition,
                Opcode.MULTIPLICATION: self._handle_multiplication,
                Opcode.INPUT: self._handle_input,
                Opcode.OUTPUT: self._handle_output,
                Opcode.JUMP_IF_TRUE: self._handle_jump_if_true,
                Opcode.JUMP_IF_FALSE: self._handle_jump_if_false,
                Opcode.LESS_THAN: self._handle_less_than,
                Opcode.EQUALS: self._handle_equals,
                Opcode.ADJUST_RELATIVE_BASE: self._handle_adjust_relative_base,
                Opcode.HALT: self._handle_halt,
            }

            result = handlers[opcode](input_params, parameter_modes)
            if result is True:
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
            return self.memory[self.memory[pointer]]
        elif mode == ParameterMode.IMMEDIATE:
            return self.memory[pointer]
        elif mode == ParameterMode.RELATIVE:
            return self.memory[self.memory[pointer] + self.relative_base]

    def _write_parameter(self, pointer: int, mode: ParameterMode, value: int):
        if mode == ParameterMode.POSITIONAL:
            self.memory[self.memory[pointer]] = value
        elif mode == ParameterMode.IMMEDIATE:
            raise ValueError("Writing is never in immediate mode")
        elif mode == ParameterMode.RELATIVE:
            self.memory[self.memory[pointer] + self.relative_base] = value

    def _handle_addition(self, input_params: Tuple[int, ...], parameter_modes: Tuple[ParameterMode, ...]):
        value = input_params[0] + input_params[1]
        self._write_parameter(self.pointer + 3, parameter_modes[2], value)
        self.pointer += 4

    def _handle_multiplication(self, input_params: Tuple[int, ...], parameter_modes: Tuple[ParameterMode, ...]):
        value = input_params[0] * input_params[1]
        self._write_parameter(self.pointer + 3, parameter_modes[2], value)
        self.pointer += 4

    def _handle_input(self, _: Tuple[int, ...], parameter_modes: Tuple[ParameterMode, ...]):
        if self.input_ is None:
            self.state = ComputerState.WAITING_FOR_INPUT
            return True
        else:
            self._write_parameter(self.pointer + 1, parameter_modes[0], self.input_)
            self.input_ = None
            self.pointer += 2

    def _handle_output(self, input_params: Tuple[int, ...], __: Tuple[ParameterMode, ...]):
        self.output.append(input_params[0])
        self.pointer += 2

    def _handle_jump_if_true(self, input_params: Tuple[int, ...], _: Tuple[ParameterMode, ...]):
        if input_params[0] != 0:
            self.pointer = input_params[1]
        else:
            self.pointer += 3

    def _handle_jump_if_false(self, input_params: Tuple[int, ...], _: Tuple[ParameterMode, ...]):
        if input_params[0] == 0:
            self.pointer = input_params[1]
        else:
            self.pointer += 3

    def _handle_less_than(self, input_params: Tuple[int, ...], parameter_modes: Tuple[ParameterMode, ...]):
        value = 1 if input_params[0] < input_params[1] else 0
        self._write_parameter(self.pointer + 3, parameter_modes[2], value)
        self.pointer += 4

    def _handle_equals(self, input_params: Tuple[int, ...], parameter_modes: Tuple[ParameterMode, ...]):
        value = 1 if input_params[0] == input_params[1] else 0
        self._write_parameter(self.pointer + 3, parameter_modes[2], value)
        self.pointer += 4

    def _handle_adjust_relative_base(self, input_params: Tuple[int, ...], __: Tuple[ParameterMode, ...]):
        self.relative_base += input_params[0]
        self.pointer += 2

    def _handle_halt(self, _: Tuple[int, ...], __: Tuple[ParameterMode, ...]):
        self.state = ComputerState.HALTED
        return True
