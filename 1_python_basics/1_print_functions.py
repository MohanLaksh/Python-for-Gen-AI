# ============================================================================
# PRINT AND INPUT FUNCTIONS
# ============================================================================

"""
The print() and input() functions are fundamental for interacting with users
in Python programs. They handle output to the console and input from the user.
"""

# ============================================================================
# 1. PRINT FUNCTION
# ============================================================================

"""
The print() function displays output to the console (standard output).
It can take multiple arguments and has optional parameters for formatting.
"""

# Basic print statement
print("Hello, MicroDegree!")

# Print multiple values (separated by space by default)
print("Hello", "World", "Python")  # Output: Hello World Python

# Using sep parameter (separator)
# sep controls what character(s) separate the arguments
print("Hello", "World", "Python", sep=", ")  # Output: Hello, World, Python
print("2024", "01", "15", sep="-")  # Output: 2024-01-15
print("Python", "Programming", sep=" | ")  # Output: Python | Programming

# Using end parameter
# end controls what character(s) are printed at the end (default is '\n')
print("Hello", "World", "Python", sep=", ", end="\n")  # Default: newline
print("Line 1", end=" ")  # No newline, adds space
print("Line 2")  # Continues on same line: "Line 1 Line 2"

print("First", end=" -> ")
print("Second", end=" -> ")
print("Third")  # Output: First -> Second -> Third

# Combining sep and end
print("Apple", "Banana", "Cherry", sep=", ", end=".\n")
# Output: Apple, Banana, Cherry.

# Printing variables
name = "Alice"
age = 25
print("Name:", name, "Age:", age)  # Output: Name: Alice Age: 25

# Using f-strings with print (Python 3.6+)
print(f"Hello, {name}! You are {age} years old.")
# Output: Hello, Alice! You are 25 years old.

# Printing different data types
print("String:", "Hello")
print("Integer:", 42)
print("Float:", 3.14)
print("Boolean:", True)
print("List:", [1, 2, 3])

# ============================================================================
# 2. INPUT FUNCTION
# ============================================================================

"""
The input() function reads a line of text from the user (standard input).
It always returns a string, even if the user enters a number.
Optional prompt parameter displays a message before reading input.
"""

# Basic input (with prompt)
name = input("Enter your name: ")
print(f"Hello, {name}!")

# Input without prompt
# value = input()  # Waits for user input

# Important: input() always returns a string
age = input("Enter your age: ")
print(f"Type of age: {type(age)}")  # <class 'str'>
print(f"You entered: {age}")

# Converting input to other types
age_int = int(input("Enter your age (as integer): "))
height_float = float(input("Enter your height in meters: "))

print(f"\nAge: {age_int} (type: {type(age_int)})")
print(f"Height: {height_float} (type: {type(height_float)})")

# Example: Multiple inputs
print("\n=== User Registration ===")
first_name = input("First name: ")
last_name = input("Last name: ")
email = input("Email: ")
phone = input("Phone: ")

print(f"\nRegistration Summary:")
print(f"Name: {first_name} {last_name}")
print(f"Email: {email}")
print(f"Phone: {phone}")
