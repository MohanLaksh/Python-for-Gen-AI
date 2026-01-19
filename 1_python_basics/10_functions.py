# ============================================================================
# FUNCTIONS IN PYTHON
# ============================================================================

"""
Functions are reusable blocks of code that perform specific tasks.
They help organize code, reduce repetition, and make programs more modular.
"""

# ============================================================================
# 1. FUNCTION DEFINITION
# ============================================================================

"""
Functions are defined using the def keyword.
They can take parameters and return values.
"""

# Basic function definition
def function_name(parameters):
    # code block
    return value

# Example: Simple function
def greet():
    """Function that greets"""
    print("Hello, World!")

# Function call
greet()  # Output: Hello, World!

# Example: Function with parameters
def greet_person(name):
    """Function that greets a person"""
    print(f"Hello, {name}!")

greet_person("Alice")  # Output: Hello, Alice!

# Example: Function with return value
def add(a, b):
    """Add two numbers"""
    return a + b

result = add(5, 3)
print(f"5 + 3 = {result}")  # Output: 8


# ============================================================================
# 2. FUNCTION CALL
# ============================================================================

"""
Functions are called using their name followed by parentheses.
Arguments are passed inside the parentheses.
"""

# Calling a function
#result = function_name(arguments)

# Example: Multiple function calls
def square(x):
    """Calculate square of a number"""
    return x ** 2

numbers = [1, 2, 3, 4, 5]
squares = []
for num in numbers:
    squares.append(square(num))
print(f"Squares: {squares}")  # Output: [1, 4, 9, 16, 25]


# ============================================================================
# 3. FUNCTION WITH DEFAULT PARAMETERS
# ============================================================================

"""
Default parameters have default values if not provided.
They must come after non-default parameters.
"""

# Function with default parameter
def greet(name, greeting="Hello"):
    """Greet with optional greeting"""
    return f"{greeting}, {name}!"

# Using default value
print(greet("Alice"))  # Output: Hello, Alice!

# Overriding default value
print(greet("Bob", "Hi"))  # Output: Hi, Bob!

# Example: Power function with default exponent
def power(base, exponent=2):
    """Calculate base raised to exponent (default: square)"""
    return base ** exponent

print(f"5^2 = {power(5)}")  # Output: 25 (uses default)
print(f"5^3 = {power(5, 3)}")  # Output: 125 (overrides default)

# Multiple default parameters
def create_profile(name, age=18, city="Unknown"):
    """Create user profile with defaults"""
    return f"Name: {name}, Age: {age}, City: {city}"

print(create_profile("Alice"))  # Uses all defaults
print(create_profile("Bob", 25))  # Overrides age
print(create_profile("Charlie", 30, "New York"))  # Overrides all


# ============================================================================
# 4. FUNCTION WITH KEYWORD ARGUMENTS
# ============================================================================

"""
Keyword arguments allow you to specify parameters by name.
Order doesn't matter when using keyword arguments.
"""

# Function with keyword arguments
def person_info(name, age, city):
    """Display person information"""
    return f"{name} is {age} years old and lives in {city}"

# Using keyword arguments
info = person_info(name="John", age=30, city="NYC")
print(info)  # Output: John is 30 years old and lives in NYC

# Order doesn't matter with keyword arguments
info = person_info(city="NYC", name="John", age=30)
print(info)  # Same output

# Mixing positional and keyword arguments
info = person_info("John", age=30, city="NYC")
print(info)  # Positional first, then keywords

# Example: Rectangle area
def rectangle_area(length, width):
    """Calculate rectangle area"""
    return length * width

# Using keyword arguments
area = rectangle_area(width=5, length=10)
print(f"Area: {area}")  # Output: 50


# ============================================================================
# 5. FUNCTION WITH *ARGS (VARIABLE POSITIONAL ARGUMENTS)
# ============================================================================

"""
*args allows a function to accept any number of positional arguments.
They are collected into a tuple.
"""

# Function with *args
def sum_numbers(*args):
    """Sum any number of arguments"""
    return sum(args)

# Calling with different numbers of arguments
print(f"Sum of 1, 2, 3: {sum_numbers(1, 2, 3)}")  # Output: 6
print(f"Sum of 1, 2, 3, 4, 5: {sum_numbers(1, 2, 3, 4, 5)}")  # Output: 15

# Example: Average function
def average(*args):
    """Calculate average of numbers"""
    if len(args) == 0:
        return 0
    return sum(args) / len(args)

print(f"Average of 10, 20, 30: {average(10, 20, 30)}")  # Output: 20.0

# Example: Print all arguments
def print_all(*args):
    """Print all arguments"""
    for arg in args:
        print(f"  {arg}")

print("Printing all arguments:")
print_all("apple", "banana", "cherry")


# ============================================================================
# 6. FUNCTION WITH **KWARGS (VARIABLE KEYWORD ARGUMENTS)
# ============================================================================

"""
**kwargs allows a function to accept any number of keyword arguments.
They are collected into a dictionary.
"""

# Function with **kwargs
def print_info(**kwargs):
    """Print all keyword arguments"""
    for key, value in kwargs.items():
        print(f"{key}: {value}")

# Calling with keyword arguments
print("Person info:")
print_info(name="John", age=30, city="NYC")

# Example: Configuration function
def configure(**kwargs):
    """Configure settings"""
    config = {}
    for key, value in kwargs.items():
        config[key] = value
    return config

settings = configure(host="localhost", port=8080, debug=True)
print(f"Settings: {settings}")

# Combining *args and **kwargs
def flexible_function(*args, **kwargs):
    """Function that accepts both args and kwargs"""
    print(f"Positional arguments: {args}")
    print(f"Keyword arguments: {kwargs}")

flexible_function(1, 2, 3, name="Alice", age=25)


# ============================================================================
# 7. LAMBDA FUNCTIONS (ANONYMOUS FUNCTIONS)
# ============================================================================

"""
Lambda functions are small, anonymous functions defined with lambda keyword.
They can take any number of arguments but only one expression.
"""

# Basic lambda function
square = lambda x: x ** 2
print(f"Square of 5: {square(5)}")  # Output: 25

# Lambda with multiple parameters
add = lambda x, y: x + y
print(f"5 + 3 = {add(5, 3)}")  # Output: 8

# Lambda functions are often used with map, filter, sorted
numbers = [1, 2, 3, 4, 5]
squares = list(map(lambda x: x ** 2, numbers))
print(f"Squares: {squares}")  # Output: [1, 4, 9, 16, 25]

# Filter even numbers
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(f"Even numbers: {evens}")  # Output: [2, 4]

# Sort by absolute value
numbers = [-5, 2, -1, 4, -3]
sorted_nums = sorted(numbers, key=lambda x: abs(x))
print(f"Sorted by absolute value: {sorted_nums}")  # Output: [-1, 2, -3, 4, -5]


# ============================================================================
# 8. FUNCTION SCOPE
# ============================================================================

"""
Variables have different scopes: global, local, and nonlocal.
Scope determines where a variable can be accessed.
"""

# Global variable - accessible everywhere
global_var = "global"

def my_function():
    """Function demonstrating scope"""
    # Local variable - accessible only within function
    local_var = "local"
    print(f"Inside function - global_var: {global_var}")
    print(f"Inside function - local_var: {local_var}")

my_function()
print(f"Outside function - global_var: {global_var}")
# print(local_var)  # Error: local_var is not defined

# Accessing global variable
count = 0

def increment():
    """Increment global count"""
    global count  # Declare we're using global variable
    count += 1

increment()
print(f"Count: {count}")  # Output: 1

# Nonlocal variable - accessible in nested function
def outer_function():
    """Outer function with nested function"""
    outer_var = "outer"
    
    def nested_function():
        """Nested function"""
        nonlocal outer_var  # Access variable from enclosing scope
        outer_var = "modified"
        print(f"Nested function - outer_var: {outer_var}")
    
    print(f"Before nested - outer_var: {outer_var}")
    nested_function()
    print(f"After nested - outer_var: {outer_var}")

outer_function()


# ============================================================================
# 9. RECURSIVE FUNCTIONS
# ============================================================================

"""
Recursive functions call themselves.
They must have a base case to avoid infinite recursion.
"""

# Factorial using recursion
def factorial(n):
    """Calculate factorial recursively"""
    if n == 0:  # Base case
        return 1
    return n * factorial(n - 1)  # Recursive case

print(f"Factorial of 5: {factorial(5)}")  # Output: 120

# Fibonacci using recursion
def fibonacci(n):
    """Calculate nth Fibonacci number recursively"""
    if n <= 1:  # Base case
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)  # Recursive case

print("Fibonacci sequence:")
for i in range(10):
    print(f"  F({i}) = {fibonacci(i)}")

# Sum of list using recursion
def sum_list(lst):
    """Sum list elements recursively"""
    if len(lst) == 0:  # Base case
        return 0
    return lst[0] + sum_list(lst[1:])  # Recursive case

numbers = [1, 2, 3, 4, 5]
print(f"Sum of {numbers}: {sum_list(numbers)}")  # Output: 15


# ============================================================================
# 10. DOCSTRINGS
# ============================================================================

"""
Docstrings document functions.
They are accessed using help() or .__doc__
"""

def function_name():
    """This is a docstring describing the function."""
    pass

# Example: Well-documented function
def calculate_area(length, width):
    """
    Calculate the area of a rectangle.
    
    Parameters:
    length (float): Length of the rectangle
    width (float): Width of the rectangle
    
    Returns:
    float: Area of the rectangle
    """
    return length * width

# Accessing docstring
print(calculate_area.__doc__)
# help(calculate_area)  # Also shows docstring


# ============================================================================
# 11. TYPE HINTS (Python 3.5+)
# ============================================================================

"""
Type hints indicate expected types for parameters and return values.
They don't enforce types but help with documentation and IDE support.
"""

# Function with type hints
def add(a: int, b: int) -> int:
    """Add two integers"""
    return a + b

result = add(5, 3)
print(f"5 + 3 = {result}")  # Output: 8

# Multiple types
from typing import Union, List

def process_data(data: Union[int, str]) -> str:
    """Process integer or string data"""
    return str(data)

# List type hint
def sum_numbers(numbers: List[int]) -> int:
    """Sum list of integers"""
    return sum(numbers)

print(f"Sum: {sum_numbers([1, 2, 3, 4, 5])}")  # Output: 15


# ============================================================================
# 12. PRACTICAL EXAMPLES
# ============================================================================

# Example 1: Calculator functions
def calculator(operation, a, b):
    """Simple calculator"""
    operations = {
        "add": lambda x, y: x + y,
        "subtract": lambda x, y: x - y,
        "multiply": lambda x, y: x * y,
        "divide": lambda x, y: x / y if y != 0 else "Cannot divide by zero"
    }
    return operations.get(operation, lambda x, y: "Invalid operation")(a, b)

print("\nCalculator:")
print(f"  10 + 5 = {calculator('add', 10, 5)}")
print(f"  10 - 5 = {calculator('subtract', 10, 5)}")
print(f"  10 * 5 = {calculator('multiply', 10, 5)}")
print(f"  10 / 5 = {calculator('divide', 10, 5)}")

# Example 2: Data validation
def validate_email(email: str) -> bool:
    """Validate email format"""
    return "@" in email and "." in email.split("@")[1]

emails = ["user@example.com", "invalid", "test@domain"]
print("\nEmail validation:")
for email in emails:
    print(f"  {email}: {validate_email(email)}")

# Example 3: Higher-order function
def apply_operation(numbers, operation):
    """Apply operation to list of numbers"""
    return [operation(num) for num in numbers]

numbers = [1, 2, 3, 4, 5]
squares = apply_operation(numbers, lambda x: x ** 2)
cubes = apply_operation(numbers, lambda x: x ** 3)

print(f"\nNumbers: {numbers}")
print(f"Squares: {squares}")
print(f"Cubes: {cubes}")

# Example 4: Function with default and variable arguments
def create_user(name, email, *roles, **metadata):
    """Create user with roles and metadata"""
    user = {
        "name": name,
        "email": email,
        "roles": list(roles),
        "metadata": metadata
    }
    return user

user = create_user("Alice", "alice@example.com", "admin", "user", 
                   department="IT", active=True)
print(f"\nUser: {user}")

# Example 5: Memoization (caching results)
cache = {}

def fibonacci_memo(n):
    """Fibonacci with memoization"""
    if n in cache:
        return cache[n]
    if n <= 1:
        result = n
    else:
        result = fibonacci_memo(n - 1) + fibonacci_memo(n - 2)
    cache[n] = result
    return result

print(f"\nFibonacci(10) with memoization: {fibonacci_memo(10)}")
