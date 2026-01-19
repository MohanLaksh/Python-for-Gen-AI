# ============================================================================
# DICTIONARIES IN PYTHON
# ============================================================================

"""
Dictionaries are unordered collections of key-value pairs.
They are mutable and very efficient for lookups.
Keys must be immutable (strings, numbers, tuples).
Values can be any type.
"""

# ============================================================================
# 1. DICTIONARY CREATION
# ============================================================================

"""
Dictionaries are created using curly braces {} or dict() constructor.
Syntax: {key: value, key: value, ...}
"""

# Empty dictionary
empty_dict = {}
print(f"Empty dict: {empty_dict}")

# Dictionary with key-value pairs
person = {"name": "John", "age": 30, "city": "New York"}
print(f"Person: {person}")

# Using dict() constructor
person = dict(name="John", age=30, city="New York")
print(f"Using dict(): {person}")

# From list of tuples
person = dict([("name", "John"), ("age", 30), ("city", "New York")])
print(f"From tuples: {person}")

# Dictionary with different value types
mixed = {
    "name": "Alice",
    "age": 25,
    "grades": [85, 90, 88],
    "is_student": True,
    "address": {"street": "123 Main St", "city": "Boston"}
}
print(f"Mixed types: {mixed}")


# ============================================================================
# 2. ACCESSING VALUES
# ============================================================================

"""
Values are accessed using keys in square brackets or .get() method.
"""

person = {"name": "John", "age": 30}

# Using square brackets
name = person["name"]  # "John"
print(f"Name: {name}")

# Using .get() method (safer - returns None if key doesn't exist)
age = person.get("age")  # 30
print(f"Age: {age}")

# .get() with default value
email = person.get("email", "Not provided")  # Returns default if key doesn't exist
print(f"Email: {email}")

# Accessing nested dictionary
person = {
    "name": "John",
    "address": {"street": "123 Main St", "city": "New York"}
}
city = person["address"]["city"]
print(f"City: {city}")

# Error handling
# person["email"]  # KeyError if key doesn't exist
# Use .get() to avoid errors
email = person.get("email", "No email")
print(f"Email: {email}")


# ============================================================================
# 3. DICTIONARY METHODS
# ============================================================================

"""
Dictionaries have many useful methods for manipulation.
"""

person = {"name": "John", "age": 30, "city": "New York"}

# .keys() - returns all keys (as dict_keys view)
keys = person.keys()
print(f"Keys: {keys}")  # Output: dict_keys(['name', 'age', 'city'])
print(f"Keys as list: {list(keys)}")

# .values() - returns all values (as dict_values view)
values = person.values()
print(f"Values: {values}")  # Output: dict_values(['John', 30, 'New York'])
print(f"Values as list: {list(values)}")

# .items() - returns all key-value pairs (as dict_items view)
items = person.items()
print(f"Items: {items}")  # Output: dict_items([('name', 'John'), ('age', 30), ...])
print(f"Items as list: {list(items)}")

#Iterating through items (will be covered in loops chapter)
for key, value in person.items():
    print(f"  {key}: {value}")

# .get() - gets value by key (with optional default)
name = person.get("name")
print(f"Name: {name}")

email = person.get("email", "No email")
print(f"Email: {email}")

# .pop() - removes and returns value by key
person = {"name": "John", "age": 30, "city": "New York"}
age = person.pop("age")
print(f"Popped age: {age}, Remaining: {person}")

# .pop() with default (no error if key doesn't exist)
value = person.pop("email", "Not found")
print(f"Popped email: {value}")

# .popitem() - removes and returns last key-value pair (Python 3.7+)
person = {"name": "John", "age": 30, "city": "New York"}
item = person.popitem()
print(f"Popped item: {item}, Remaining: {person}")

# .update() - updates dictionary with another dictionary
person = {"name": "John", "age": 30}
person.update({"email": "john@example.com", "city": "New York"})
print(f"After update: {person}")

# .clear() - removes all items
person = {"name": "John", "age": 30}
person.clear()
print(f"After clear: {person}")  # Output: {}

# .copy() - returns shallow copy
original = {"name": "John", "age": 30}
copied = original.copy()
copied["age"] = 31
print(f"Original: {original}")  # Output: {'name': 'John', 'age': 30}
print(f"Copied: {copied}")  # Output: {'name': 'John', 'age': 31}

# .setdefault() - gets value or sets default if key doesn't exist
person = {"name": "John", "age": 30}
name = person.setdefault("name", "Unknown")
print(f"Name: {name}")  # Output: John (key exists)

phone = person.setdefault("phone", "123-456-7890")
print(f"Phone: {phone}")  # Output: 123-456-7890 (key didn't exist, set default)
print(f"Person: {person}")


# ============================================================================
# 4. ADDING/UPDATING ITEMS
# ============================================================================

"""
Items can be added or updated using square bracket notation.
"""

person = {"name": "John", "age": 30}

# Adding new key-value pair
person["email"] = "john@example.com"  # add new key-value
print(f"After adding email: {person}")

# Updating existing value
person["age"] = 31  # update existing value
print(f"After updating age: {person}")

# Adding multiple items
person.update({"city": "New York", "country": "USA"})
print(f"After update: {person}")


# ============================================================================
# 5. DICTIONARY OPERATIONS
# ============================================================================

"""
Dictionaries support membership testing and length operations.
"""

person = {"name": "John", "age": 30, "city": "New York"}

# Membership: "name" in person  # True (checks keys)
is_key = "name" in person
print(f"'name' in person: {is_key}")  # Output: True

is_key = "email" in person
print(f"'email' in person: {is_key}")  # Output: False

# Check values
is_value = "John" in person.values()
print(f"'John' in person.values(): {is_value}")  # Output: True

# Length: len(person)  # number of key-value pairs
length = len(person)
print(f"Length: {length}")  # Output: 3

# Delete item
del person["age"]
print(f"After deleting 'age': {person}")


# ============================================================================
# 6. NESTED DICTIONARIES
# ============================================================================

"""
Dictionaries can contain other dictionaries (nested dictionaries).
"""

# Nested dictionary
students = {
    "student1": {"name": "Alice", "age": 20, "grades": [85, 90, 88]},
    "student2": {"name": "Bob", "age": 21, "grades": [92, 87, 95]},
    "student3": {"name": "Charlie", "age": 19, "grades": [78, 85, 80]}
}

print("Nested dictionary:")
print(f"  student1: {students['student1']['name']}, Age: {students['student1']['age']}")
print(f"  student2: {students['student2']['name']}, Age: {students['student2']['age']}")
print(f"  student3: {students['student3']['name']}, Age: {students['student3']['age']}")

# Accessing nested values
alice_grades = students["student1"]["grades"]
print(f"Alice's grades: {alice_grades}")

# Updating nested dictionary
students["student1"]["age"] = 21
print(f"Updated Alice's age: {students['student1']['age']}")


# ============================================================================
# 7. PRACTICAL EXAMPLES
# ============================================================================

# Example 1: Student gradebook
gradebook = {
    "Alice": {"math": 85, "science": 90, "english": 88},
    "Bob": {"math": 92, "science": 87, "english": 95},
    "Charlie": {"math": 78, "science": 85, "english": 80}
}

print(f"\nGradebook:")
alice_grades = gradebook["Alice"]
alice_avg = (alice_grades["math"] + alice_grades["science"] + alice_grades["english"]) / 3
print(f"  Alice: {alice_grades}, Average: {alice_avg:.2f}")

bob_grades = gradebook["Bob"]
bob_avg = (bob_grades["math"] + bob_grades["science"] + bob_grades["english"]) / 3
print(f"  Bob: {bob_grades}, Average: {bob_avg:.2f}")

# Example 2: Configuration settings
config = {
    "database": {
        "host": "localhost",
        "port": 5432,
        "name": "mydb"
    },
    "api": {
        "timeout": 30,
        "retries": 3
    }
}

print(f"\nConfiguration:")
print(f"Database host: {config['database']['host']}")
print(f"API timeout: {config['api']['timeout']}")

# Example 3: Dictionary as lookup table
days = {
    1: "Monday",
    2: "Tuesday",
    3: "Wednesday",
    4: "Thursday",
    5: "Friday",
    6: "Saturday",
    7: "Sunday"
}

day_number = 3
day_name = days.get(day_number, "Invalid day")
print(f"\nDay lookup:")
print(f"  Day {day_number}: {day_name}")

# Example 4: Merging dictionaries
dict1 = {"a": 1, "b": 2}
dict2 = {"c": 3, "d": 4}

# Method 1: Using update()
merged1 = dict1.copy()
merged1.update(dict2)
print(f"\nMerged (update): {merged1}")

# Method 2: Using ** operator (Python 3.5+)
merged2 = {**dict1, **dict2}
print(f"Merged (**): {merged2}")
