# ============================================================================
# STRINGS IN PYTHON
# ============================================================================

"""
Strings are sequences of characters used to represent text.
Python strings are immutable (cannot be changed after creation).
Strings support many methods for manipulation and formatting.
"""

# ============================================================================
# 1. STRING CREATION
# ============================================================================

"""
Strings can be created using single quotes, double quotes, or triple quotes.
Triple quotes are useful for multi-line strings.
"""

# Single quotes
single_quotes = 'Hello'
print(f"Single quotes: {single_quotes}")

# Double quotes
double_quotes = "World"
print(f"Double quotes: {double_quotes}")

# Triple quotes for multi-line strings
triple_quotes = """Multi-line
string"""
print(f"Triple quotes:\n{triple_quotes}")

# Triple quotes preserve formatting
formatted_text = """
    This is a
    multi-line string
    with indentation
"""
print(f"Formatted text:{formatted_text}")

# Escaping characters
escaped = "He said \"Hello\""
print(f"Escaped quotes: {escaped}")

# Raw strings (r prefix) - ignores escape sequences
raw_string = r"C:\Users\Documents\file.txt"
print(f"Raw string: {raw_string}")


# ============================================================================
# 2. STRING CONCATENATION
# ============================================================================

"""
Concatenation combines multiple strings into one.
Use + operator or join() method.
"""

# Using + operator
full_name = "John" + " " + "Doe"
print(f"Concatenation: {full_name}")  # Output: John Doe

# Concatenating variables
first = "Hello"
second = "World"
greeting = first + " " + second
print(f"Greeting: {greeting}")  # Output: Hello World

# Multiple concatenations
result = "Python" + " is " + "awesome"
print(f"Result: {result}")  # Output: Python is awesome


# ============================================================================
# 3. STRING REPETITION
# ============================================================================

"""
Use * operator to repeat strings.
"""

# Repeat string multiple times
repeated = "Hello" * 3
print(f"Repeated: {repeated}")  # Output: HelloHelloHello

# With spaces
separator = "-" * 20
print(f"Separator: {separator}")  # Output: --------------------


# ============================================================================
# 4. STRING INDEXING
# ============================================================================

"""
Strings are sequences, so you can access individual characters by index.
Indexing starts at 0. Negative indices count from the end.
"""

text = "Python"
first_char = text[0]  # 'P'
print(f"First character: {first_char}")

second_char = text[1]  # 'y'
print(f"Second character: {second_char}")

last_char = text[-1]  # 'n' (last character)
print(f"Last character: {last_char}")

second_last = text[-2]  # 'o'
print(f"Second last: {second_last}")

# Accessing all characters
print("All characters:")
for i in range(len(text)):
    print(f"  Index {i}: {text[i]}")


# ============================================================================
# 5. STRING SLICING
# ============================================================================

"""
Slicing extracts a substring from a string.
Syntax: string[start:end:step]
- start: inclusive (default: 0)
- end: exclusive (default: end of string)
- step: increment (default: 1)
"""

text = "Python"

# Get substring from index 0 to 3 (exclusive)
substring = text[0:3]  # 'Pyt'
print(f"text[0:3]: {substring}")

# From start to index 3
substring = text[:3]   # 'Pyt' (same as text[0:3])
print(f"text[:3]: {substring}")

# From index 3 to end
substring = text[3:]   # 'hon'
print(f"text[3:]: {substring}")

# Get all characters
substring = text[:]    # 'Python'
print(f"text[:]: {substring}")

# Negative indices
substring = text[-3:]  # 'hon' (last 3 characters)
print(f"text[-3:]: {substring}")

# With step
substring = text[::2]  # 'Pto' (every 2nd character)
print(f"text[::2]: {substring}")

# Reverse string
reversed_text = text[::-1]  # 'nohtyP'
print(f"Reversed: {reversed_text}")

# Complex slicing
substring = text[1:5:2]  # 'yh' (from index 1 to 5, step 2)
print(f"text[1:5:2]: {substring}")


# ============================================================================
# 6. STRING METHODS
# ============================================================================

"""
String methods return new strings (strings are immutable).
Common methods for case conversion, searching, replacing, etc.
"""

# .upper() - converts to uppercase
text = "hello"
uppercase = text.upper()
print(f"'{text}'.upper(): '{uppercase}'")  # Output: 'HELLO'

# .lower() - converts to lowercase
text = "HELLO"
lowercase = text.lower()
print(f"'{text}'.lower(): '{lowercase}'")  # Output: 'hello'

# .capitalize() - capitalizes first letter
text = "hello world"
capitalized = text.capitalize()
print(f"'{text}'.capitalize(): '{capitalized}'")  # Output: 'Hello world'

# .title() - capitalizes first letter of each word
text = "hello world"
titled = text.title()
print(f"'{text}'.title(): '{titled}'")  # Output: 'Hello World'

# .strip() - removes leading/trailing whitespace
text = "  hello  "
stripped = text.strip()
print(f"'{text}'.strip(): '{stripped}'")  # Output: 'hello'

# .lstrip() - removes leading whitespace
text = "  hello  "
left_stripped = text.lstrip()
print(f"'{text}'.lstrip(): '{left_stripped}'")  # Output: 'hello  '

# .rstrip() - removes trailing whitespace
text = "  hello  "
right_stripped = text.rstrip()
print(f"'{text}'.rstrip(): '{right_stripped}'")  # Output: '  hello'

# .split() - splits string into list
text = "hello world"
words = text.split()
print(f"'{text}'.split(): {words}")  # Output: ['hello', 'world']

text = "apple,banana,cherry"
fruits = text.split(",")
print(f"'{text}'.split(','): {fruits}")  # Output: ['apple', 'banana', 'cherry']

# .join() - joins list elements into string
words = ["hello", "world"]
joined = " ".join(words)
print(f"' '.join({words}): '{joined}'")  # Output: 'hello world'

separated = "-".join(words)
print(f"'-'.join({words}): '{separated}'")  # Output: 'hello-world'

# .replace() - replaces substring
text = "hello world"
replaced = text.replace("world", "python")
print(f"'{text}'.replace('world', 'python'): '{replaced}'")  # Output: 'hello python'

# .find() - finds substring index (returns -1 if not found)
text = "hello"
index = text.find("e")
print(f"'{text}'.find('e'): {index}")  # Output: 1

index = text.find("x")
print(f"'{text}'.find('x'): {index}")  # Output: -1

# .index() - finds substring index (raises error if not found)
index = text.index("e")
print(f"'{text}'.index('e'): {index}")  # Output: 1

# .count() - counts substring occurrences
text = "hello"
count = text.count("l")
print(f"'{text}'.count('l'): {count}")  # Output: 2

# .startswith() - checks if string starts with substring
text = "hello"
starts = text.startswith("he")
print(f"'{text}'.startswith('he'): {starts}")  # Output: True

# .endswith() - checks if string ends with substring
text = "hello"
ends = text.endswith("lo")
print(f"'{text}'.endswith('lo'): {ends}")  # Output: True

# .isalpha() - checks if all characters are alphabetic
text = "hello"
is_alpha = text.isalpha()
print(f"'{text}'.isalpha(): {is_alpha}")  # Output: True

# .isdigit() - checks if all characters are digits
text = "123"
is_digit = text.isdigit()
print(f"'{text}'.isdigit(): {is_digit}")  # Output: True

# .isalnum() - checks if all characters are alphanumeric
text = "hello123"
is_alnum = text.isalnum()
print(f"'{text}'.isalnum(): {is_alnum}")  # Output: True

# .isspace() - checks if all characters are whitespace
text = "   "
is_space = text.isspace()
print(f"'{text}'.isspace(): {is_space}")  # Output: True


# ============================================================================
# 7. STRING FORMATTING
# ============================================================================

"""
Python provides multiple ways to format strings.
Modern approach uses f-strings (Python 3.6+).
"""

name = "John"
age = 30

# f-strings (recommended - Python 3.6+)
message = f"Hello, {name}! You are {age} years old."
print(f"f-string: {message}")

# Expressions in f-strings
result = f"2 + 3 = {2 + 3}"
print(f"Expression: {result}")

# Formatting numbers
pi = 3.14159
formatted = f"Pi: {pi:.2f}"
print(f"Formatted: {formatted}")  # Output: Pi: 3.14

# .format() method (older style)
message = "Hello, {}! You are {} years old.".formatter(name, age)
print(f".format(): {message}")

# Named placeholders
message = "Hello, {name}! You are {age} years old.".format(name=name, age=age)
print(f"Named: {message}")

# % formatting (oldest style)
message = "Hello, %s! You are %d years old." % (name, age)
print(f"% formatting: {message}")

# Multiple formatting examples
price = 19.99
quantity = 3
total = price * quantity

print(f"\nFormatting examples:")
print(f"Price: ${price:.2f}")
print(f"Quantity: {quantity}")
print(f"Total: ${total:.2f}")
print(f"Percentage: {0.75:.1%}")


# ============================================================================
# 8. PRACTICAL EXAMPLES
# ============================================================================

# Example 1: Text processing
text = "  Python Programming  "
processed = text.strip().title()
print(f"\nText processing:")
print(f"Original: '{text}'")
print(f"Processed: '{processed}'")

# Example 2: String reversal
text = "Python"
reversed_text = text[::-1]
print(f"\nString reversal:")
print(f"Original: {text}")
print(f"Reversed: {reversed_text}")

# Example 3: Checking if string contains substring
email = "user@example.com"
has_at = "@" in email
has_dot = "." in email
print(f"\nEmail check:")
print(f"'{email}' contains '@': {has_at}")
print(f"'{email}' contains '.': {has_dot}")
