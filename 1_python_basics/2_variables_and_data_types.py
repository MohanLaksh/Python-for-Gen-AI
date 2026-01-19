# ============================================================================
# VARIABLES & DATA TYPES
# ============================================================================

"""
Variables are containers for storing data values. Python is dynamically typed,
meaning you don't need to declare the type of a variable - Python infers it
from the value assigned. Python supports various data types.
"""

# ============================================================================
# 1. DATA TYPES IN PYTHON
# ============================================================================

"""
Python has several built-in data types:
- String (str): Text data
- Integer (int): Whole numbers
- Float (float): Decimal numbers
- Boolean (bool): True or False
- None: Represents absence of value
"""

# String -> Text enclosed in quotes
name = "Name"
greeting = "Hello Python"
number_as_string = '123'  # This is a string, not a number
print(f"String examples: {name}, {greeting}, {number_as_string}")

# Integer -> Whole numbers (positive, negative, or zero)
age = 1
count = 2
temperature = -5
population = 100
print(f"Integer examples: {age}, {count}, {temperature}, {population}")

# Float -> Decimal numbers
price = 1.5
temperature = 2.5
pi = 3.5
percentage = 98.75
print(f"Float examples: {price}, {temperature}, {pi}, {percentage}")

# Boolean -> True or False (must be capitalized)
is_student = True
is_active = False
has_permission = True
print(f"Boolean examples: {is_student}, {is_active}, {has_permission}")

# None -> Represents absence of value
value = None
result = None
print(f"None examples: {value}, {result}")


# ============================================================================
# 2. VARIABLE NAMING CONVENTIONS
# ============================================================================

"""
Python has specific rules and conventions for naming variables:
1. Must start with a letter (a-z, A-Z) or an underscore (_)
2. Can only contain letters, numbers, and underscores
3. Must be unique within the scope
4. Should be descriptive and meaningful
5. Should be short and concise
6. Are case-sensitive (name, Name, NAME are different)
7. Cannot use Python keywords (if, for, def, etc.)
"""

# Valid variable names
name = "John"
_name = "Private variable"
name1 = "With number"
user_name = "Snake case (recommended)"
userName = "Camel case (also valid)"
USER_CONSTANT = "Constants in UPPER_CASE"

# Invalid variable names (will cause errors)
# 1name = "Invalid"  # Cannot start with number
# name-var = "Invalid"  # Cannot use hyphens
# name var = "Invalid"  # Cannot use spaces
# if = "Invalid"  # Cannot use keywords

# Best practices
# Use snake_case for variables and functions
user_age = 25
total_count = 100
is_valid = True

# Use UPPER_CASE for constants
MAX_SIZE = 1000
DEFAULT_TIMEOUT = 30
PI = 3.14159

# Use descriptive names
# Good:
student_count = 50
user_email = "user@example.com"

# Bad:
sc = 50  # Not descriptive
ue = "user@example.com"  # Abbreviation unclear


# ============================================================================
# 3. VARIABLE ASSIGNMENT
# ============================================================================

"""
Variables are assigned using the = operator. Python is dynamically typed,
so the same variable can hold different types of values.
"""

# Single variable assignment
name = "John"
age = 20
is_student = True
height = 1.75

print(f"\nSingle assignments:")
print(f"Name: {name}, Type: {type(name)}")
print(f"Age: {age}, Type: {type(age)}")
print(f"Is student: {is_student}, Type: {type(is_student)}")
print(f"Height: {height}, Type: {type(height)}")

# Multiple variable assignment (unpacking)
name, age, is_student, height = "John", 20, True, 1.75

print(f"\nMultiple assignments:")
print(f"Name: {name}, Age: {age}, Student: {is_student}, Height: {height}")

# Swapping variables (Pythonic way)
a = 10
b = 20
print(f"\nBefore swap: a={a}, b={b}")
a, b = b, a  # Swap without temporary variable
print(f"After swap: a={a}, b={b}")

# Chained assignment
x = y = z = 0
print(f"\nChained assignment: x={x}, y={y}, z={z}")

# Unpacking from tuples
coordinates = (10, 20, 30)
x, y, z = coordinates
print(f"Unpacked coordinates: x={x}, y={y}, z={z}")


# ============================================================================
# 4. TYPE CHECKING
# ============================================================================

"""
The type() function returns the type of a variable or value.
This is useful for debugging and type checking.
"""

# Using type() function
name = "John"
age = 25
price = 19.99
is_active = True

print(f"\nType checking:")
print(f"type(name): {type(name)}")  # <class 'str'>
print(f"type(age): {type(age)}")  # <class 'int'>
print(f"type(price): {type(price)}")  # <class 'float'>
print(f"type(is_active): {type(is_active)}")  # <class 'bool'>

# Checking if variable is of specific type
print(f"\nType checking with isinstance():")
print(f"isinstance(name, str): {isinstance(name, str)}")  # True
print(f"isinstance(age, int): {isinstance(age, int)}")  # True
print(f"isinstance(age, float): {isinstance(age, float)}")  # False


# ============================================================================
# 5. TYPE CASTING (TYPE CONVERSION)
# ============================================================================

"""
Type casting converts a value from one data type to another.
Python provides built-in functions for type conversion.
"""

# int() -> converts to integer
print(f"\nType casting to integer:")
print(f"int('123'): {int('123')}")  # 123
print(f"int(3.7): {int(3.7)}")  # 3 (truncates decimal)
print(f"int(True): {int(True)}")  # 1
print(f"int(False): {int(False)}")  # 0
# Note: int("3.14") will raise ValueError - must convert to float first

# float() -> converts to float
print(f"\nType casting to float:")
print(f"float('3.14'): {float('3.14')}")  # 3.14
print(f"float(5): {float(5)}")  # 5.0
print(f"float('123'): {float('123')}")  # 123.0

# str() -> converts to string
print(f"\nType casting to string:")
print(f"str(123): {str(123)}")  # '123'
print(f"str(3.14): {str(3.14)}")  # '3.14'
print(f"str(True): {str(True)}")  # 'True'
print(f"str([1, 2, 3]): {str([1, 2, 3])}")  # '[1, 2, 3]'

# bool() -> converts to boolean
print(f"\nType casting to boolean:")
print(f"bool(1): {bool(1)}")  # True
print(f"bool(0): {bool(0)}")  # False
print(f"bool(''): {bool('')}")  # False (empty string)
print(f"bool('hello'): {bool('hello')}")  # True (non-empty string)
print(f"bool([]): {bool([])}")  # False (empty list)
print(f"bool([1, 2]): {bool([1, 2])}")  # True (non-empty list)
print(f"bool(None): {bool(None)}")  # False

# Truthiness in Python:
# False values: False, None, 0, 0.0, '', [], (), {}, set()
# True values: Everything else


# ============================================================================
# 6. PRACTICAL EXAMPLES
# ============================================================================

# Example 1: User input with type conversion
print("\n=== Example: User Input Processing ===")
# Simulating user input
user_input = "25"  # input() always returns string
age = int(user_input)
print(f"User age: {age}, Type: {type(age)}")

# Example 2: Dynamic typing demonstration
print("\n=== Example: Dynamic Typing ===")
variable = 10
print(f"variable = {variable}, type = {type(variable)}")

variable = "Hello"
print(f"variable = {variable}, type = {type(variable)}")

variable = [1, 2, 3]
print(f"variable = {variable}, type = {type(variable)}")

# Example 4: Type conversion in calculations
print("\n=== Example: Type Conversion in Calculations ===")
num1 = "10"
num2 = "20"
result = int(num1) + int(num2)
print(f"{num1} + {num2} = {result}")

price_str = "19.99"
tax_rate = 0.08
price = float(price_str)
total = price * (1 + tax_rate)
print(f"Price: ${price}, Total with tax: ${total:.2f}")

# Example 5: Boolean conversion examples
print("\n=== Example: Boolean Conversion ===")
print(f"bool(1): {bool(1)}")  # True
print(f"bool(0): {bool(0)}")  # False
print(f"bool(''): {bool('')}")  # False (empty string)
print(f"bool('hello'): {bool('hello')}")  # True (non-empty string)
print(f"bool([]): {bool([])}")  # False (empty list)
print(f"bool([1, 2]): {bool([1, 2])}")  # True (non-empty list)
