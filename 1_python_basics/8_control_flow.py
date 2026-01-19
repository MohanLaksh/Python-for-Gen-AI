# ============================================================================
# CONTROL FLOW IN PYTHON
# ============================================================================

"""
Control flow statements determine the order in which code executes.
Python provides if, elif, else, and match-case statements for decision making.
"""

# ============================================================================
# 1. IF STATEMENT
# ============================================================================

"""
The if statement executes code only if a condition is True.
"""

# Basic if statement
condition = True
if condition:
    # code block
    print("Condition is True")

# Example with variable
age = 18
if age >= 18:
    print("You are an adult")

# Example with comparison
temperature = 25
if temperature > 20:
    print("It's warm outside")


# ============================================================================
# 2. IF-ELSE STATEMENT
# ============================================================================

"""
The if-else statement executes one block if condition is True,
another block if condition is False.
"""

# Basic if-else
age = 15
if age >= 18:
    # code block
    print("You are an adult")
else:
    # code block
    print("You are a minor")

# Example: Even or odd
number = 7
if number % 2 == 0:
    print(f"{number} is even")
else:
    print(f"{number} is odd")

# Example: Positive or negative
value = -5
if value > 0:
    print(f"{value} is positive")
else:
    print(f"{value} is negative or zero")


# ============================================================================
# 3. IF-ELIF-ELSE STATEMENT
# ============================================================================

"""
The if-elif-else statement allows multiple conditions to be checked.
Only the first True condition's block executes.
"""

# Basic if-elif-else
score = 85
if score >= 90:
    # code block
    print("Grade: A")
elif score >= 80:
    # code block
    print("Grade: B")
elif score >= 70:
    # code block
    print("Grade: C")
else:
    # code block
    print("Grade: F")

# Example: Temperature ranges
temperature = 15
if temperature > 30:
    print("It's hot")
elif temperature > 20:
    print("It's warm")
elif temperature > 10:
    print("It's cool")
else:
    print("It's cold")

# Example: Age groups
age = 25
if age < 13:
    print("Child")
elif age < 20:
    print("Teenager")
elif age < 65:
    print("Adult")
else:
    print("Senior")


# ============================================================================
# 4. NESTED IF STATEMENTS
# ============================================================================

"""
If statements can be nested inside other if statements.
Useful for complex conditional logic.
"""

# Basic nested if
age = 25
has_license = True

if age >= 18:
    if has_license:
        # code block
        print("You can drive")
    else:
        print("You need a license")
else:
    print("You are too young to drive")

# Example: Login system
username = "admin"
password = "secret123"
is_active = True

if username == "admin":
    if password == "secret123":
        if is_active:
            print("Login successful")
        else:
            print("Account is inactive")
    else:
        print("Incorrect password")
else:
    print("User not found")

# Example: Grade with attendance
score = 85
attendance = 0.75

if score >= 70:
    if attendance >= 0.80:
        print("Passed")
    else:
        print("Failed due to low attendance")
else:
    print("Failed due to low score")


# ============================================================================
# 5. TERNARY OPERATOR (CONDITIONAL EXPRESSION)
# ============================================================================

"""
The ternary operator provides a concise way to write if-else statements.
Syntax: value_if_true if condition else value_if_false
"""

# Basic ternary operator
result = "Even" if 4 % 2 == 0 else "Odd"
print(f"Result: {result}")  # Output: Even

# Example: Maximum value
a = 10
b = 20
max_value = a if a > b else b
print(f"Maximum: {max_value}")  # Output: 20

# Example: Age check
age = 20
status = "Adult" if age >= 18 else "Minor"
print(f"Status: {status}")  # Output: Adult

# Example: Sign of number
number = -5
sign = "Positive" if number > 0 else "Negative" if number < 0 else "Zero"
print(f"Sign: {sign}")  # Output: Negative

# Nested ternary (use sparingly - can be hard to read)
score = 85
grade = "A" if score >= 90 else "B" if score >= 80 else "C" if score >= 70 else "F"
print(f"Grade: {grade}")  # Output: B


# ============================================================================
# 6. MATCH-CASE STATEMENT (Python 3.10+)
# ============================================================================

"""
The match-case statement provides pattern matching (similar to switch-case).
More powerful than if-elif chains for certain use cases.
"""

# Basic match-case
value = 2
match value:
    case 1:
        # code block
        print("One")
    case 2:
        # code block
        print("Two")
    case 3:
        # code block
        print("Three")
    case _:
        # default case
        print("Other")

# Example: Day of week
day = "Monday"
match day:
    case "Monday" | "Tuesday" | "Wednesday" | "Thursday" | "Friday":
        print("Weekday")
    case "Saturday" | "Sunday":
        print("Weekend")
    case _:
        print("Invalid day")

# Example: HTTP status codes
status_code = 404
match status_code:
    case 200:
        print("OK")
    case 301 | 302:
        print("Redirect")
    case 404:
        print("Not Found")
    case 500:
        print("Server Error")
    case _:
        print("Unknown status")

# Example: Pattern matching with conditions
score = 85
match score:
    case s if s >= 90:
        print("Excellent")
    case s if s >= 80:
        print("Good")
    case s if s >= 70:
        print("Average")
    case _:
        print("Needs improvement")


# ============================================================================
# 7. LOGICAL OPERATORS IN CONDITIONS
# ============================================================================

"""
Combine multiple conditions using and, or, not operators.
"""

# Using and
age = 25
has_license = True
if age >= 18 and has_license:
    print("Can drive")

# Using or
is_weekend = False
is_holiday = True
if is_weekend or is_holiday:
    print("Can sleep in")

# Using not
is_raining = False
if not is_raining:
    print("Can go outside")

# Complex conditions
score = 85
attendance = 0.90
if score >= 70 and attendance >= 0.80:
    print("Passed")
else:
    print("Failed")

# Combining operators
temperature = 25
is_sunny = True
if (temperature > 20 and temperature < 30) or is_sunny:
    print("Good weather for outdoor activities")


# ============================================================================
# 8. PRACTICAL EXAMPLES
# ============================================================================

# Example 1: Grade calculator
score = 85
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
elif score >= 60:
    grade = "D"
else:
    grade = "F"

print(f"\nGrade calculator:")
print(f"  Score {score}: Grade {grade}")

# Example 2: Login validation
username = "admin"
password = "secret123"
valid_username = "admin"
valid_password = "secret123"

if username == valid_username:
    if password == valid_password:
        result = "Login successful"
    else:
        result = "Incorrect password"
else:
    result = "User not found"

print(f"\nLogin validation:")
print(f"  {result}")

# Example 3: Discount calculator
price = 100
is_member = True
is_weekend = True

if is_member and is_weekend:
    discount = 0.20  # 20% discount
elif is_member:
    discount = 0.10  # 10% discount
elif is_weekend:
    discount = 0.05  # 5% discount
else:
    discount = 0

final_price = price * (1 - discount)
print(f"\nDiscount calculator:")
print(f"  Regular price ${price}, member, weekend: ${final_price:.2f}")

# Example 4: Number classifier
number = 5
if number == 0:
    classification = "Zero"
elif number > 0:
    if number % 2 == 0:
        classification = "Positive even"
    else:
        classification = "Positive odd"
else:
    if number % 2 == 0:
        classification = "Negative even"
    else:
        classification = "Negative odd"

print(f"\nNumber classifier:")
print(f"  {number}: {classification}")

# Example 5: BMI calculator
weight = 70  # kg
height = 1.75  # meters
bmi = weight / (height ** 2)

if bmi < 18.5:
    category = "Underweight"
elif bmi < 25:
    category = "Normal"
elif bmi < 30:
    category = "Overweight"
else:
    category = "Obese"

print(f"\nBMI calculator:")
print(f"  Weight: {weight}kg, Height: {height}m")
print(f"  BMI: {bmi:.2f}, Category: {category}")
