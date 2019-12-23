import unittest

from day7.intcode_program import IntcodeProgram


class IntcodeProgramTestSuite(unittest.TestCase):

    def setUp(self) -> None:
        self.larger_program = IntcodeProgram([3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31,
                                              1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104,
                                              999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99])

    def test_parse_opcode(self):
        empty_program = IntcodeProgram(program=[])
        self.assertEqual((2, (0, 1, 0)), empty_program._parse_opcode(1002))
        self.assertEqual((3, (0, 0, 0)), empty_program._parse_opcode(3))

    def test_simple_io(self):
        program = IntcodeProgram([3, 0, 4, 0, 99])
        self.assertEqual(8, program.run([8]))

    def test_larger_program_less(self):
        self.assertEqual(999, self.larger_program.run([5]))

    def test_larger_program_equal(self):
        self.assertEqual(1000, self.larger_program.run([8]))

    def test_larger_program_more(self):
        self.assertEqual(1001, self.larger_program.run([15]))
