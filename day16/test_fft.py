import unittest

from day16.fft import number_to_digits, get_pattern


class FFTTestSuite(unittest.TestCase):

    def test_number_to_digits(self):
        self.assertEqual([1, 2], number_to_digits(12))

    def test_get_pattern(self):
        self.assertEqual([0, 1, 1, 0, 0, -1, -1, 0], get_pattern(2, 8))
        self.assertEqual([1, 0], get_pattern(1, 2))
