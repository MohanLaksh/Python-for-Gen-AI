# ============================================================================
# LOOPS IN PYTHON
# ============================================================================

"""
Loops allow you to execute code repeatedly.
Python provides for loops and while loops for iteration.
"""

# ============================================================================
# 1. FOR LOOP
# ============================================================================

"""
The for loop iterates over a sequence (list, tuple, string, etc.).
It executes the code block for each item in the sequence.
"""

# Basic for loop structure
# for item in iterable:
#     # code block
#     pass

# Example: Iterating through a list
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(f"Fruit: {fruit}")
    print(f"Fruit: {fruit}")
    print(f"Fruit: {fruit}")
    print(f"Fruit: {fruit}")    
    print(f"Fruit: {fruit}")
    print(f"Fruit: {fruit}")

print("--------------------------------")
# Example: Iterating through a string
text = "Python"
for char in text:
    print(f"Character: {char}")

# Example: Iterating through a tuple
numbers = (1, 2, 3, 4, 5)
for number in numbers:
    print(f"Number: {number}")


# ============================================================================
# 2. FOR LOOP WITH RANGE
# ============================================================================

"""
range() generates a sequence of numbers.
Commonly used with for loops to iterate a specific number of times.
"""

# range(stop) - generates numbers from 0 to stop-1
for i in range(5):  # 0, 1, 2, 3, 4
    print(f"i = {i}")

# range(start, stop) - generates numbers from start to stop-1
for i in range(1, 6):  # 1, 2, 3, 4, 5
    print(f"i = {i}")

# range(start, stop, step) - generates numbers with step
for i in range(0, 10, 2):  # 0, 2, 4, 6, 8
    print(f"i = {i}")

# Counting backwards
for i in range(10, 0, -1):  # 10, 9, 8, ..., 1
    print(f"Countdown: {i}")

# Example: Sum of numbers
total = 0
for i in range(1, 11):
    total += i
print(f"Sum of 1 to 10: {total}")  # Output: 55


# ============================================================================
# 3. FOR LOOP WITH ENUMERATE
# ============================================================================

"""
enumerate() returns both index and value when iterating.
Useful when you need both the index and the item.
"""

# Basic enumerate
iterable = ["apple", "banana", "cherry"]
for index, value in enumerate(iterable):
    print(f"Index {index}: {value}")

# Example: List with indices
fruits = ["apple", "banana", "cherry"]
print("Fruits list:")
for i, fruit in enumerate(fruits, start=1):  # Start from 1 instead of 0
    print(f"  {i}. {fruit}")

# Example: Finding index of specific item
items = ["apple", "banana", "cherry", "banana"]
for index, item in enumerate(items):
    if item == "banana":
        print(f"Found 'banana' at index {index}")


# ============================================================================
# 4. FOR LOOP WITH ZIP
# ============================================================================

"""
zip() combines multiple iterables element-wise.
Useful for iterating through multiple lists simultaneously.
"""

# Basic zip
list1 = [1, 2, 3]
list2 = ["a", "b", "c"]
for item1, item2 in zip(list1, list2):
    print(f"{item1} -> {item2}")

# Example: Combining names and ages
names = ["Alice", "Bob", "Charlie"]
ages = [25, 30, 35]
for name, age in zip(names, ages):
    print(f"{name} is {age} years old")

# Example: Multiple lists
list1 = [1, 2, 3]
list2 = [10, 20, 30]
list3 = [100, 200, 300]
for a, b, c in zip(list1, list2, list3):
    print(f"Sum: {a + b + c}")

# Note: zip stops at shortest iterable
list1 = [1, 2, 3, 4]
list2 = ["a", "b"]
for item1, item2 in zip(list1, list2):
    print(f"{item1} -> {item2}")  # Only prints 2 pairs


# ============================================================================
# 5. WHILE LOOP
# ============================================================================

"""
The while loop executes code as long as a condition is True.
Be careful to avoid infinite loops!
"""

# Basic while loop structure
# while condition:
#     # code block
#     pass

# Example: Countdown
count = 5
while count > 0:
    print(f"Countdown: {count}")
    count -= 1
print("Blast off!")

# Example: User input validation
# Simulating user input
attempts = 0
max_attempts = 3
correct_password = "secret123"

# In real code, you'd use: password = input("Enter password: ")
password = "wrong"  # Simulating wrong password

while password != correct_password and attempts < max_attempts:
    attempts += 1
    print(f"Attempt {attempts}: Incorrect password")
    # password = input("Enter password: ")  # In real code
    if attempts < max_attempts:
        password = "secret123"  # Simulating correct password on retry

if password == correct_password:
    print("Access granted")
else:
    print("Access denied")

# Example: Sum until condition
total = 0
number = 1
while total < 100:
    total += number
    number += 1
print(f"Sum reached {total} after adding numbers up to {number - 1}")


# ============================================================================
# 6. LOOP CONTROL STATEMENTS
# ============================================================================

"""
break, continue, and pass control loop execution.
"""

# break - exits the loop immediately
print("Break example:")
for i in range(10):
    if i == 5:
        break  # Exit loop when i is 5
    print(f"i = {i}")
# Output: 0, 1, 2, 3, 4

# continue - skips to next iteration
print("\nContinue example:")
for i in range(10):
    if i % 2 == 0:
        continue  # Skip even numbers
    print(f"i = {i}")
# Output: 1, 3, 5, 7, 9

# pass - placeholder (does nothing)
print("\nPass example:")
for i in range(5):
    if i == 2:
        pass  # Do nothing, continue execution
    print(f"i = {i}")
# Output: 0, 1, 2, 3, 4

# Example: Finding first even number
numbers = [1, 3, 5, 8, 9, 10]
for num in numbers:
    if num % 2 == 0:
        print(f"First even number: {num}")
        break

# Example: Skipping specific values
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print("\nOdd numbers only:")
for num in numbers:
    if num % 2 == 0:
        continue  # Skip even numbers
    print(f"  {num}")


# ============================================================================
# 7. NESTED LOOPS
# ============================================================================

"""
Loops can be nested inside other loops.
Useful for working with 2D data structures.
"""

# Basic nested loops
for i in range(3):
    for j in range(3):
        # code block
        print(f"i={i}, j={j}")

# Example: Multiplication table
print("\nMultiplication table (1-5):")
for i in range(1, 6):
    for j in range(1, 6):
        print(f"{i * j:3}", end=" ")  # :3 for formatting
    print()  # New line after each row

# Example: 2D list iteration
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
print("\nMatrix elements:")
for row in matrix:
    for element in row:
        print(f"{element}", end=" ")
    print()

# Example: Finding pairs
numbers = [1, 2, 3, 4]
print("\nAll pairs:")
for i in range(len(numbers)):
    for j in range(i + 1, len(numbers)):
        print(f"({numbers[i]}, {numbers[j]})")


# ============================================================================
# 8. ELSE CLAUSE WITH LOOPS
# ============================================================================

"""
The else clause with loops executes when loop completes normally
(not exited via break).
"""

# For loop with else structure
# for item in iterable:
#     # code block
#     pass
# else:
#     # executed when loop completes normally (not via break)
#     pass

# Example: Searching with else
numbers = [1, 3, 5, 7, 9]
target = 4

for num in numbers:
    if num == target:
        print(f"Found {target}")
        break
else:
    print(f"{target} not found")  # Executes if break never happens

# Example: Prime number check
def is_prime(n):
    """Check if number is prime"""
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    else:
        return True

print("\nPrime check:")
for num in [2, 4, 7, 9, 11]:
    print(f"  {num} is prime: {is_prime(num)}")


# ============================================================================
# 9. PRACTICAL EXAMPLES
# ============================================================================

# Example 1: Sum and average
numbers = [10, 20, 30, 40, 50]
total = 0
for num in numbers:
    total += num
average = total / len(numbers)
print(f"\nNumbers: {numbers}")
print(f"Sum: {total}, Average: {average}")

# Example 2: Finding maximum
numbers = [3, 7, 2, 9, 1, 5]
max_num = numbers[0]
for num in numbers:
    if num > max_num:
        max_num = num
print(f"\nNumbers: {numbers}")
print(f"Maximum: {max_num}")

# Example 3: Factorial
def factorial(n):
    """Calculate factorial"""
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

print(f"\nFactorials:")
for n in range(1, 6):
    print(f"  {n}! = {factorial(n)}")

# Example 4: Fibonacci sequence
def fibonacci(n):
    """Generate first n Fibonacci numbers"""
    fib = [0, 1]
    for i in range(2, n):
        fib.append(fib[i-1] + fib[i-2])
    return fib[:n]

print(f"\nFibonacci sequence (first 10):")
print(f"  {fibonacci(10)}")

# Example 5: Pattern printing
print("\nPattern 1:")
for i in range(1, 6):
    print("*" * i)

print("\nPattern 2:")
for i in range(5, 0, -1):
    print("*" * i)

print("\nPattern 3:")
for i in range(1, 6):
    print(" " * (5 - i) + "*" * i)

# Example 6: Data processing
students = [
    {"name": "Alice", "grades": [85, 90, 88]},
    {"name": "Bob", "grades": [92, 87, 95]},
    {"name": "Charlie", "grades": [78, 85, 80]}
]

print("\nStudent averages:")
for student in students:
    average = sum(student["grades"]) / len(student["grades"])
    print(f"  {student['name']}: {average:.2f}")

# Example 7: Nested data processing
data = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

print("\nSum of each row:")
for row in data:
    row_sum = sum(row)
    print(f"  Row {row}: Sum = {row_sum}")
