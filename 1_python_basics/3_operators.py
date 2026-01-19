# ============================================================================
# OPERATORS IN PYTHON
# ============================================================================

"""
Operators are special symbols that perform operations on variables and values.
Python supports various types of operators for different purposes.
"""

# ============================================================================
# 1. ARITHMETIC OPERATORS
# ============================================================================

"""
Arithmetic operators perform mathematical operations on numeric values.
"""

# + (addition) - Adds two numbers
result = 5 + 3
print(f"5 + 3 = {result}")  # Output: 8

# Can also concatenate strings and lists
text = "Hello" + " " + "World"
print(f"String concatenation: {text}")  # Output: Hello World

# - (subtraction) - Subtracts second number from first
result = 10 - 4
print(f"10 - 4 = {result}")  # Output: 6

# * (multiplication) - Multiplies two numbers
result = 3 * 4
print(f"3 * 4 = {result}")  # Output: 12

# Can also repeat strings and lists
text = "Hi" * 3
print(f"String repetition: {text}")  # Output: HiHiHi

# / (division) - Divides first number by second (always returns float)
result = 15 / 3
print(f"15 / 3 = {result}")  # Output: 5.0
result = 10 / 3
print(f"10 / 3 = {result}")  # Output: 3.3333333333333335

# % (modulus) - Returns remainder after division
result = 10 % 3
print(f"10 % 3 = {result}")  # Output: 1 (10 divided by 3 is 3 with remainder 1)
result = 15 % 4
print(f"15 % 4 = {result}")  # Output: 3

# ** (exponentiation) - Raises first number to power of second
result = 2 ** 3
print(f"2 ** 3 = {result}")  # Output: 8 (2 to the power of 3)
result = 5 ** 2
print(f"5 ** 2 = {result}")  # Output: 25

# // (floor division) - Divides and rounds down to nearest integer
result = 15 // 4
print(f"15 // 4 = {result}")  # Output: 3 (not 3.75)
result = -15 // 4
print(f"-15 // 4 = {result}")  # Output: -4 (rounds down, not toward zero)


# ============================================================================
# 2. COMPARISON OPERATORS
# ============================================================================

"""
Comparison operators compare two values and return a boolean (True or False).
Used extensively in conditional statements and loops.
"""

# == (equal to) - Checks if two values are equal
result = 5 == 5
print(f"5 == 5: {result}")  # Output: True
result = 5 == 3
print(f"5 == 3: {result}")  # Output: False

# != (not equal to) - Checks if two values are not equal
result = 5 != 3
print(f"5 != 3: {result}")  # Output: True
result = 5 != 5
print(f"5 != 5: {result}")  # Output: False

# < (less than) - Checks if first value is less than second
result = 5 < 10
print(f"5 < 10: {result}")  # Output: True
result = 10 < 5
print(f"10 < 5: {result}")  # Output: False

# > (greater than) - Checks if first value is greater than second
result = 5 > 3
print(f"5 > 3: {result}")  # Output: True
result = 3 > 5
print(f"3 > 5: {result}")  # Output: False

# <= (less than or equal to) - Checks if first value is less than or equal to second
result = 5 <= 5
print(f"5 <= 5: {result}")  # Output: True
result = 5 <= 3
print(f"5 <= 3: {result}")  # Output: False

# >= (greater than or equal to) - Checks if first value is greater than or equal to second
result = 5 >= 3
print(f"5 >= 3: {result}")  # Output: True
result = 3 >= 5
print(f"3 >= 5: {result}")  # Output: False

# Chaining comparisons (Python feature)
age = 25
result = 18 <= age <= 65
print(f"18 <= {age} <= 65: {result}")  # Output: True


# ============================================================================
# 3. LOGICAL OPERATORS
# ============================================================================

"""
Logical operators combine boolean expressions and return boolean results.
Used to create complex conditions.
"""

# and - Returns True if both conditions are True
result = True and False
print(f"True and False: {result}")  # Output: False
result = True and True
print(f"True and True: {result}")  # Output: True

# Practical example
age = 25
has_license = True
can_drive = age >= 18 and has_license
print(f"Can drive: {can_drive}")  # Output: True

# or - Returns True if at least one condition is True
result = True or False
print(f"True or False: {result}")  # Output: True
result = False or False
print(f"False or False: {result}")  # Output: False

# Practical example
is_weekend = False
is_holiday = True
can_sleep_in = is_weekend or is_holiday
print(f"Can sleep in: {can_sleep_in}")  # Output: True

# not - Reverses the boolean value
result = not True
print(f"not True: {result}")  # Output: False
result = not False
print(f"not False: {result}")  # Output: True

# Practical example
is_raining = True
should_go_out = not is_raining
print(f"Should go out: {should_go_out}")  # Output: False

# Combining logical operators
score = 85
attendance = 0.95
passed = score >= 70 and attendance >= 0.80
print(f"Passed: {passed}")  # Output: True

# Operator precedence: not > and > or
result = not False and True or False
print(f"not False and True or False: {result}")  # Output: True


# ============================================================================
# 4. ASSIGNMENT OPERATORS
# ============================================================================

"""
Assignment operators assign values to variables.
Shorthand operators combine assignment with arithmetic operations.
"""

# = (assignment) - Assigns value to variable
x = 5
print(f"x = 5: x = {x}")

# += (add and assign) - Equivalent to x = x + value
x = 5
x += 3  # Same as x = x + 3
print(f"x += 3: x = {x}")  # Output: 8

# -= (subtract and assign) - Equivalent to x = x - value
x = 10
x -= 2  # Same as x = x - 2
print(f"x -= 2: x = {x}")  # Output: 8

# *= (multiply and assign) - Equivalent to x = x * value
x = 5
x *= 2  # Same as x = x * 2
print(f"x *= 2: x = {x}")  # Output: 10

# /= (divide and assign) - Equivalent to x = x / value
x = 10
x /= 2  # Same as x = x / 2
print(f"x /= 2: x = {x}")  # Output: 5.0

# %= (modulus and assign) - Equivalent to x = x % value
x = 10
x %= 3  # Same as x = x % 3
print(f"x %= 3: x = {x}")  # Output: 1

# **= (exponentiate and assign) - Equivalent to x = x ** value
x = 2
x **= 3  # Same as x = x ** 3
print(f"x **= 3: x = {x}")  # Output: 8

# //= (floor divide and assign) - Equivalent to x = x // value
x = 15
x //= 4  # Same as x = x // 4
print(f"x //= 4: x = {x}")  # Output: 3

# Works with other types too
text = "Hello"
text += " World"  # String concatenation
print(f"text += ' World': {text}")  # Output: Hello World


# ============================================================================
# 5. OPERATOR PRECEDENCE
# ============================================================================

"""
Operators have different precedence levels. When multiple operators are used,
operations with higher precedence are performed first.

Order (highest to lowest):
1. Parentheses ()
2. Exponentiation **
3. Multiplication, Division, Floor Division, Modulus (*, /, //, %)
4. Addition, Subtraction (+, -)
5. Comparison operators (==, !=, <, >, <=, >=)
6. Identity operators (is, is not)
7. Membership operators (in, not in)
8. Logical NOT (not)
9. Logical AND (and)
10. Logical OR (or)
"""

# Example demonstrating precedence
result = 2 + 3 * 4
print(f"2 + 3 * 4 = {result}")  # Output: 14 (not 20)
# Multiplication happens first: 3 * 4 = 12, then 2 + 12 = 14

result = (2 + 3) * 4
print(f"(2 + 3) * 4 = {result}")  # Output: 20
# Parentheses change order: 2 + 3 = 5, then 5 * 4 = 20

result = 2 ** 3 * 4
print(f"2 ** 3 * 4 = {result}")  # Output: 32
# Exponentiation first: 2 ** 3 = 8, then 8 * 4 = 32

# Complex expression
result = 5 + 3 * 2 ** 2 - 1
print(f"5 + 3 * 2 ** 2 - 1 = {result}")  # Output: 16
# Order: 2 ** 2 = 4, then 3 * 4 = 12, then 5 + 12 = 17, then 17 - 1 = 16
