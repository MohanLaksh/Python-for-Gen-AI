# ============================================================================
# LIST COMPREHENSIONS IN PYTHON
# ============================================================================

"""
List comprehensions provide a concise and readable way to create lists.
They are more Pythonic and often faster than equivalent loops.
They can also be used for dictionaries and sets.
"""

# ============================================================================
# 1. BASIC LIST COMPREHENSION
# ============================================================================

"""
Basic syntax: [expression for item in iterable]
Creates a new list by applying expression to each item.
"""

# Basic list comprehension
squares = [x**2 for x in range(10)]
print(f"Squares: {squares}")  # Output: [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

# Equivalent loop
squares_loop = []
for x in range(10):
    squares_loop.append(x**2)
print(f"Squares (loop): {squares_loop}")

# Example: Convert to uppercase
words = ["hello", "world", "python"]
uppercase = [word.upper() for word in words]
print(f"Uppercase: {uppercase}")  # Output: ['HELLO', 'WORLD', 'PYTHON']

uppercase_loop = []
for word in words:
    uppercase_loop.append(word.upper())
print(f"Uppercase (loop): {uppercase_loop}")

# Example: Extract first character
words = ["apple", "banana", "cherry"]
first_chars = [word[0] for word in words]
print(f"First characters: {first_chars}")  # Output: ['a', 'b', 'c']


# ============================================================================
# 2. LIST COMPREHENSION WITH CONDITION
# ============================================================================

"""
Syntax: [expression for item in iterable if condition]
Only includes items that meet the condition.
"""

# List comprehension with condition
evens = [x for x in range(10) if x % 2 == 0]
print(f"Even numbers: {evens}")  # Output: [0, 2, 4, 6, 8]

# Equivalent loop
evens_loop = []
for x in range(10):
    if x % 2 == 0:
        evens_loop.append(x)
print(f"Even numbers (loop): {evens_loop}")

# Example: Filter positive numbers
numbers = [-5, -2, 0, 3, 7, -1, 9]
positives = [x for x in numbers if x > 0]
print(f"Positive numbers: {positives}")  # Output: [3, 7, 9]

# Example: Filter strings by length
words = ["apple", "pie", "banana", "kiwi", "cherry"]
long_words = [word for word in words if len(word) > 4]
print(f"Long words: {long_words}")  # Output: ['apple', 'banana', 'cherry']

# Example: Extract numbers divisible by 3
numbers = range(1, 20)
divisible_by_3 = [x for x in numbers if x % 3 == 0]
print(f"Divisible by 3: {divisible_by_3}")  # Output: [3, 6, 9, 12, 15, 18]


# ============================================================================
# 3. LIST COMPREHENSION WITH IF-ELSE
# ============================================================================

"""
Syntax: [expression_if_true if condition else expression_if_false for item in iterable]
Applies different expressions based on condition.
"""

# List comprehension with if-else
result = [x if x % 2 == 0 else x*2 for x in range(10)]
print(f"Result: {result}")  # Output: [0, 2, 2, 6, 4, 10, 6, 14, 8, 18]
# Even numbers stay the same, odd numbers are doubled


# Equivalent loop
result_loop = []
for x in range(10):
    if x % 2 == 0:
        result_loop.append(x)
    else:
        result_loop.append(x * 2)
print(f"Result (loop): {result_loop}")

# Example: Mark positive/negative
numbers = [-5, -2, 0, 3, 7, -1, 9]
labels = ["positive" if x > 0 else "negative" if x < 0 else "zero" for x in numbers]
print(f"Labels: {labels}")  # Output: ['negative', 'negative', 'zero', 'positive', ...]

# Example: Square evens, cube odds
numbers = range(1, 11)
transformed = [x**2 if x % 2 == 0 else x**3 for x in numbers]
print(f"Transformed: {transformed}")


# ============================================================================
# 4. NESTED LIST COMPREHENSION
# ============================================================================

"""
Nested comprehensions create lists of lists (matrices).
Syntax: [[expression for inner_item in inner_iterable] for outer_item in outer_iterable]
"""

# Nested list comprehension
matrix = [[i*j for j in range(3)] for i in range(3)] 
print(f"Matrix: {matrix}")  # Output: [[0, 0, 0], [0, 1, 2], [0, 2, 4]]

# Equivalent nested loops
matrix_loop = []
for i in range(3): # [0, 1, 2]
    row = []
    for j in range(3): # [0, 1, 2]
        row.append(i * j)
    matrix_loop.append(row)
print(f"Matrix (loop): {matrix_loop}")

# Example: Multiplication table
multiplication_table = [[i * j for j in range(1, 6)] for i in range(1, 6)]
print("\nMultiplication table:")
for row in multiplication_table:
    print(f"  {row}")

# Example: Flatten nested list
nested = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flattened = [item for sublist in nested for item in sublist]
print(f"Flattened: {flattened}")  # Output: [1, 2, 3, 4, 5, 6, 7, 8, 9]

# Example: All pairs
pairs = [(x, y) for x in [1, 2, 3] for y in [4, 5, 6]]
print(f"Pairs: {pairs}")  # Output: [(1, 4), (1, 5), (1, 6), (2, 4), ...]


# ============================================================================
# 5. LIST COMPREHENSION WITH MULTIPLE ITERABLES
# ============================================================================

"""
You can iterate over multiple iterables simultaneously.
"""

# Multiple iterables
pairs = [(x, y) for x in [1, 2, 3] for y in [4, 5, 6]]
print(f"Pairs: {pairs}")

# With condition
pairs_filtered = [(x, y) for x in [1, 2, 3] for y in [4, 5, 6] if x != y]
print(f"Filtered pairs: {pairs_filtered}")

# Example: Cartesian product
colors = ["red", "green", "blue"]
sizes = ["S", "M", "L"]
combinations = [(color, size) for color in colors for size in sizes]
print(f"Color-size combinations: {combinations}")


# ============================================================================
# 6. DICTIONARY COMPREHENSION
# ============================================================================

"""
Dictionary comprehensions create dictionaries concisely.
Syntax: {key_expression: value_expression for item in iterable}
"""

# Basic dictionary comprehension
squares_dict = {x: x**2 for x in range(5)}
print(f"Squares dict: {squares_dict}")  # Output: {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

# With condition
evens_dict = {x: x**2 for x in range(10) if x % 2 == 0}
print(f"Even squares: {evens_dict}")  # Output: {0: 0, 2: 4, 4: 16, 6: 36, 8: 64}

# Example: Word length dictionary
words = ["apple", "pie", "banana", "kiwi"]
word_lengths = {word: len(word) for word in words}
print(f"Word lengths: {word_lengths}")  # Output: {'apple': 5, 'pie': 3, 'banana': 6, 'kiwi': 4}

# Example: Swap keys and values
original = {"a": 1, "b": 2, "c": 3}
swapped = {v: k for k, v in original.items()}
print(f"Swapped: {swapped}")  # Output: {1: 'a', 2: 'b', 3: 'c'}

# Example: Filter dictionary
scores = {"Alice": 85, "Bob": 92, "Charlie": 78, "David": 95}
high_scores = {name: score for name, score in scores.items() if score > 80}
print(f"High scores: {high_scores}")  # Output: {'Alice': 85, 'Bob': 92, 'David': 95}


# ============================================================================
# 7. SET COMPREHENSION
# ============================================================================

"""
Set comprehensions create sets concisely.
Syntax: {expression for item in iterable}
"""

# Basic set comprehension
unique_squares = {x**2 for x in [-2, -1, 0, 1, 2]}
print(f"Unique squares: {unique_squares}")  # Output: {0, 1, 4}
# Note: Sets automatically remove duplicates

# With condition
unique_evens = {x for x in range(20) if x % 2 == 0}
print(f"Unique evens: {unique_evens}")  # Output: {0, 2, 4, 6, 8, 10, 12, 14, 16, 18}

# Example: Unique first letters
words = ["apple", "banana", "apricot", "cherry", "blueberry"]
first_letters = {word[0] for word in words}
print(f"First letters: {first_letters}")  # Output: {'a', 'b', 'c'}

# Example: Remove duplicates from list
numbers = [1, 2, 2, 3, 3, 3, 4, 5]
unique = {x for x in numbers}
print(f"Unique numbers: {unique}")  # Output: {1, 2, 3, 4, 5}


# ============================================================================
# 8. GENERATOR EXPRESSION
# ============================================================================

"""
Generator expressions are similar to list comprehensions but lazy (memory efficient).
They use parentheses instead of square brackets.
Syntax: (expression for item in iterable)
"""

# Generator expression (similar to list comprehension but lazy)
squares_gen = (x**2 for x in range(10))
print(f"Generator: {squares_gen}")  # Output: <generator object>
print(f"List from generator: {list(squares_gen)}")  # Convert to list

# Generator expressions are memory efficient
# They don't create the entire list in memory
large_gen = (x**2 for x in range(1000000))  # Doesn't create 1M items in memory

# Example: Sum of squares (memory efficient)
total = sum(x**2 for x in range(100))
print(f"Sum of squares: {total}")  # Output: 328350

# Example: Find first item matching condition
first_even_square = next(x**2 for x in range(10) if x % 2 == 0)
print(f"First even square: {first_even_square}")  # Output: 0


# ============================================================================
# 9. ADVANTAGES OF COMPREHENSIONS
# ============================================================================

"""
Advantages:
- More concise and readable
- Often faster than equivalent loops
- Pythonic way to create lists/dicts/sets
- Can be more expressive
"""

# Comparison: Loop vs Comprehension
# Loop version
result_loop = []
for x in range(10):
    if x % 2 == 0:
        result_loop.append(x**2)

# Comprehension version
result_comp = [x**2 for x in range(10) if x % 2 == 0]

print(f"Loop result: {result_loop}")
print(f"Comprehension result: {result_comp}")
# Both produce same result, but comprehension is more concise


# ============================================================================
# 10. PRACTICAL EXAMPLES
# ============================================================================

# Example 1: Processing data
data = [("Alice", 25), ("Bob", 30), ("Charlie", 35)]
names = [name for name, age in data]
ages = [age for name, age in data]
print(f"Names: {names}")
print(f"Ages: {ages}")

# Example 2: Data transformation
temperatures_c = [0, 10, 20, 30, 40]
temperatures_f = [(temp * 9/5 + 32) for temp in temperatures_c]
print(f"Celsius: {temperatures_c}")
print(f"Fahrenheit: {temperatures_f}")

# Example 3: Filtering and transforming
numbers = range(1, 21)
even_squares = [x**2 for x in numbers if x % 2 == 0]
print(f"Even squares: {even_squares}")

# Example 4: Creating lookup dictionary
students = ["Alice", "Bob", "Charlie"]
student_ids = {name: i+1 for i, name in enumerate(students)}
print(f"Student IDs: {student_ids}")

# Example 5: Matrix operations
matrix1 = [[1, 2], [3, 4]]
matrix2 = [[5, 6], [7, 8]]
# Transpose
transposed = [[row[i] for row in matrix1] for i in range(len(matrix1[0]))]
print(f"Original: {matrix1}")
print(f"Transposed: {transposed}")

# Example 6: Complex filtering
words = ["python", "java", "javascript", "c++", "ruby"]
long_uppercase = [word.upper() for word in words if len(word) > 4]
print(f"Long uppercase words: {long_uppercase}")

# Example 7: Nested data processing
data = [
    {"name": "Alice", "scores": [85, 90, 88]},
    {"name": "Bob", "scores": [92, 87, 95]},
    {"name": "Charlie", "scores": [78, 85, 80]}
]
averages = {item["name"]: sum(item["scores"])/len(item["scores"]) 
            for item in data}
print(f"Student averages: {averages}")

# Example 8: Conditional dictionary
numbers = range(1, 11)
number_types = {x: "even" if x % 2 == 0 else "odd" for x in numbers}
print(f"Number types: {number_types}")
