from ast import pattern
from enum import Enum
from pydantic import BaseModel, Field, validate_call, ValidationError

class User(BaseModel):
    """A simple user model with basic fields."""
    name: str
    age: int
    email: str = Field(..., pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", message="Invalid email address")
    is_active: bool = True  # Default value


print("Example 11 - Error Handling:")

try:
    invalid_user = User(
        name="",  # Empty name might be invalid
        email="not-an-email",
        age=6.7,   # Negative age is invalid
    )
except ValidationError as e:
    print("Validation errors occurred:")
    for error in e.errors():
        print(f"  - Field: {error['loc']}, Error: {error['msg']}")
print()

# Pydantic GEN AI use case
# Collections use cases for Gen AI
# HTTPX library for Gen AI

