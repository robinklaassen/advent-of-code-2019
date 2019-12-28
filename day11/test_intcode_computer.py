import unittest

from day11.intcode_computer import IntcodeComputer, Opcode, ParameterMode


class IntcodeProgramTestSuite(unittest.TestCase):

    def setUp(self) -> None:
        self.larger_program = IntcodeComputer([3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31,
                                               1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104,
                                               999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99])

    def test_parse_opcode(self):
        empty_program = IntcodeComputer(program=[])
        self.assertEqual(
            (Opcode.MULTIPLICATION, (ParameterMode.POSITIONAL, ParameterMode.IMMEDIATE, ParameterMode.POSITIONAL)),
            empty_program._parse_opcode(1002))
        self.assertEqual((Opcode.INPUT, tuple([ParameterMode.POSITIONAL] * 3)), empty_program._parse_opcode(3))

    def test_simple_io(self):
        program = IntcodeComputer([3, 0, 4, 0, 99])
        program.start()
        program.pass_input(8)
        self.assertEqual([8], program.read_output())

    def test_larger_program_less(self):
        self.larger_program.start()
        self.larger_program.pass_input(5)
        self.assertEqual([999], self.larger_program.read_output())

    def test_larger_program_equal(self):
        self.larger_program.start()
        self.larger_program.pass_input(8)
        self.assertEqual([1000], self.larger_program.read_output())

    def test_larger_program_more(self):
        self.larger_program.start()
        self.larger_program.pass_input(15)
        self.assertEqual([1001], self.larger_program.read_output())

    def test_quine(self):  # a quine is a program that outputs a copy of itself
        program = [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]
        computer = IntcodeComputer(program)
        computer.start()
        self.assertEqual(program, computer.read_output())

    def test_large_number(self):
        computer = IntcodeComputer([1102, 34915192, 34915192, 7, 4, 7, 99, 0])
        computer.start()
        output = computer.read_output()
        output_value = output[0]
        self.assertEqual(16, len(str(output_value)))
