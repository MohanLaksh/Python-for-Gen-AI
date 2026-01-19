import unittest
import sys
from pathlib import Path

# Add parent directory to path to import calc module
sys.path.insert(0, str(Path(__file__).parent.parent))

from calc import substract, subtract


class TestSubtract(unittest.TestCase):
    def test_substract_two_numbers(self):
        self.assertEqual(substract(10, 3), 7)
        self.assertEqual(substract(3, 10), -7)

    def test_subtract_alias_two_numbers(self):
        self.assertEqual(subtract(10, 3), 7)
        self.assertEqual(subtract(-1, -2), 1)


if __name__ == "__main__":
    unittest.main()

