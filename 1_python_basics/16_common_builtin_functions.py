# ============================================================================
# COMMON BUILT-IN FUNCTIONS IN PYTHON
# ============================================================================

"""
Python provides many built-in functions that are always available.
These functions don't require importing and are ready to use.
This file covers the most commonly used built-in functions.
"""

# ============================================================================
# 1. TYPE CONVERSION FUNCTIONS
# ============================================================================

"""
These functions convert values from one type to another.
"""

# int() - converts to integer
result = int("123")
print(f"int('123'): {result}")  # Output: 123
result = int(3.14)
print(f"int(3.14): {result}")  # Output: 3 (truncates)

# float() - converts to float
result = float("3.14")
print(f"float('3.14'): {result}")  # Output: 3.14
result = float(5)
print(f"float(5): {result}")  # Output: 5.0

# str() - converts to string
result = str(123)
print(f"str(123): {result}")  # Output: '123'
result = str(3.14)
print(f"str(3.14): {result}")  # Output: '3.14'

# bool() - converts to boolean
result = bool(1)
print(f"bool(1): {result}")  # Output: True
result = bool(0)
print(f"bool(0): {result}")  # Output: False
result = bool("")
print(f"bool(''): {result}")  # Output: False

# list() - converts to list
result = list((1, 2, 3))
print(f"list((1, 2, 3)): {result}")  # Output: [1, 2, 3]
result = list("hello")
print(f"list('hello'): {result}")  # Output: ['h', 'e', 'l', 'l', 'o']

# tuple() - converts to tuple
result = tuple([1, 2, 3])
print(f"tuple([1, 2, 3]): {result}")  # Output: (1, 2, 3)

# set() - converts to set
result = set([1, 2, 3, 2, 1])
print(f"set([1, 2, 3, 2, 1]): {result}")  # Output: {1, 2, 3}

# dict() - converts to dictionary
result = dict([("a", 1), ("b", 2)])
print(f"dict([('a', 1), ('b', 2)]): {result}")  # Output: {'a': 1, 'b': 2}


# ============================================================================
# 2. TYPE CHECKING
# ============================================================================

"""
Functions to check types of objects.
"""

# type() - returns type of object
result = type(5)
print(f"type(5): {result}")  # Output: <class 'int'>
result = type("hello")
print(f"type('hello'): {result}")  # Output: <class 'str'>

# isinstance() - checks if object is instance of class
result = isinstance(5, int)
print(f"isinstance(5, int): {result}")  # Output: True
result = isinstance(5, str)
print(f"isinstance(5, str): {result}")  # Output: False

# Check multiple types
result = isinstance(5, (int, float))
print(f"isinstance(5, (int, float)): {result}")  # Output: True


# ============================================================================
# 3. MATHEMATICAL FUNCTIONS
# ============================================================================

"""
Mathematical operations and calculations.
"""

# abs() - absolute value
result = abs(-5)
print(f"abs(-5): {result}")  # Output: 5
result = abs(5)
print(f"abs(5): {result}")  # Output: 5

# round() - rounds number
result = round(3.14159, 2)
print(f"round(3.14159, 2): {result}")  # Output: 3.14
result = round(3.5)
print(f"round(3.5): {result}")  # Output: 4

# min() - minimum value
result = min(1, 2, 3)
print(f"min(1, 2, 3): {result}")  # Output: 1
result = min([10, 5, 20, 3])
print(f"min([10, 5, 20, 3]): {result}")  # Output: 3

# max() - maximum value
result = max(1, 2, 3)
print(f"max(1, 2, 3): {result}")  # Output: 3
result = max([10, 5, 20, 3])
print(f"max([10, 5, 20, 3]): {result}")  # Output: 20

# sum() - sum of iterable
result = sum([1, 2, 3])
print(f"sum([1, 2, 3]): {result}")  # Output: 6
result = sum(range(1, 6))
print(f"sum(range(1, 6)): {result}")  # Output: 15

# pow() - power function
result = pow(2, 3)
print(f"pow(2, 3): {result}")  # Output: 8
result = pow(5, 2)
print(f"pow(5, 2): {result}")  # Output: 25
# Equivalent to: 2 ** 3

# divmod() - division and modulus
result = divmod(10, 3)
print(f"divmod(10, 3): {result}")  # Output: (3, 1)
# Returns (quotient, remainder)


# ============================================================================
# 4. SEQUENCE FUNCTIONS
# ============================================================================

"""
Functions for working with sequences (lists, tuples, strings, etc.).
"""

# len() - length of sequence
result = len([1, 2, 3])
print(f"len([1, 2, 3]): {result}")  # Output: 3
result = len("hello")
print(f"len('hello'): {result}")  # Output: 5

# sorted() - returns sorted list
result = sorted([3, 1, 2])
print(f"sorted([3, 1, 2]): {result}")  # Output: [1, 2, 3]
result = sorted([3, 1, 2], reverse=True)
print(f"sorted([3, 1, 2], reverse=True): {result}")  # Output: [3, 2, 1]

# reversed() - returns reversed iterator
result = list(reversed([1, 2, 3]))
print(f"list(reversed([1, 2, 3])): {result}")  # Output: [3, 2, 1]
result = "".join(reversed("hello"))
print(f"Reversed string: {result}")  # Output: 'olleh'

# enumerate() - returns index and value
result = list(enumerate(["a", "b", "c"]))
print(f"list(enumerate(['a', 'b', 'c'])): {result}")  # Output: [(0, 'a'), (1, 'b'), (2, 'c')]

# zip() - combines iterables
result = list(zip([1, 2], [3, 4]))
print(f"list(zip([1, 2], [3, 4])): {result}")  # Output: [(1, 3), (2, 4)]

# range() - generates sequence of numbers
result = list(range(5))
print(f"list(range(5)): {result}")  # Output: [0, 1, 2, 3, 4]
result = list(range(1, 6))
print(f"list(range(1, 6)): {result}")  # Output: [1, 2, 3, 4, 5]
result = list(range(0, 10, 2))
print(f"list(range(0, 10, 2)): {result}")  # Output: [0, 2, 4, 6, 8]

# all() - returns True if all elements are truthy
result = all([True, True, False])
print(f"all([True, True, False]): {result}")  # Output: False
result = all([True, True, True])
print(f"all([True, True, True]): {result}")  # Output: True

# any() - returns True if any element is truthy
result = any([False, False, True])
print(f"any([False, False, True]): {result}")  # Output: True
result = any([False, False, False])
print(f"any([False, False, False]): {result}")  # Output: False


# ============================================================================
# 5. STRING FUNCTIONS
# ============================================================================

"""
Functions for character and string operations.
"""

# chr() - converts integer to character
result = chr(65)
print(f"chr(65): {result}")  # Output: 'A'
result = chr(97)
print(f"chr(97): {result}")  # Output: 'a'

# ord() - converts character to integer
result = ord("A")
print(f"ord('A'): {result}")  # Output: 65
result = ord("a")
print(f"ord('a'): {result}")  # Output: 97

# hex() - converts to hexadecimal string
result = hex(255)
print(f"hex(255): {result}")  # Output: '0xff'

# oct() - converts to octal string
result = oct(64)
print(f"oct(64): {result}")  # Output: '0o100'

# bin() - converts to binary string
result = bin(10)
print(f"bin(10): {result}")  # Output: '0b1010'


# ============================================================================
# 6. INPUT/OUTPUT FUNCTIONS
# ============================================================================

"""
Functions for reading input and displaying output.
"""

# print() - prints to console
print("Hello, World!")
print("Multiple", "values", "separated", "by", "spaces")

# input() - reads from console
# name = input("Enter your name: ")
# print(f"Hello, {name}!")

# open() - opens a file
# file = open("filename.txt", "r")
# content = file.read()
# file.close()


# ============================================================================
# 7. OBJECT FUNCTIONS
# ============================================================================

"""
Functions for inspecting and manipulating objects.
"""

# id() - returns identity of object
x = [1, 2, 3]
result = id(x)
print(f"id(x): {result}")  # Returns unique identifier

# hash() - returns hash value
result = hash("hello")
print(f"hash('hello'): {result}")  # Returns hash value

# dir() - returns list of attributes
result = dir([])
print(f"dir([]) attributes (first 5): {result[:5]}")  # Shows list methods

# vars() - returns __dict__ attribute
class Person:
    def __init__(self, name):
        self.name = name

person = Person("John")
result = vars(person)
print(f"vars(person): {result}")  # Output: {'name': 'John'}

# hasattr() - checks if object has attribute
result = hasattr([], "append")
print(f"hasattr([], 'append'): {result}")  # Output: True
result = hasattr([], "nonexistent")
print(f"hasattr([], 'nonexistent'): {result}")  # Output: False

# getattr() - gets attribute value
result = getattr([], "append")
print(f"getattr([], 'append'): {type(result)}")  # Output: <class 'builtin_function_or_method'>

# setattr() - sets attribute value
class Person:
    pass

person = Person()
setattr(person, "name", "Alice")
print(f"person.name: {person.name}")  # Output: Alice

# delattr() - deletes attribute
class Person:
    def __init__(self, name):
        self.name = name

person = Person("Bob")
delattr(person, "name")
# print(person.name)  # AttributeError


# ============================================================================
# 8. ITERABLE FUNCTIONS
# ============================================================================

"""
Functions for working with iterables and iterators.
"""

# iter() - returns iterator
iterator = iter([1, 2, 3])
print(f"iter([1, 2, 3]): {type(iterator)}")  # Output: <class 'list_iterator'>

# next() - returns next item from iterator
iterator = iter([1, 2, 3])
result = next(iterator)
print(f"next(iterator): {result}")  # Output: 1
result = next(iterator)
print(f"next(iterator): {result}")  # Output: 2

# map() - applies function to iterable
result = list(map(lambda x: x**2, [1, 2, 3]))
print(f"map(lambda x: x**2, [1, 2, 3]): {result}")  # Output: [1, 4, 9]

# filter() - filters iterable based on condition
result = list(filter(lambda x: x > 1, [1, 2, 3]))
print(f"filter(lambda x: x > 1, [1, 2, 3]): {result}")  # Output: [2, 3]

# reduce() - reduces iterable to single value (from functools)
from functools import reduce
result = reduce(lambda x, y: x + y, [1, 2, 3])
print(f"reduce(lambda x, y: x + y, [1, 2, 3]): {result}")  # Output: 6


# ============================================================================
# 9. OTHER USEFUL FUNCTIONS
# ============================================================================

"""
Additional useful built-in functions.
"""

# eval() - evaluates string as Python expression
result = eval("2 + 2")
print(f"eval('2 + 2'): {result}")  # Output: 4
# Warning: eval() can be dangerous with user input

# exec() - executes string as Python code
# exec("x = 5")
# print(x)  # Output: 5
# Warning: exec() can be dangerous with user input

# globals() - returns dictionary of global variables
result = globals()
print(f"globals() keys (first 5): {list(result.keys())[:5]}")

# locals() - returns dictionary of local variables
def my_function():
    local_var = "local"
    return locals()

result = my_function()
print(f"locals() in function: {result}")  # Output: {'local_var': 'local'}

# callable() - checks if object is callable
result = callable(print)
print(f"callable(print): {result}")  # Output: True
result = callable(5)
print(f"callable(5): {result}")  # Output: False

# help() - shows help documentation
# help(print)  # Shows help for print function

# repr() - returns official string representation
result = repr([1, 2, 3])
print(f"repr([1, 2, 3]): {result}")  # Output: '[1, 2, 3]'


# ============================================================================
# 10. PRACTICAL EXAMPLES
# ============================================================================

# Example 1: Type conversion in data processing
data = ["10", "20", "30", "40"]
numbers = [int(x) for x in data]
total = sum(numbers)
print(f"\nData processing:")
print(f"  Original: {data}")
print(f"  Converted: {numbers}")
print(f"  Total: {total}")

# Example 2: Finding min/max in data
scores = [85, 92, 78, 96, 88]
print(f"\nScores: {scores}")
print(f"  Highest: {max(scores)}")
print(f"  Lowest: {min(scores)}")
print(f"  Average: {sum(scores) / len(scores):.2f}")

# Example 3: Using enumerate and zip
names = ["Alice", "Bob", "Charlie"]
ages = [25, 30, 35]
print(f"\nPeople:")
for idx, (name, age) in enumerate(zip(names, ages), start=1):
    print(f"  {idx}. {name}: {age} years old")

# Example 4: Character manipulation
text = "Hello"
encoded = [ord(c) for c in text]
decoded = "".join([chr(c) for c in encoded])
print(f"\nCharacter encoding:")
print(f"  Original: {text}")
print(f"  Encoded: {encoded}")
print(f"  Decoded: {decoded}")

# Example 5: Data validation with all/any
numbers = [2, 4, 6, 8, 10]
all_even = all(x % 2 == 0 for x in numbers)
print(f"\nValidation:")
print(f"  Numbers: {numbers}")
print(f"  All even: {all_even}")

# Example 6: Using map and filter
numbers = range(1, 11)
squares = list(map(lambda x: x**2, numbers))
even_squares = list(filter(lambda x: x % 2 == 0, squares))
print(f"\nEven squares:")
print(f"  Numbers: {list(numbers)}")
print(f"  Squares: {squares}")
print(f"  Even squares: {even_squares}")

# Example 7: Type checking in function
def process_data(data):
    """Process data with type checking"""
    if isinstance(data, (list, tuple)):
        return sum(data) / len(data)
    elif isinstance(data, dict):
        return sum(data.values()) / len(data)
    else:
        return "Invalid data type"

print(f"\nData processing:")
print(f"  List: {process_data([1, 2, 3, 4, 5])}")
print(f"  Dict: {process_data({'a': 10, 'b': 20, 'c': 30})}")

# Example 8: Using sorted with key
students = [
    {"name": "Alice", "score": 85},
    {"name": "Bob", "score": 92},
    {"name": "Charlie", "score": 78}
]
sorted_by_score = sorted(students, key=lambda x: x["score"], reverse=True)
print(f"\nStudents sorted by score:")
for student in sorted_by_score:
    print(f"  {student['name']}: {student['score']}")

print("\nBuilt-in functions examples completed.")
