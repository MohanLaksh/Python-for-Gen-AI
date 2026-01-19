# ============================================================================
# MODULES & PACKAGES IN PYTHON
# ============================================================================

"""
Modules are files containing Python code (functions, classes, variables).
Packages are directories containing multiple modules.
They help organize code and promote code reuse.
"""

# ============================================================================
# 1. IMPORTING A MODULE
# ============================================================================

"""
Modules are imported using the import statement.
You can import entire modules or specific items.
"""

# Import entire module
import module_name
import module_name as alias

# Example: Import math module
import math
print(f"Pi: {math.pi}")  # Access using module.attribute
print(f"Square root of 16: {math.sqrt(16)}")

# Import with alias
import math as m
print(f"Pi: {m.pi}")

# Import specific items from module
from module_name import function_name
from module_name import function1, function2
from module_name import *

# Example: Import specific functions
from math import sqrt, pi
print(f"Pi: {pi}")  # Direct access, no module prefix
print(f"Square root: {sqrt(25)}")

# Import multiple items
from math import sqrt, pi, sin, cos
print(f"Sin(90): {sin(pi/2)}")

# Import all (not recommended - can cause name conflicts)
from math import *
print(f"Pi: {pi}")  # Direct access


# ============================================================================
# 2. CREATING A MODULE
# ============================================================================

"""
To create a module, save code in a .py file.
The filename (without .py) becomes the module name.
"""

# Creating a module:
# 1. Save code in a .py file (e.g., my_module.py)
# 2. The filename (without .py) becomes the module name
# Example: my_module.py contains:
#   def greet(name):
#       return f"Hello, {name}!"
#   
#   PI = 3.14159
#
# Then import it:
#   import my_module
#   my_module.greet("Alice")

# Example: Creating a simple module
# Save this in a file called calculator.py:
"""
# calculator.py
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    return a / b if b != 0 else None
"""

# Then use it:
# import calculator
# result = calculator.add(5, 3)


# ============================================================================
# 3. USING A MODULE
# ============================================================================

"""
Modules are used by importing them and accessing their contents.
"""

# Using a module
import my_module
my_module.function_name()

# Example: Using math module
import math

# Using module functions
print(f"Square root: {math.sqrt(16)}")
print(f"Power: {math.pow(2, 3)}")
print(f"Factorial: {math.factorial(5)}")

# Using module constants
print(f"Pi: {math.pi}")
print(f"E: {math.e}")

# Using module classes
from math import radians, degrees
print(f"90 degrees = {radians(90)} radians")


# ============================================================================
# 4. STANDARD LIBRARY MODULES
# ============================================================================

"""
Python comes with many built-in modules (standard library).
These provide common functionality without installing packages.
"""

# os - operating system interface
import os
current_dir = os.getcwd()
print(f"Current directory: {current_dir}")
# os.listdir() - list directory contents
# os.mkdir() - create directory
# os.path.exists() - check if path exists

# sys - system-specific parameters
import sys
print(f"Python version: {sys.version}")
print(f"Platform: {sys.platform})
# sys.argv - command line arguments
# sys.exit() - exit program

# math - mathematical functions
import math
print(f"Pi: {math.pi}")
print(f"Square root: {math.sqrt(16)}")
# math.sin(), math.cos(), math.tan() - trigonometric functions
# math.log(), math.exp() - logarithmic and exponential functions

# datetime - date and time
import datetime
now = datetime.datetime.now()
print(f"Current time: {now}")
today = datetime.date.today()
print(f"Today: {today}")
# datetime.timedelta - time differences
# datetime.strftime() - format dates

# random - random number generation
import random
print(f"Random number: {random.randint(1, 100)}")
print(f"Random choice: {random.choice(['apple', 'banana', 'cherry'])}")
# random.random() - random float between 0 and 1
# random.shuffle() - shuffle list

# json - JSON encoder/decoder
import json
data = {"name": "John", "age": 30}
json_str = json.dumps(data)
print(f"JSON string: {json_str}")
data_parsed = json.loads(json_str)
print(f"Parsed data: {data_parsed}")

# csv - CSV file handling
import csv
# with open('data.csv', 'r') as file:
#     reader = csv.reader(file)
#     for row in reader:
#         print(row)

# re - regular expressions
import re
text = "Hello, my email is user@example.com"
email = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
if email:
    print(f"Found email: {email.group()}")

# urllib - URL handling
import urllib.request
# response = urllib.request.urlopen('https://www.example.com')
# content = response.read()

# collections - specialized container datatypes
from collections import Counter, defaultdict, deque
counter = Counter(['apple', 'banana', 'apple', 'cherry'])
print(f"Counter: {counter}")  # Output: Counter({'apple': 2, 'banana': 1, 'cherry': 1})


# ============================================================================
# 5. CREATING A PACKAGE
# ============================================================================

"""
Packages are directories containing multiple modules.
They help organize related modules together.
"""

# Creating a package:
# 1. Create a directory with __init__.py file
# 2. Place modules inside the directory
# 3. Package structure:
#    my_package/
#        __init__.py
#        module1.py
#        module2.py

# Example package structure:
"""
my_package/
    __init__.py          # Makes directory a package
    math_utils.py        # Module for math utilities
    string_utils.py      # Module for string utilities
    data_utils.py        # Module for data utilities
"""

# __init__.py can be empty or contain initialization code
# It makes Python treat the directory as a package


# ============================================================================
# 6. IMPORTING FROM PACKAGE
# ============================================================================

"""
Packages are imported using dot notation.
"""

# Importing from package
from package_name import module_name
from package_name.module_name import function_name

# Example: Import from package
# from my_package import math_utils
# result = math_utils.add(5, 3)

# Import specific function
# from my_package.math_utils import add, subtract

# Import all from module in package
# from my_package.math_utils import *


# ============================================================================
# 7. __init__.py FILE
# ============================================================================

"""
The __init__.py file makes a directory a Python package.
It can be empty or contain initialization code.
"""

# __init__.py file:
# - Can be empty (just marks directory as package)
# - Can contain initialization code
# - Controls what gets imported with "from package import *"

# Example __init__.py:
"""
# my_package/__init__.py
from .math_utils import add, subtract
from .string_utils import capitalize_all

__all__ = ['add', 'subtract', 'capitalize_all']  # Controls import *
"""

# Then you can use:
# from my_package import add, subtract
# add(5, 3)


# ============================================================================
# 8. __name__ AND __main__
# ============================================================================

"""
__name__ is a special variable that indicates how a module is being used.
If __name__ == "__main__", the script is being run directly.
"""

# __name__ and __main__:
if __name__ == "__main__":
    # code that runs only when script is executed directly
    print("This script is being run directly")
    print("__name__ is:", __name__)
else:
    print("This script is being imported as a module")
    print("__name__ is:", __name__)

# Example: Module with main block
def greet(name):
    """Greet a person"""
    return f"Hello, {name}!"

def main():
    """Main function"""
    print("Running as main program")
    print(greet("World"))

if __name__ == "__main__":
    main()
# When run directly: executes main()
# When imported: main() is not executed


# ============================================================================
# 9. MODULE SEARCH PATH
# ============================================================================

"""
Python searches for modules in specific locations.
"""

# Module search path:
# Python searches for modules in:
# 1. Current directory
# 2. Directories in PYTHONPATH environment variable
# 3. Standard library directories
# 4. Site-packages directory (where pip installs packages)

# Viewing search path
import sys
print("\nPython module search path:")
for path in sys.path:
    print(f"  {path}")


# ============================================================================
# 10. INSTALLING PACKAGES
# ============================================================================

"""
Third-party packages are installed using pip (Python package installer).
"""

# Installing packages:
# pip install package_name
# pip install package_name==version
# pip uninstall package_name
# pip list - shows installed packages
# pip show package_name - shows package info
# pip freeze - shows installed packages with versions

# Example commands (commented out - don't run automatically):
# pip install numpy
# pip install requests==2.28.0
# pip install pandas matplotlib
# pip uninstall package_name
# pip list
# pip show numpy
# pip freeze > requirements.txt  # Save dependencies

# Requirements file (requirements.txt):
"""
numpy==1.24.0
pandas==2.0.0
matplotlib==3.7.0
requests==2.28.0
"""

# Install from requirements file:
# pip install -r requirements.txt


# ============================================================================
# 11. PRACTICAL EXAMPLES
# ============================================================================

# Example 1: Using standard library modules
import datetime
import random
import math

# Get current date
today = datetime.date.today()
print(f"\nToday: {today}")

# Generate random number
random_num = random.randint(1, 100)
print(f"Random number: {random_num}")

# Calculate circle area
radius = 5
area = math.pi * radius ** 2
print(f"Circle area (radius {radius}): {area:.2f}")

# Example 2: Creating and using a simple module
# Save this as utils.py:
"""
# utils.py
def greet(name):
    return f"Hello, {name}!"

def add(a, b):
    return a + b
"""

# Then use it:
# import utils
# print(utils.greet("Alice"))
# print(utils.add(5, 3))

# Example 3: Package structure example
# my_package/
#     __init__.py
#     math_ops.py
#     string_ops.py

# math_ops.py:
"""
def add(a, b):
    return a + b

def multiply(a, b):
    return a * b
"""

# string_ops.py:
"""
def uppercase(text):
    return text.upper()

def lowercase(text):
    return text.lower()
"""

# __init__.py:
"""
from .math_ops import add, multiply
from .string_ops import uppercase, lowercase

__all__ = ['add', 'multiply', 'uppercase', 'lowercase']
"""

# Usage:
# from my_package import add, uppercase
# print(add(5, 3))
# print(uppercase("hello"))

# Example 4: Conditional imports
try:
    import numpy as np
    print("NumPy is installed")
    # Use NumPy
except ImportError:
    print("NumPy is not installed")
    # Fallback to standard library

# Example 5: Module aliasing for clarity
import datetime as dt
from datetime import timedelta

now = dt.datetime.now()
tomorrow = now + timedelta(days=1)
print(f"\nNow: {now}")
print(f"Tomorrow: {tomorrow}")

# Example 6: Using __name__ for testing
def calculate_area(length, width):
    """Calculate rectangle area"""
    return length * width

def test_calculate_area():
    """Test function"""
    assert calculate_area(5, 3) == 15
    assert calculate_area(10, 10) == 100
    print("All tests passed!")

if __name__ == "__main__":
    test_calculate_area()
    # This code only runs when script is executed directly
    # Not when imported as a module

print("\nModules and packages examples completed.")
