# ============================================================================
# TUPLES & SETS IN PYTHON
# ============================================================================

"""
Tuples are ordered, immutable collections of items.
Sets are unordered collections of unique items.
Both are useful for different purposes in Python.
"""

# ============================================================================
# 1. TUPLES
# ============================================================================

"""
Tuples are similar to lists but are immutable (cannot be changed after creation).
They are faster than lists and can be used as dictionary keys.
Use parentheses () to create tuples.
"""

# ============================================================================
# 1.1 TUPLE CREATION
# ============================================================================

# Empty tuple
empty_tuple = ()
print(f"Empty tuple: {empty_tuple}")

# Tuple with values
numbers = (1, 2, 3, 4, 5)
print(f"Numbers tuple: {numbers}")

# Single item tuple (note the comma - required!)
single_item = (1,)
print(f"Single item: {single_item}, Type: {type(single_item)}")

# Without comma, it's not a tuple
not_tuple = (1)
print(f"Without comma: {not_tuple}, Type: {type(not_tuple)}")  # int, not tuple

# Mixed types
mixed = (1, "hello", 3.14, True)
print(f"Mixed tuple: {mixed}")

# Tuple without parentheses (tuple packing)
numbers = 1, 2, 3, 4, 5
print(f"Without parentheses: {numbers}, Type: {type(numbers)}")

# Tuple unpacking
a, b, c = (1, 2, 3)
print(f"Unpacked: a={a}, b={b}, c={c}")


# ============================================================================
# 1.2 TUPLE INDEXING
# ============================================================================

"""
Tuples support indexing and slicing like lists.
"""

numbers = (1, 2, 3, 4, 5)

# Access first element
first = numbers[0]  # 1
print(f"First element: {first}")

# Access last element
last = numbers[-1]  # 5
print(f"Last element: {last}")

# Access by index
print("All elements:")
print(f"  Index 0: {numbers[0]}")
print(f"  Index 1: {numbers[1]}")
print(f"  Index 2: {numbers[2]}")
print(f"  Index 3: {numbers[3]}")
print(f"  Index 4: {numbers[4]}")


# ============================================================================
# 1.3 TUPLE SLICING
# ============================================================================

"""
Tuples support slicing operations.
"""

numbers = (1, 2, 3, 4, 5)

# Get subset
subset = numbers[1:3]  # (2, 3)
print(f"numbers[1:3]: {subset}")

# From start
subset = numbers[:3]   # (1, 2, 3)
print(f"numbers[:3]: {subset}")

# To end
subset = numbers[3:]   # (4, 5)
print(f"numbers[3:]: {subset}")

# Reverse
reversed_tuple = numbers[::-1]  # (5, 4, 3, 2, 1)
print(f"Reversed: {reversed_tuple}")


# ============================================================================
# 1.4 TUPLE METHODS
# ============================================================================

"""
Tuples have only two methods since they are immutable.
"""

numbers = (1, 2, 3, 2, 4, 2)

# .count() - counts occurrences of value
count = numbers.count(2)
print(f"Count of 2 in {numbers}: {count}")  # Output: 3

# .index() - returns index of first occurrence
index = numbers.index(3)
print(f"Index of 3 in {numbers}: {index}")  # Output: 2


# ============================================================================
# 1.5 TUPLE OPERATIONS
# ============================================================================

"""
Tuples support concatenation, repetition, and membership operations.
"""

# Concatenation: (1, 2) + (3, 4)  # (1, 2, 3, 4)
tuple1 = (1, 2)
tuple2 = (3, 4)
combined = tuple1 + tuple2
print(f"Concatenation: {combined}")  # Output: (1, 2, 3, 4)

# Repetition: (1, 2) * 3  # (1, 2, 1, 2, 1, 2)
repeated = (1, 2) * 3
print(f"Repetition: {repeated}")  # Output: (1, 2, 1, 2, 1, 2)

# Membership: 1 in (1, 2, 3)  # True
numbers = (1, 2, 3)
is_member = 1 in numbers
print(f"1 in {numbers}: {is_member}")  # Output: True

# Length
length = len(numbers)
print(f"Length: {length}")  # Output: 3


# ============================================================================
# 1.6 TUPLES ARE IMMUTABLE
# ============================================================================

"""
Tuples cannot be modified after creation.
This makes them hashable and usable as dictionary keys.
"""

numbers = (1, 2, 3)

# These operations will raise errors:
# numbers[0] = 10  # TypeError: 'tuple' object does not support item assignment
# numbers.append(4)  # AttributeError: 'tuple' object has no attribute 'append'
# numbers.remove(2)  # AttributeError: 'tuple' object has no attribute 'remove'

# But you can create a new tuple
new_tuple = numbers + (4, 5)
print(f"Original: {numbers}")
print(f"New tuple: {new_tuple}")


# ============================================================================
# 1.7 TUPLE UNPACKING
# ============================================================================

"""
Tuple unpacking is a powerful feature for assigning multiple values.
"""

# Basic unpacking
x, y, z = (1, 2, 3)
print(f"Unpacked: x={x}, y={y}, z={z}")

# Swapping variables
a, b = 10, 20
print(f"Before swap: a={a}, b={b}")
a, b = b, a
print(f"After swap: a={a}, b={b}")

# Extended unpacking
numbers = (1, 2, 3, 4, 5)
first, *middle, last = numbers
print(f"First: {first}, Middle: {middle}, Last: {last}")

# Function returning multiple values (returns tuple)
# This will be covered in the functions chapter
# For now, just know that tuples can be unpacked
name, age = ("John", 30)
print(f"Name: {name}, Age: {age}")


# ============================================================================
# 2. SETS
# ============================================================================

"""
Sets are unordered collections of unique elements.
They are mutable and support mathematical set operations.
Use curly braces {} or set() constructor to create sets.
"""

# ============================================================================
# 2.1 SET CREATION
# ============================================================================

# Empty set (must use set(), not {})
empty_set = set()
print(f"Empty set: {empty_set}")

# Set with values
numbers = {1, 2, 3, 4, 5}
print(f"Numbers set: {numbers}")

# Mixed types
mixed = {1, "hello", 3.14}
print(f"Mixed set: {mixed}")

# From list (removes duplicates)
numbers_list = [1, 2, 2, 3, 3, 3, 4]
unique_set = set(numbers_list)
print(f"From list {numbers_list}: {unique_set}")  # Output: {1, 2, 3, 4}

# From string (creates set of characters)
char_set = set("hello")
print(f"From 'hello': {char_set}")  # Output: {'h', 'e', 'l', 'o'} (unordered, unique)


# ============================================================================
# 2.2 SET METHODS
# ============================================================================

"""
Sets have methods for adding, removing, and performing set operations.
"""

# .add() - adds element
numbers = {1, 2, 3}
numbers.add(6)
print(f"After add(6): {numbers}")  # Output: {1, 2, 3, 6}

# Adding duplicate (no effect)
numbers.add(2)
print(f"After add(2) (duplicate): {numbers}")  # Output: {1, 2, 3, 6}

# .remove() - removes element (raises error if not found)
numbers = {1, 2, 3, 4}
numbers.remove(3)
print(f"After remove(3): {numbers}")  # Output: {1, 2, 4}

# .discard() - removes element (no error if not found)
numbers = {1, 2, 3, 4}
numbers.discard(3)
print(f"After discard(3): {numbers}")  # Output: {1, 2, 4}

numbers.discard(99)  # No error even though 99 doesn't exist
print(f"After discard(99): {numbers}")  # Output: {1, 2, 4}

# .pop() - removes and returns arbitrary element
numbers = {1, 2, 3, 4, 5}
popped = numbers.pop()
print(f"Popped: {popped}, Remaining: {numbers}")

# .clear() - removes all elements
numbers = {1, 2, 3}
numbers.clear()
print(f"After clear(): {numbers}")  # Output: set()

# .copy() - returns shallow copy
original = {1, 2, 3}
copied = original.copy()
copied.add(4)
print(f"Original: {original}")  # Output: {1, 2, 3}
print(f"Copied: {copied}")  # Output: {1, 2, 3, 4}


# ============================================================================
# 2.3 SET OPERATIONS
# ============================================================================

"""
Sets support mathematical set operations: union, intersection, difference, etc.
"""

set1 = {1, 2, 3}
set2 = {2, 3, 4}

# .union() - returns union of sets
union = set1.union(set2)
print(f"Union of {set1} and {set2}: {union}")  # Output: {1, 2, 3, 4}

# Using | operator
union = set1 | set2
print(f"Using | operator: {union}")  # Output: {1, 2, 3, 4}

# .intersection() - returns intersection of sets
intersection = set1.intersection(set2)
print(f"Intersection of {set1} and {set2}: {intersection}")  # Output: {2, 3}

# Using & operator
intersection = set1 & set2
print(f"Using & operator: {intersection}")  # Output: {2, 3}

# .difference() - returns difference of sets
difference = set1.difference(set2)
print(f"Difference {set1} - {set2}: {difference}")  # Output: {1}

# Using - operator
difference = set1 - set2
print(f"Using - operator: {difference}")  # Output: {1}

# .symmetric_difference() - returns symmetric difference
sym_diff = set1.symmetric_difference(set2)
print(f"Symmetric difference: {sym_diff}")  # Output: {1, 4}

# Using ^ operator
sym_diff = set1 ^ set2
print(f"Using ^ operator: {sym_diff}")  # Output: {1, 4}

# .update() - updates set with union
set1 = {1, 2, 3}
set2 = {3, 4, 5}
set1.update(set2)
print(f"After update: {set1}")  # Output: {1, 2, 3, 4, 5}

# Membership: 1 in {1, 2, 3}  # True
numbers = {1, 2, 3}
is_member = 1 in numbers
print(f"1 in {numbers}: {is_member}")  # Output: True

# Subset and superset
set1 = {1, 2}
set2 = {1, 2, 3}
print(f"{set1} is subset of {set2}: {set1.issubset(set2)}")  # True
print(f"{set2} is superset of {set1}: {set2.issuperset(set1)}")  # True


# ============================================================================
# 2.4 SETS ARE UNORDERED AND UNIQUE
# ============================================================================

"""
Sets don't maintain order and automatically remove duplicates.
"""

# Unordered
my_set = {3, 1, 4, 1, 5, 9, 2, 6}
print(f"Set (unordered, unique): {my_set}")  # Order may vary

# Unique elements
numbers = [1, 2, 2, 3, 3, 3, 4, 5]
unique = set(numbers)
print(f"Original list: {numbers}")
print(f"Unique set: {unique}")  # Output: {1, 2, 3, 4, 5}


# ============================================================================
# 3. PRACTICAL EXAMPLES
# ============================================================================

# Example 1: Using tuples for coordinates
point1 = (10, 20)
point2 = (30, 40)
print(f"\nPoint 1: {point1}")
print(f"Point 2: {point2}")

# Calculate distance (using tuple unpacking)
x1, y1 = point1
x2, y2 = point2
dist = ((x2 - x1)**2 + (y2 - y1)**2)**0.5
print(f"Distance: {dist:.2f}")

# Example 2: Using sets to find unique items
shopping_list = ["apple", "banana", "apple", "cherry", "banana"]
unique_items = set(shopping_list)
print(f"\nShopping list: {shopping_list}")
print(f"Unique items: {unique_items}")

# Example 3: Set operations for data analysis
students_math = {"Alice", "Bob", "Charlie", "David"}
students_science = {"Bob", "Charlie", "Eve", "Frank"}

# Students in both classes
both = students_math & students_science
print(f"\nStudents in both classes: {both}")

# Students only in math
only_math = students_math - students_science
print(f"Students only in math: {only_math}")

# All students
all_students = students_math | students_science
print(f"All students: {all_students}")

# Example 4: Tuple unpacking
person1 = ("Alice", 25)
person2 = ("Bob", 30)
name1, age1 = person1
name2, age2 = person2
print(f"\nPeople:")
print(f"  {name1}: {age1} years old")
print(f"  {name2}: {age2} years old")

# Example 5: Using sets to check for duplicates
numbers1 = [1, 2, 3, 4, 5]
numbers2 = [1, 2, 2, 3, 4]
set1 = set(numbers1)
set2 = set(numbers2)

print(f"\n{numbers1} has duplicates: {len(numbers1) != len(set1)}")  # False
print(f"{numbers2} has duplicates: {len(numbers2) != len(set2)}")  # True

# Example 6: Tuple as dictionary key
locations = {
    (0, 0): "Origin",
    (1, 1): "Point A",
    (2, 2): "Point B"
}
print(f"\nLocations: {locations}")
print(f"Location at (1, 1): {locations[(1, 1)]}")
