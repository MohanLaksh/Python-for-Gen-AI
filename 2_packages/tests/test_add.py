import unittest
import sys
from pathlib import Path

# Add parent directory to path to import calc module
sys.path.insert(0, str(Path(__file__).parent.parent))

from calc import add, add_numbers

class TestAdd(unittest.TestCase):
    def test_add_two_numbers_positive(self):
        self.assertEqual(add(1, -2), -1)
        self.assertNotEqual(add(1, 2), 6)

    def test_add_multiple_numbers(self):
        self.assertEqual(add_numbers(1, 2, 3, 4, 5), 15)
        self.assertEqual(add_numbers(5), 5)
        self.assertEqual(add_numbers(), 0)

if __name__ == "__main__":
    unittest.main()