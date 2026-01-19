# test_math.py
def add(a, b):
    return a + b

def multiply(a, b):
    return a * b
# Test functions - no class needed!


import pytest

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0
def test_multiply():
    assert multiply(2, 3) == 6
    assert multiply(-1, 5) == -5
    assert multiply(0, 100) == 0
def test_add_floats():
    result = add(0.1, 0.2)
    assert result == pytest.approx(0.3) # Handle floating point