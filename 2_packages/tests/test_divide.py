import unittest
import sys
from pathlib import Path

# Add parent directory to path to import calc module
sys.path.insert(0, str(Path(__file__).parent.parent))

from calc import divide


class TestDivide(unittest.TestCase):
    def test_divide_two_numbers(self):
        self.assertEqual(divide(10, 2), 5)
        self.assertAlmostEqual(divide(1, 4), 0.25)

    def test_divide_by_zero_raises(self):
        with self.assertRaises(ZeroDivisionError):
            divide(1, 0)


if __name__ == "__main__":
    unittest.main()

