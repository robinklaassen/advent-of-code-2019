import unittest

from day5.part2 import run_program


class IntcodeProgramTestSuite(unittest.TestCase):

    def setUp(self) -> None:
        self.jump_position_mode_program = [3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9]
        self.jump_immediate_mode_program = [3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1]
        self.larger_program = [3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31,
                               1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104,
                               999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99]

    def test_simple_io(self):
        program = [3, 0, 4, 0, 99]
        _, output = run_program(initial_program_state=program, program_input=15)
        self.assertEqual(15, output)

    def test_equal_position_mode(self):
        program = [3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8]
        _, output = run_program(initial_program_state=program, program_input=8)
        self.assertEqual(1, output)

    def test_less_position_mode(self):
        program = [3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8]
        _, output = run_program(initial_program_state=program, program_input=4)
        self.assertEqual(1, output)

    def test_equal_immediate_mode(self):
        program = [3, 3, 1108, -1, 8, 3, 4, 3, 99]
        _, output = run_program(initial_program_state=program, program_input=8)
        self.assertEqual(1, output)

    def test_less_immediate_mode(self):
        program = [3, 3, 1107, -1, 8, 3, 4, 3, 99]
        _, output = run_program(initial_program_state=program, program_input=4)
        self.assertEqual(1, output)

    def test_jump_position_mode_true(self):
        _, output = run_program(initial_program_state=self.jump_position_mode_program, program_input=1)
        self.assertEqual(1, output)

    def test_jump_position_mode_false(self):
        _, output = run_program(initial_program_state=self.jump_position_mode_program, program_input=0)
        self.assertEqual(0, output)

    def test_jump_immediate_mode_true(self):
        _, output = run_program(initial_program_state=self.jump_immediate_mode_program, program_input=1)
        self.assertEqual(1, output)

    def test_jump_immediate_mode_false(self):
        _, output = run_program(initial_program_state=self.jump_immediate_mode_program, program_input=0)
        self.assertEqual(0, output)

    def test_larger_program_less(self):
        _, output = run_program(initial_program_state=self.larger_program, program_input=5)
        self.assertEqual(999, output)

    def test_larger_program_equal(self):
        _, output = run_program(initial_program_state=self.larger_program, program_input=8)
        self.assertEqual(1000, output)

    def test_larger_program_more(self):
        _, output = run_program(initial_program_state=self.larger_program, program_input=15)
        self.assertEqual(1001, output)

