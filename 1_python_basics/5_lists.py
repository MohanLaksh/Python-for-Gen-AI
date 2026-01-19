# ============================================================================
# LISTS IN PYTHON
# ============================================================================

"""
Lists are ordered, mutable (changeable) collections of items.
They can contain items of different types and are one of the most
commonly used data structures in Python.
"""

# ============================================================================
# 1. LIST CREATION
# ============================================================================

"""
Lists are created using square brackets [].
They can contain any type of data, including mixed types.
"""

# Empty list
empty_list = []
print(f"Empty list: {empty_list}")

# List with integers
numbers = [1, 2, 3, 4, 5]
print(f"Numbers: {numbers}")

# List with mixed types
mixed = [1, "hello", 3.14, True]
print(f"Mixed types: {mixed}")

# List of strings
fruits = ["apple", "banana", "cherry"]
print(f"Fruits: {fruits}")

# Nested lists (lists within lists)
nested = [[1, 2], [3, 4], [5, 6]]
print(f"Nested list: {nested}")

# Using list() constructor
numbers_from_range = list(range(5))
print(f"From range: {numbers_from_range}")  # Output: [0, 1, 2, 3, 4]


# ============================================================================
# 2. LIST INDEXING
# ============================================================================

"""
Lists are indexed starting from 0.
Negative indices count from the end.
"""

numbers = [1, 2, 3, 4, 5]

# Access first element
first = numbers[0]  # 1
print(f"First element: {first}")

# Access last element
last = numbers[-1]  # 5
print(f"Last element: {last}")

# Access second last element
second_last = numbers[-2]  # 4
print(f"Second last: {second_last}")

# Access all elements by index
print("All elements:")
print(f"  Index 0: {numbers[0]}")
print(f"  Index 1: {numbers[1]}")
print(f"  Index 2: {numbers[2]}")
print(f"  Index 3: {numbers[3]}")
print(f"  Index 4: {numbers[4]}")


# ============================================================================
# 3. LIST SLICING
# ============================================================================

"""
Slicing extracts a portion of a list.
Syntax: list[start:end:step]
"""

numbers = [1, 2, 3, 4, 5]

# Get subset from index 1 to 3 (exclusive)
subset = numbers[1:3]  # [2, 3]
print(f"numbers[1:3]: {subset}")

# From start to index 3
subset = numbers[:3]   # [1, 2, 3]
print(f"numbers[:3]: {subset}")

# From index 3 to end
subset = numbers[3:]   # [4, 5]
print(f"numbers[3:]: {subset}")

# Get all elements
subset = numbers[:]    # [1, 2, 3, 4, 5] (shallow copy)
print(f"numbers[:]: {subset}")

# Negative indices
subset = numbers[-3:]  # [3, 4, 5] (last 3 elements)
print(f"numbers[-3:]: {subset}")

# With step
subset = numbers[::2]  # [1, 3, 5] (every 2nd element)
print(f"numbers[::2]: {subset}")

# Reverse list
reversed_list = numbers[::-1]  # [5, 4, 3, 2, 1]
print(f"Reversed: {reversed_list}")


# ============================================================================
# 4. LIST METHODS
# ============================================================================

"""
Lists have many built-in methods for manipulation.
Most methods modify the list in-place (mutate it).
"""

# .append() - adds element to end
numbers = [1, 2, 3]
numbers.append(6)
print(f"After append(6): {numbers}")  # Output: [1, 2, 3, 6]

# .extend() - extends list with another list
numbers = [1, 2, 3]
numbers.extend([7, 8])
print(f"After extend([7, 8]): {numbers}")  # Output: [1, 2, 3, 7, 8]

# Difference between append and extend
list1 = [1, 2, 3]
list1.append([4, 5])
print(f"append([4, 5]): {list1}")  # Output: [1, 2, 3, [4, 5]]

list2 = [1, 2, 3]
list2.extend([4, 5])
print(f"extend([4, 5]): {list2}")  # Output: [1, 2, 3, 4, 5]

# .insert() - inserts element at index
numbers = [1, 2, 3]
numbers.insert(0, 0)  # Insert 0 at index 0
print(f"After insert(0, 0): {numbers}")  # Output: [0, 1, 2, 3]

numbers.insert(2, 99)  # Insert 99 at index 2
print(f"After insert(2, 99): {numbers}")  # Output: [0, 1, 99, 2, 3]

# .remove() - removes first occurrence of value
numbers = [1, 2, 3, 2]
numbers.remove(3)
print(f"After remove(3): {numbers}")  # Output: [1, 2, 2]

# .pop() - removes and returns element at index (default: last)
numbers = [1, 2, 3, 4, 5]
popped = numbers.pop()  # Removes and returns last element
print(f"Popped: {popped}, List: {numbers}")  # Output: Popped: 5, List: [1, 2, 3, 4]

popped = numbers.pop(0)  # Removes and returns element at index 0
print(f"Popped at index 0: {popped}, List: {numbers}")  # Output: Popped: 1, List: [2, 3, 4]

# .clear() - removes all elements
numbers = [1, 2, 3]
numbers.clear()
print(f"After clear(): {numbers}")  # Output: []

# .index() - returns index of first occurrence
numbers = [1, 2, 3, 2]
index = numbers.index(2)
print(f"Index of 2: {index}")  # Output: 1

# .count() - counts occurrences of value
numbers = [1, 2, 3, 2, 2]
count = numbers.count(2)
print(f"Count of 2: {count}")  # Output: 3

# .sort() - sorts list in place
numbers = [3, 1, 4, 1, 5, 9, 2, 6]
numbers.sort()
print(f"After sort(): {numbers}")  # Output: [1, 1, 2, 3, 4, 5, 6, 9]

# Sort in descending order
numbers.sort(reverse=True)
print(f"After sort(reverse=True): {numbers}")  # Output: [9, 6, 5, 4, 3, 2, 1, 1]

# Sort strings
fruits = ["banana", "apple", "cherry"]
fruits.sort()
print(f"Sorted fruits: {fruits}")  # Output: ['apple', 'banana', 'cherry']

# .reverse() - reverses list in place
numbers = [1, 2, 3, 4, 5]
numbers.reverse()
print(f"After reverse(): {numbers}")  # Output: [5, 4, 3, 2, 1]

# .copy() - returns shallow copy
original = [1, 2, 3]
copied = original.copy()
copied.append(4)
print(f"Original: {original}")  # Output: [1, 2, 3]
print(f"Copied: {copied}")  # Output: [1, 2, 3, 4]


# ============================================================================
# 5. LIST OPERATIONS
# ============================================================================

"""
Lists support various operations like concatenation, repetition, and membership.
"""

# Concatenation: [1, 2] + [3, 4]  # [1, 2, 3, 4]
list1 = [1, 2]
list2 = [3, 4]
combined = list1 + list2
print(f"Concatenation: {combined}")  # Output: [1, 2, 3, 4]

# Repetition: [1, 2] * 3  # [1, 2, 1, 2, 1, 2]
repeated = [1, 2] * 3
print(f"Repetition: {repeated}")  # Output: [1, 2, 1, 2, 1, 2]

# Membership: 1 in [1, 2, 3]  # True
numbers = [1, 2, 3]
is_member = 1 in numbers
print(f"1 in {numbers}: {is_member}")  # Output: True

is_member = 5 in numbers
print(f"5 in {numbers}: {is_member}")  # Output: False

# Length
length = len(numbers)
print(f"Length of {numbers}: {length}")  # Output: 3


# ============================================================================
# 6. PRACTICAL EXAMPLES
# ============================================================================

# Example 1: Shopping list
shopping_list = ["apples", "bananas", "milk"]
print(f"\nShopping list: {shopping_list}")

# Add item
shopping_list.append("bread")
print(f"After adding bread: {shopping_list}")

# Remove item
shopping_list.remove("bananas")
print(f"After removing bananas: {shopping_list}")

# Example 2: Student grades
grades = [85, 92, 78, 96, 88]
print(f"\nGrades: {grades}")
print(f"Highest: {max(grades)}")
print(f"Lowest: {min(grades)}")
print(f"Average: {sum(grades) / len(grades):.2f}")

# Example 3: Matrix (2D list)
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
print(f"\nMatrix:")
print(f"  Row 0: {matrix[0]}")
print(f"  Row 1: {matrix[1]}")
print(f"  Row 2: {matrix[2]}")

# Access element
element = matrix[1][2]  # Row 1, Column 2
print(f"Element at [1][2]: {element}")  # Output: 6

# Example 4: List as stack (LIFO - Last In First Out)
stack = []
stack.append(1)  # Push
stack.append(2)
stack.append(3)
print(f"\nStack after pushes: {stack}")

popped = stack.pop()  # Pop
print(f"Popped: {popped}, Stack: {stack}")
