# ============================================================================
# EXCEPTION HANDLING IN PYTHON
# ============================================================================

"""
Exception handling allows you to gracefully handle errors in your code.
Python uses try-except blocks to catch and handle exceptions.
Proper error handling makes programs more robust and user-friendly.
"""

# ============================================================================
# 1. TRY-EXCEPT BLOCK
# ============================================================================

"""
The try-except block catches exceptions and handles them.
Code in try block is executed, if exception occurs, except block runs.
"""

# Basic try-except block
from curses import A_ALTCHARSET
from re import A


try:
    # code that might raise an exception
    result = 10 / 0

except Exception:
    # code to handle the exception
    print("An error occurred")

# Example: Division by zero
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero!")

# Example: File not found
try:
    with open("nonexistent.txt", "r") as file:
        content = file.read()
except FileNotFoundError:
    print("File not found!")

# Example: Type error
try:
    result = "hello" + 5
except TypeError:
    print("Cannot concatenate string and integer!")


# ============================================================================
# 2. TRY-EXCEPT-ELSE BLOCK
# ============================================================================

"""
The else block executes only if no exception occurred in try block.
"""

# Try-except-else block
try:
    # code that might raise an exception
    result = 10 / 2
except ZeroDivisionError:
    # code to handle the exception
    print("Cannot divide by zero!")
else:
    # code that runs if no exception occurred
    print(f"Result: {result}")

# Example: File reading
try:
    # Simulating file read
    content = "File content"
    print("File read successfully")
except FileNotFoundError:
    print("File not found!")
else:
    print(f"Content: {content}")

# Example: User input validation
try:
    number = int("123")  # Valid conversion
except ValueError:
    print("Invalid number!")
else:
    print(f"Number: {number}")


# ============================================================================
# 3. TRY-EXCEPT-FINALLY BLOCK
# ============================================================================

"""
The finally block always executes, regardless of whether exception occurred.
Useful for cleanup operations (closing files, releasing resources).
"""

# Try-except-finally block
try:
    # code that might raise an exception
    result = 10 / 2
except ZeroDivisionError:
    # code to handle the exception
    print("Cannot divide by zero!")
finally:
    # code that always runs
    print("This always executes")

# Example: File handling with finally
file = None
try:
    # file = open("example.txt", "r")
    # content = file.read()
    print("File operations")
except FileNotFoundError:
    print("File not found!")
finally:
    if file:
        file.close()  # Always close file
    print("Cleanup completed")

# Example: Resource cleanup
resource = "opened"
try:
    # Use resource
    result = 10 / 2
except ZeroDivisionError:
    print("Error occurred")
finally:
    resource = "closed"  # Always cleanup
    print(f"Resource: {resource}")


# ============================================================================
# 4. MULTIPLE EXCEPT CLAUSES
# ============================================================================

"""
You can handle different exceptions with multiple except clauses.
More specific exceptions should come before general ones.
"""

# Multiple except clauses
try:
    # code that might raise different exceptions
    pass
except ValueError:
    # Handle ValueError
    print("Value error occurred")
except TypeError:
    # Handle TypeError
    print("Type error occurred")
except Exception:
    # Handle any other exception (should be last)
    print("Other error occurred")

# Example: Multiple exception handling
def divide_numbers(a, b):
    """Divide two numbers with error handling"""
    try:
        result = a / b
        return result
    except ZeroDivisionError:
        print("Cannot divide by zero!")
        return None
    except TypeError:
        print("Invalid types for division!")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

print(divide_numbers(10, 2))  # Output: 5.0
print(divide_numbers(10, 0))  # Output: Cannot divide by zero!
print(divide_numbers("10", 2))  # Output: Invalid types for division!

# Example: File operations
try:
    # file = open("data.txt", "r")
    # number = int(file.read())
    number = int("123")
    result = 100 / number
except FileNotFoundError:
    print("File not found!")
except ValueError:
    print("Invalid number format!")
except ZeroDivisionError:
    print("Cannot divide by zero!")
except Exception as e:
    print(f"Unexpected error: {e}")


# ============================================================================
# 5. CATCHING EXCEPTION WITH VARIABLE
# ============================================================================

"""
You can catch the exception object to get more information about the error.
"""

# Catching exception with variable
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f"Error: {e}")  # Output: Error: division by zero

# Example: Getting error message
try:
    number = int("abc")
except ValueError as e:
    print(f"ValueError: {e}")  # Output: ValueError: invalid literal for int() with base 10: 'abc'

# Example: Accessing exception attributes
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f"Exception type: {type(e).__name__}")
    print(f"Exception message: {str(e)}")
    print(f"Exception args: {e.args}")

# Example: Logging exceptions
try:
    result = 10 / 0
except Exception as e:
    error_msg = f"Error occurred: {type(e).__name__}: {str(e)}"
    print(error_msg)
    # In real code, you might log this to a file


# ============================================================================
# 6. RAISING EXCEPTIONS
# ============================================================================

"""
You can raise exceptions manually using the raise statement.
Useful for validating input or indicating error conditions.
"""

# Raising exceptions
#raise ValueError("Error message")
#raise Exception("Error message")

# Example: Input validation
def validate_age(age):
    """Validate age input"""
    if age < 0:
        raise ValueError("Age cannot be negative")
    if age > 150:
        raise ValueError("Age seems unrealistic")
    return True

try:
    validate_age(-5)
except ValueError as e:
    print(f"Validation error: {e}")

# Example: Custom error conditions
def divide(a, b):
    """Divide with custom error messages"""
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero!")
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Both arguments must be numbers")
    return a / b

try:
    result = divide(10, 0)
except (ZeroDivisionError, TypeError) as e:
    print(f"Error: {e}")

# Example: Re-raising exceptions
try:
    try:
        result = 10 / 0
    except ZeroDivisionError:
        print("Caught division by zero, re-raising...")
        raise  # Re-raise the same exception
except ZeroDivisionError:
    print("Caught re-raised exception")


# ============================================================================
# 7. CUSTOM EXCEPTIONS
# ============================================================================

"""
You can create custom exception classes by inheriting from Exception.
Useful for application-specific error handling.
"""

# Custom exception class
class CustomError(Exception):
    """Custom exception class"""
    pass

# Raising custom exception
raise CustomError("Custom error message")

# Example: Custom exception with attributes
class ValidationError(Exception):
    """Custom validation error"""
    def __init__(self, message, field):
        self.message = message
        self.field = field
        super().__init__(f"{message} (field: {field})")

# Using custom exception
try:
    raise ValidationError("Invalid value", "email")
except ValidationError as e:
    print(f"Error: {e}")
    print(f"Field: {e.field}")

# Example: Application-specific exceptions
class InsufficientFundsError(Exception):
    """Raised when account has insufficient funds"""
    pass

class InvalidAccountError(Exception):
    """Raised when account is invalid"""
    pass

def withdraw(account, amount):
    """Withdraw money with custom exceptions"""
    if account is None:
        raise InvalidAccountError("Account does not exist")
    if account.balance < amount:
        raise InsufficientFundsError(f"Insufficient funds. Balance: {account.balance}")
    account.balance -= amount
    return account.balance

# Example usage (with mock account)
class Account:
    def __init__(self, balance):
        self.balance = balance

account = Account(100)
try:
    withdraw(account, 150)
except InsufficientFundsError as e:
    print(f"Withdrawal failed: {e}")


# ============================================================================
# 8. COMMON BUILT-IN EXCEPTIONS
# ============================================================================

"""
Python has many built-in exceptions for different error types.
"""

# ValueError - wrong value type
try:
    int("abc")
except ValueError as e:
    print(f"ValueError: {e}")

# TypeError - wrong type
try:
    "hello" + 5
except TypeError as e:
    print(f"TypeError: {e}")

# IndexError - index out of range
try:
    numbers = [1, 2, 3]
    value = numbers[10]
except IndexError as e:
    print(f"IndexError: {e}")

# KeyError - key not found in dictionary
try:
    person = {"name": "John"}
    age = person["age"]
except KeyError as e:
    print(f"KeyError: {e}")

# FileNotFoundError - file not found
try:
    with open("nonexistent.txt", "r") as file:
        content = file.read()
except FileNotFoundError as e:
    print(f"FileNotFoundError: {e}")

# ZeroDivisionError - division by zero
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f"ZeroDivisionError: {e}")

# AttributeError - attribute not found
try:
    obj = None
    value = obj.attribute
except AttributeError as e:
    print(f"AttributeError: {e}")

# NameError - name not defined
try:
    print(undefined_variable)
except NameError as e:
    print(f"NameError: {e}")


# ============================================================================
# 9. PRACTICAL EXAMPLES
# ============================================================================

# Example 1: Safe division function
def safe_divide(a, b):
    """Safely divide two numbers"""
    try:
        return a / b
    except ZeroDivisionError:
        return "Cannot divide by zero"
    except TypeError:
        return "Both arguments must be numbers"

print("\nSafe division:")
print(f"  10 / 2 = {safe_divide(10, 2)}")
print(f"  10 / 0 = {safe_divide(10, 0)}")
print(f"  10 / '2' = {safe_divide(10, '2')}")

# Example 2: File reading with error handling
def read_file_safe(filename):
    """Safely read file with error handling"""
    try:
        with open(filename, "r") as file:
            return file.read()
    except FileNotFoundError:
        return f"Error: File '{filename}' not found"
    except PermissionError:
        return f"Error: Permission denied to read '{filename}'"
    except Exception as e:
        return f"Error reading file: {e}"

# Example 3: Input validation
def get_valid_number(prompt):
    """Get valid number from user with error handling"""
    while True:
        try:
            # In real code: number = float(input(prompt))
            number = float("3.14")  # Simulating input
            return number
        except ValueError:
            print("Invalid input! Please enter a number.")
            break  # In real code, would continue loop

# Example 4: Dictionary access with defaults
def safe_dict_access(dictionary, key, default=None):
    """Safely access dictionary key"""
    try:
        return dictionary[key]
    except KeyError:
        return default

person = {"name": "John", "age": 30}
print(f"\nSafe dictionary access:")
print(f"  Name: {safe_dict_access(person, 'name', 'Unknown')}")
print(f"  Email: {safe_dict_access(person, 'email', 'Not provided')}")

# Example 5: List operations with error handling
def safe_list_access(lst, index, default=None):
    """Safely access list element"""
    try:
        return lst[index]
    except IndexError:
        return default

numbers = [1, 2, 3, 4, 5]
print(f"\nSafe list access:")
print(f"  Index 2: {safe_list_access(numbers, 2)}")
print(f"  Index 10: {safe_list_access(numbers, 10, 'Index out of range')}")

# Example 6: Comprehensive error handling
def process_data(data):
    """Process data with comprehensive error handling"""
    try:
        # Validate input
        if not isinstance(data, (list, tuple)):
            raise TypeError("Data must be a list or tuple")
        
        # Process data
        result = sum(data) / len(data)
        return result
    except TypeError as e:
        print(f"Type error: {e}")
        return None
    except ZeroDivisionError:
        print("Error: Cannot calculate average of empty sequence")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

print(f"\nProcess data:")
print(f"  Average: {process_data([1, 2, 3, 4, 5])}")
print(f"  Average: {process_data([])}")
print(f"  Average: {process_data('invalid')}")

# Example 7: Context manager with exception handling
class ResourceManager:
    """Simple resource manager"""
    def __enter__(self):
        print("Resource acquired")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Resource released")
        if exc_type:
            print(f"Exception occurred: {exc_type.__name__}")
        return False  # Don't suppress exception

with ResourceManager():
    print("Using resource")
    # If exception occurs, resource is still released

print("\nException handling examples completed.")
