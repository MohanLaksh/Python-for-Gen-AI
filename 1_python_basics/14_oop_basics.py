# ============================================================================
# OOP BASICS - Object-Oriented Programming in Python
# ============================================================================

"""
Object-Oriented Programming (OOP) is a programming paradigm that organizes
code into objects that contain both data (attributes) and behavior (methods).
Python supports OOP with classes and objects.
"""

# ============================================================================
# 1. CLASS DEFINITION
# ============================================================================

"""
A class is a blueprint for creating objects. It defines the structure and
behavior that objects of that class will have.

Syntax:
    class ClassName:
        # class body
        pass
"""

# Example: Basic class definition
class ClassName:
    # class body
    pass

# Example: Creating a simple class
class Dog:
    pass

# Creating an object (instance) from a class
my_dog = Dog()
print(f"Created object: {my_dog}")  # Shows memory location
print(f"Type: {type(my_dog)}")  # <class '__main__.Dog'>


# ============================================================================
# 2. __init__ METHOD (CONSTRUCTOR)
# ============================================================================

"""
The __init__ method is a special method called when an object is created.
It's used to initialize the object's attributes (instance variables).
'self' refers to the instance of the class.
"""

# Example: Class with __init__ method
class Person:
    def __init__(self, name, age):
        self.name = name  # instance variable
        self.age = age    # instance variable

# Creating objects with initial values
person1 = Person("Alice", 25)
person2 = Person("Bob", 30)

print(f"\nPerson 1: {person1.name}, Age: {person1.age}")
print(f"Person 2: {person2.name}, Age: {person2.age}")


# ============================================================================
# 3. INSTANCE METHODS
# ============================================================================

"""
Instance methods are functions defined inside a class that operate on
instances of the class. They always take 'self' as the first parameter.
"""

# Example: Class with instance methods
class Person:
    def __init__(self, name):
        self.name = name
    
    def greet(self):
        """Instance method that uses instance data"""
        return f"Hello, I'm {self.name}"
    
    def introduce(self, other_person):
        """Instance method with additional parameters"""
        return f"Hi {other_person.name}, I'm {self.name}"

# Using instance methods
alice = Person("Alice")
bob = Person("Bob")

print(f"\n{alice.greet()}")
print(f"{bob.greet()}")
print(f"{alice.introduce(bob)}")


# ============================================================================
# 4. CLASS VARIABLES vs INSTANCE VARIABLES
# ============================================================================

"""
Class variables are shared by all instances of a class.
Instance variables are unique to each instance.
"""

# Example: Class variables and instance variables
class Person:
    # Class variable (shared by all instances)
    species = "Homo sapiens"
    population = 0  # Can track all instances
    
    def __init__(self, name, age):
        # Instance variables (unique to each instance)
        self.name = name
        self.age = age
        Person.population += 1  # Increment class variable
    
    def get_info(self):
        return f"{self.name} is {self.age} years old, species: {self.species}"

# Creating instances
person1 = Person("Alice", 25)
person2 = Person("Bob", 30)

print(f"\n{person1.get_info()}")
print(f"{person2.get_info()}")
print(f"Total population: {Person.population}")

# Accessing class variable directly
print(f"Species: {Person.species}")

# Modifying class variable affects all instances
Person.species = "Homo sapiens sapiens"
print(f"After change: {person1.species}")


# ============================================================================
# 5. INHERITANCE
# ============================================================================

"""
Inheritance allows a class (child) to inherit attributes and methods
from another class (parent). This promotes code reuse.
"""

# Example: Basic inheritance
class Animal:
    def __init__(self, name):
        self.name = name
    
    def speak(self):
        return f"{self.name} makes a sound"

class Dog(Animal):  # Dog inherits from Animal
    def speak(self):
        return f"{self.name} barks"

class Cat(Animal):  # Cat inherits from Animal
    def speak(self):
        return f"{self.name} meows"

# Using inheritance
dog = Dog("Buddy")
cat = Cat("Whiskers")

print(f"\n{dog.speak()}")
print(f"{cat.speak()}")


# ============================================================================
# 6. METHOD OVERRIDING
# ============================================================================

"""
Method overriding occurs when a child class provides its own implementation
of a method that exists in the parent class.
"""

# Example: Method overriding
class Parent:
    def method(self):
        return "Parent method"
    
    def common_method(self):
        return "This is from Parent"

class Child(Parent):
    # Override the parent's method
    def method(self):
        return "Child method"
    
    # Child can also have its own methods
    def child_only_method(self):
        return "This is only in Child"

parent = Parent()
child = Child()

print(f"\nParent.method(): {parent.method()}")
print(f"Child.method(): {child.method()}")  # Overridden
print(f"Child.common_method(): {child.common_method()}")  # Inherited


# ============================================================================
# 7. super() FUNCTION
# ============================================================================

"""
super() is used to call methods from the parent class. It's especially
useful when you want to extend parent functionality rather than replace it.
"""

# Example: Using super()
class Animal:
    def __init__(self, name, species):
        self.name = name
        self.species = species
    
    def info(self):
        return f"{self.name} is a {self.species}"

class Dog(Animal):
    def __init__(self, name, breed):
        # Call parent's __init__ using super()
        super().__init__(name, "Canine")
        self.breed = breed
    
    def info(self):
        # Extend parent's method
        parent_info = super().info()
        return f"{parent_info} of breed {self.breed}"

dog = Dog("Buddy", "Golden Retriever")
print(f"\n{dog.info()}")


# ============================================================================
# 8. ENCAPSULATION (PRIVATE AND PROTECTED ATTRIBUTES)
# ============================================================================

"""
Encapsulation is the practice of restricting access to certain attributes.
Python uses naming conventions:
- Single underscore (_): Protected (convention, not enforced)
- Double underscore (__): Private (name mangling occurs)
"""

# Example: Encapsulation
class Person:
    def __init__(self, name, age):
        self._name = name      # Protected attribute (convention)
        self.__age = age       # Private attribute (name mangling)
        self.public = "This is public"  # Public attribute
    
    def get_age(self):
        """Getter method for private attribute"""
        return self.__age
    
    def set_age(self, age):
        """Setter method for private attribute"""
        if age > 0:
            self.__age = age
        else:
            print("Age must be positive")
    
    def display_info(self):
        return f"Name: {self._name}, Age: {self.__age}"

person = Person("Alice", 25)

# Public attribute - accessible directly
print(f"\nPublic: {person.public}")

# Protected attribute - accessible but convention says don't
print(f"Protected: {person._name}")

# Private attribute - should use getter/setter
print(f"Age via getter: {person.get_age()}")
person.set_age(26)
print(f"After setter: {person.display_info()}")

# Note: Private attributes can still be accessed (Python doesn't enforce privacy)
# But it's bad practice: person._Person__age


# ============================================================================
# 9. POLYMORPHISM
# ============================================================================

"""
Polymorphism allows objects of different classes to be treated as objects
of a common parent class. Different classes can have methods with the same
name that behave differently.
"""

# Example: Polymorphism
class Shape:
    def area(self):
        raise NotImplementedError("Subclass must implement area()")

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    
    def area(self):
        return 3.14159 * self.radius ** 2

# Polymorphism in action - same method name, different behavior
shapes = [Rectangle(5, 3), Circle(4), Rectangle(2, 2)]

print("\nPolymorphism example:")
for shape in shapes:
    print(f"Area: {shape.area()}")


# ============================================================================
# 10. SPECIAL METHODS (DUNDER METHODS)
# ============================================================================

"""
Special methods (dunder methods) allow you to define how objects behave
with built-in Python operations. They start and end with double underscores.
"""

# Example: Special methods
class Book:
    def __init__(self, title, author, pages):
        self.title = title
        self.author = author
        self.pages = pages
    
    # __str__: Called by str() and print() - user-friendly representation
    def __str__(self):
        return f"'{self.title}' by {self.author}"
    
    # __repr__: Called by repr() - official representation (for developers)
    def __repr__(self):
        return f"Book('{self.title}', '{self.author}', {self.pages})"
    
    # __len__: Called by len()
    def __len__(self):
        return self.pages
    
    # __add__: Called by + operator
    def __add__(self, other):
        if isinstance(other, Book):
            return Book(
                f"{self.title} & {other.title}",
                f"{self.author} & {other.author}",
                self.pages + other.pages
            )
        return NotImplemented
    
    # __eq__: Called by == operator
    def __eq__(self, other):
        if isinstance(other, Book):
            return (self.title == other.title and 
                   self.author == other.author and 
                   self.pages == other.pages)
        return False

    def __float__(self):
        return float(self.pages)

    def __getitem__(self, index):
        return self.pages[index]
    
    # __lt__: Called by < operator
    def __lt__(self, other):
        if isinstance(other, Book):
            return self.pages < other.pages
        return NotImplemented

# Using special methods
book1 = Book("Python Guide", "John Doe", 300)
book2 = Book("Python Guide", "John Doe", 300)
book3 = Book("Java Basics", "Jane Smith", 250)

print("\nSpecial methods examples:")
print(f"str(): {str(book1)}")
print(f"repr(): {repr(book1)}")
print(f"len(): {len(book1)} pages")
print(f"Equality: {book1 == book2}")
print(f"Comparison: {book3 < book1}")
print(f"Addition: {book1 + book3}")
print(f"Float: {float(book1)}")


# ============================================================================
# 11. PROPERTY DECORATOR
# ============================================================================

"""
The @property decorator allows you to define methods that can be accessed
like attributes. It's useful for computed properties and validation.
"""

# Example: Property decorator
class Person:
    def __init__(self, name, birth_year):
        self._name = name
        self._birth_year = birth_year
    
    # Getter property
    @property
    def name(self):
        """Get the person's name"""
        return self._name
    
    # Setter property
    @name.setter
    def name(self, value):
        """Set the person's name with validation"""
        if isinstance(value, str) and len(value) > 0:
            self._name = value
        else:
            raise ValueError("Name must be a non-empty string")
    
    # Read-only property (no setter)
    @property
    def age(self):
        """Calculate age from birth year"""
        from datetime import datetime
        return datetime.now().year - self._birth_year
    
    # Computed property
    @property
    def info(self):
        """Return formatted info string"""
        return f"{self._name} is {self.age} years old"

# Using properties
person = Person("Alice", 1998)

print("\nProperty decorator examples:")
print(f"Name: {person.name}")  # Access like attribute
print(f"Age: {person.age}")    # Computed property
print(f"Info: {person.info}")

# Using setter
person.name = "Alice Smith"
print(f"After setter: {person.name}")

# Trying to set read-only property will raise AttributeError
# person.age = 25  # This would raise an error


# ============================================================================
# COMPREHENSIVE EXAMPLE: Complete OOP Application
# ============================================================================

class BankAccount:
    """A bank account class demonstrating OOP concepts"""
    
    # Class variable
    account_count = 0
    interest_rate = 0.05  # 5% interest
    
    def __init__(self, owner, initial_balance=0):
        self.owner = owner
        self.__balance = initial_balance  # Private attribute
        BankAccount.account_count += 1
        self.account_number = BankAccount.account_count
    
    def deposit(self, amount):
        """Deposit money into account"""
        if amount > 0:
            self.__balance += amount
            return f"Deposited ${amount}. New balance: ${self.__balance}"
        return "Deposit amount must be positive"
    
    def withdraw(self, amount):
        """Withdraw money from account"""
        if amount > 0 and amount <= self.__balance:
            self.__balance -= amount
            return f"Withdrew ${amount}. New balance: ${self.__balance}"
        return "Insufficient funds or invalid amount"
    
    @property
    def balance(self):
        """Get account balance"""
        return self.__balance
    
    def __str__(self):
        return f"Account #{self.account_number} - Owner: {self.owner}, Balance: ${self.__balance}"
    
    def __repr__(self):
        return f"BankAccount('{self.owner}', {self.__balance})"

# Using the comprehensive example
print("\n" + "="*60)
print("COMPREHENSIVE EXAMPLE: Bank Account")
print("="*60)

account1 = BankAccount("Alice", 1000)
account2 = BankAccount("Bob", 500)

print(f"\n{account1}")
print(f"{account2}")

print(f"\n{account1.deposit(200)}")
print(f"{account1.withdraw(100)}")
print(f"Balance: ${account1.balance}")

print(f"\nTotal accounts created: {BankAccount.account_count}")
