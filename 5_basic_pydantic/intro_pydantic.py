"""
Pydantic Basics - Comprehensive Examples
========================================
This file demonstrates the fundamental concepts of Pydantic:
- Basic model definition
- Field types and validation
- Optional fields and default values
- Nested models
- List and dict fields
- Model serialization/deserialization
"""

from pydantic import BaseModel, Field, ValidationError
from typing import Optional, List, Dict, Any
from datetime import datetime


# ============================================================================
# Example 1: Basic Model Definition
# ============================================================================

class User(BaseModel):
    """A simple user model with basic fields."""
    name: str
    age: int
    email: str = "no email provided"
    is_active: bool = True  # Default value


# Create an instance
user1 = User(name="Alice", age=30, email="alice@example.com")
print("Example 1 - Basic Model:")
print(f"User: {user1}")
print(f"User name: {user1.name}")
print(f"User age: {user1.age}")
print(f"User dict: {user1.model_dump()}")
print()


# ============================================================================
# Example 2: Field Validation with Constraints
# ============================================================================

class Product(BaseModel):
    """Product model with field validation."""
    name: str = Field(..., min_length=1, max_length=100, regex=r"^[a-zA-Z0-9]+$")
    price: float = Field(..., gt=0, description="Price must be greater than 0")
    quantity: int = Field(..., ge=0, description="Quantity must be non-negative")
    category: str = Field(default="general", max_length=50)


# Valid product
product1 = Product(name="Laptop", price=999.99, quantity=10)
print("Example 2 - Field Validation:")
print(f"Product: {product1}")
print()

# This would raise a ValidationError:
# product2 = Product(name="", price=-10, quantity=-5)  # Invalid!


# ============================================================================
# Example 3: Optional Fields
# ============================================================================

class Profile(BaseModel):
    """User profile with optional fields."""
    username: str
    full_name: Optional[str] = None
    bio: Optional[str] = None
    website: Optional[str] = None
    followers: int = 0  # Default value


profile1 = Profile(username="johndoe")
profile2 = Profile(
    username="janedoe",
    full_name="Jane Doe",
    bio="Software Engineer",
    website="https://jane.doe",
    followers=1500
)

print("Example 3 - Optional Fields:")
print(f"Profile 1 (minimal): {profile1}")
print(f"Profile 2 (complete): {profile2}")
print()


# ============================================================================
# Example 4: Nested Models
# ============================================================================

class Address(BaseModel):
    """Address model for nesting."""
    street: str
    city: str
    state: str
    zip_code: str
    country: str = "USA"


class Person(BaseModel):
    """Person model with nested address."""
    name: str
    age: int
    address: Address


person1 = Person(
    name="Bob Smith",
    age=35,
    address=Address(
        street="123 Main St",
        city="New York",
        state="NY",
        zip_code="10001"
    )
)

print("Example 4 - Nested Models:")
print(f"Person: {person1}")
print(f"Person's city: {person1.address.city}")
print()


# ============================================================================
# Example 5: List Fields
# ============================================================================

class Course(BaseModel):
    """Course model with list of students."""
    name: str
    instructor: str
    students: List[str] = []  # List of student names
    grades: List[float] = Field(default_factory=list)


course1 = Course(
    name="Python 101",
    instructor="Dr. Smith",
    students=["Alice", "Bob", "Charlie"],
    grades=[95.5, 87.0, 92.5]
)

print("Example 5 - List Fields:")
print(f"Course: {course1}")
print(f"Number of students: {len(course1.students)}")
print(f"Average grade: {sum(course1.grades) / len(course1.grades):.2f}")
print()


# ============================================================================
# Example 6: Dictionary Fields
# ============================================================================

class Settings(BaseModel):
    """Settings model with dictionary field."""
    theme: str = "light"
    preferences: Dict[str, str] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)


settings1 = Settings(
    theme="dark",
    preferences={
        "language": "en",
        "timezone": "UTC",
        "notifications": "enabled"
    },
    metadata={
        "version": "1.0",
        "created_at": "2024-01-01"
    }
)

print("Example 6 - Dictionary Fields:")
print(f"Settings: {settings1}")
print(f"Language preference: {settings1.preferences.get('language')}")
print()


# ============================================================================
# Example 7: Complex Nested Model
# ============================================================================

class Author(BaseModel):
    """Author model."""
    name: str
    email: str


class Book(BaseModel):
    """Book model with nested author and list of tags."""
    title: str
    author: Author
    isbn: str
    pages: int = Field(..., gt=0)
    tags: List[str] = []
    published_year: Optional[int] = None


book1 = Book(
    title="Python for Beginners",
    author=Author(name="John Doe", email="john@example.com"),
    isbn="978-1234567890",
    pages=300,
    tags=["programming", "python", "beginner"],
    published_year=2023
)

print("Example 7 - Complex Nested Model:")
print(f"Book: {book1}")
print(f"Author email: {book1.author.email}")
print(f"Tags: {', '.join(book1.tags)}")
print()


# ============================================================================
# Example 8: Model Methods
# ============================================================================

class Rectangle(BaseModel):
    """Rectangle model with custom methods."""
    width: float = Field(..., gt=0)
    height: float = Field(..., gt=0)

    def area(self) -> float:
        """Calculate the area of the rectangle."""
        return self.width * self.height

    def perimeter(self) -> float:
        """Calculate the perimeter of the rectangle."""
        return 2 * (self.width + self.height)

    def is_square(self) -> bool:
        """Check if the rectangle is a square."""
        return self.width == self.height


rect1 = Rectangle(width=5.0, height=5.0)
rect2 = Rectangle(width=4.0, height=6.0)

print("Example 8 - Model Methods:")
print(f"Rectangle 1: {rect1}")
print(f"Area: {rect1.area()}")
print(f"Perimeter: {rect1.perimeter()}")
print(f"Is square: {rect1.is_square()}")
print(f"Rectangle 2 is square: {rect2.is_square()}")
print()


# ============================================================================
# Example 9: Serialization (Model to Dict/JSON)
# ============================================================================

class Employee(BaseModel):
    """Employee model for serialization examples."""
    id: int
    name: str
    department: str
    salary: float


employee1 = Employee(id=1, name="Alice", department="Engineering", salary=95000.0)

# Convert to dictionary
employee_dict = employee1.model_dump()
print("Example 9 - Serialization:")
print(f"Model: {employee1}")
print(f"Dictionary: {employee_dict}")
print(f"JSON string: {employee1.model_dump_json()}")
print(f"JSON (indented): {employee1.model_dump_json(indent=2)}")
print()


# ============================================================================
# Example 10: Deserialization (Dict/JSON to Model)
# ============================================================================

# Create from dictionary
employee_data = {
    "id": 2,
    "name": "Bob",
    "department": "Marketing",
    "salary": 75000.0
}

employee2 = Employee(**employee_data)
print("Example 10 - Deserialization:")
print(f"Created from dict: {employee2}")

# Create from JSON string
json_data = '{"id": 3, "name": "Charlie", "department": "Sales", "salary": 65000.0}'
employee3 = Employee.model_validate_json(json_data)
print(f"Created from JSON: {employee3}")
print()


# ============================================================================
# Example 11: Error Handling
# ============================================================================

print("Example 11 - Error Handling:")

try:
    invalid_user = User(
        name="",  # Empty name might be invalid
        age=-5,   # Negative age is invalid
        email="not-an-email"  # Invalid email format
    )
except ValidationError as e:
    print("Validation errors occurred:")
    for error in e.errors():
        print(f"  - Field: {error['loc']}, Error: {error['msg']}")

try:
    invalid_product = Product(
        name="A" * 200,  # Too long
        price=-10,        # Negative price
        quantity=-5       # Negative quantity
    )
except ValidationError as e:
    print("\nProduct validation errors:")
    for error in e.errors():
        print(f"  - Field: {error['loc']}, Error: {error['msg']}")
print()


# ============================================================================
# Example 12: Field Aliases
# ============================================================================

class ConfigModel(BaseModel):
    """Model with field aliases for different naming conventions."""
    first_name: str = Field(..., alias="firstName")
    last_name: str = Field(..., alias="lastName")
    user_id: int = Field(..., alias="userId")

    class Config:
        populate_by_name = True  # Allows both alias and field name


# Create using alias
config1 = ConfigModel(firstName="John", lastName="Doe", userId=123)
print("Example 12 - Field Aliases:")
print(f"Using alias: {config1}")
print(f"Access by field name: {config1.first_name}")
print(f"Dict with alias: {config1.model_dump(by_alias=True)}")
print()


# ============================================================================
# Example 13: Model with DateTime
# ============================================================================

class Event(BaseModel):
    """Event model with datetime field."""
    title: str
    description: str
    start_time: datetime
    end_time: Optional[datetime] = None
    attendees: List[str] = []


from datetime import datetime, timedelta

event1 = Event(
    title="Python Workshop",
    description="Learn Python basics",
    start_time=datetime(2024, 3, 15, 10, 0, 0),
    end_time=datetime(2024, 3, 15, 12, 0, 0),
    attendees=["Alice", "Bob", "Charlie"]
)

print("Example 13 - DateTime Fields:")
print(f"Event: {event1}")
print(f"Start time: {event1.start_time}")
print(f"Duration: {event1.end_time - event1.start_time}")
print()


# ============================================================================
# Example 14: Model Inheritance
# ============================================================================

class Animal(BaseModel):
    """Base animal model."""
    name: str
    species: str
    age: int


class Dog(Animal):
    """Dog model inheriting from Animal."""
    breed: str
    is_trained: bool = False


class Cat(Animal):
    """Cat model inheriting from Animal."""
    color: str
    is_indoor: bool = True


dog1 = Dog(name="Buddy", species="Canine", age=3, breed="Golden Retriever", is_trained=True)
cat1 = Cat(name="Whiskers", species="Feline", age=2, color="Orange", is_indoor=True)

print("Example 14 - Model Inheritance:")
print(f"Dog: {dog1}")
print(f"Cat: {cat1}")
print(f"Both are animals: {isinstance(dog1, Animal)} and {isinstance(cat1, Animal)}")
print()


# ============================================================================
# Example 15: Model with Computed Fields
# ============================================================================

from pydantic import computed_field

class Order(BaseModel):
    """Order model with computed fields."""
    items: List[Dict[str, any]]
    tax_rate: float = 0.1

    @computed_field
    @property
    def subtotal(self) -> float:
        """Calculate subtotal from items."""
        return sum(item.get("price", 0) * item.get("quantity", 0) for item in self.items)

    @computed_field
    @property
    def tax(self) -> float:
        """Calculate tax."""
        return self.subtotal * self.tax_rate

    @computed_field
    @property
    def total(self) -> float:
        """Calculate total."""
        return self.subtotal + self.tax


order1 = Order(
    items=[
        {"name": "Item 1", "price": 10.0, "quantity": 2},
        {"name": "Item 2", "price": 15.0, "quantity": 1},
        {"name": "Item 3", "price": 5.0, "quantity": 3}
    ],
    tax_rate=0.08
)

print("Example 15 - Computed Fields:")
print(f"Order items: {order1.items}")
print(f"Subtotal: ${order1.subtotal:.2f}")
print(f"Tax: ${order1.tax:.2f}")
print(f"Total: ${order1.total:.2f}")
print()


print("=" * 60)
print("All Pydantic basics examples completed successfully!")
print("=" * 60)
