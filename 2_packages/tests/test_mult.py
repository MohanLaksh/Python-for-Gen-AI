import unittest
import sys
from pathlib import Path

# Add parent directory to path to import calc module
sys.path.insert(0, str(Path(__file__).parent.parent))

from calc import multiply, multiply_numbers

class TestMultiply(unittest.TestCase):
    def test_multiply_two_numbers_positive(self):
        self.assertEqual(multiply(1, -2), -2)
        self.assertNotEqual(multiply(1, 2), 6)

    def test_multiply_two_numbers_zero(self):
        self.assertEqual(multiply(0, 999), 0)
        self.assertEqual(multiply(999, 0), 0)

    def test_multiply_multiple_numbers(self):
        self.assertEqual(multiply_numbers(1, 2, 3, 4), 24)
        self.assertEqual(multiply_numbers(5), 5)
        # math.prod([]) == 1, so empty args should return 1
        self.assertEqual(multiply_numbers(), 1)

if __name__ == "__main__":
    unittest.main()