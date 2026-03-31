# Pydantic — Interview Questions & Ideal Answers

---

## 1. Core Value Proposition

**Q: Why is Pydantic widely used in Python AI applications? What problems does it solve?**

**A:**
Pydantic solves three interconnected problems in AI pipelines:

1. **Validation at system boundaries** — LLM outputs and API responses can be malformed. Pydantic enforces a schema and raises descriptive errors.
2. **Parsing** — converts raw dicts/JSON strings into typed Python objects automatically.
3. **Serialisation** — converts models back to JSON for logging, caching, or passing to downstream services.

In LangChain and the OpenAI Python SDK, Pydantic models represent structured LLM outputs (function call arguments, tool inputs/outputs). FastAPI uses Pydantic for every request and response body.

---

## 2. Basic Model Definition

**Q: Define a Pydantic model for an LLM API request and demonstrate validation error handling.**

**A:**
```python
from pydantic import BaseModel, Field, field_validator
from typing import Literal

class ChatRequest(BaseModel):
    model: Literal["gpt-4o", "gpt-4o-mini", "claude-3-5-sonnet"] = "gpt-4o-mini"
    prompt: str = Field(min_length=1, max_length=4096)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=512, ge=1, le=4096)

    @field_validator("prompt")
    @classmethod
    def no_injection(cls, v: str) -> str:
        forbidden = ["ignore all previous", "disregard instructions"]
        if any(phrase in v.lower() for phrase in forbidden):
            raise ValueError("Prompt contains forbidden content")
        return v.strip()

# Valid
req = ChatRequest(prompt="What is RAG?", temperature=1.2)
print(req.model)  # gpt-4o-mini

# Invalid — raises ValidationError
from pydantic import ValidationError
try:
    ChatRequest(prompt="", temperature=3.0)
except ValidationError as e:
    print(e)
# 2 validation errors:
#   prompt: String should have at least 1 character
#   temperature: Input should be less than or equal to 2.0
```

---

## 3. Nested Models & Complex Types

**Q: How do you model nested JSON structures like an LLM chat conversation history?**

**A:**
```python
from pydantic import BaseModel
from typing import Literal
from datetime import datetime

class Message(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class Conversation(BaseModel):
    id: str
    messages: list[Message] = []
    model: str = "gpt-4o"
    total_tokens: int = 0

    def add_message(self, role: str, content: str) -> None:
        self.messages.append(Message(role=role, content=content))

# Usage
convo = Conversation(id="conv-123")
convo.add_message("user", "What is a vector database?")
convo.add_message("assistant", "A vector database stores embeddings...")

# Serialise to JSON for storage
print(convo.model_dump_json(indent=2))
```

---

## 4. Field Aliases & Serialisation

**Q: An external API returns `snake_case` but your internal code uses `camelCase`. How does Pydantic handle this?**

**A:**
Use `Field(alias=...)` or model-level `model_config` with `populate_by_name=True`.

```python
from pydantic import BaseModel, Field
from pydantic import ConfigDict

class EmbeddingResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    object_type: str = Field(alias="object")
    embedding_data: list[dict] = Field(alias="data")
    model_name: str = Field(alias="model")
    usage_tokens: int = Field(alias="usage")

# Parse from API response (uses aliases)
raw = {"object": "list", "data": [...], "model": "text-embedding-3-small", "usage": 12}
resp = EmbeddingResponse.model_validate(raw)

# Access via Python name
print(resp.model_name)   # text-embedding-3-small

# Serialise back with aliases for the API
print(resp.model_dump(by_alias=True))
```

---

## 5. Validators

**Q: What is the difference between `@field_validator` and `@model_validator`? When do you need each?**

**A:**
- `@field_validator` runs on a **single field** after it is parsed. Use for field-level constraints (format checks, normalisation).
- `@model_validator` runs on the **whole model** (before or after field parsing). Use for cross-field validation.

```python
from pydantic import BaseModel, field_validator, model_validator
from typing import Optional

class DateRange(BaseModel):
    start_date: str   # "YYYY-MM-DD"
    end_date: str
    max_days: Optional[int] = None

    @field_validator("start_date", "end_date")
    @classmethod
    def valid_date_format(cls, v: str) -> str:
        from datetime import datetime
        datetime.strptime(v, "%Y-%m-%d")  # raises ValueError if bad format
        return v

    @model_validator(mode="after")
    def end_after_start(self) -> "DateRange":
        from datetime import datetime
        start = datetime.strptime(self.start_date, "%Y-%m-%d")
        end = datetime.strptime(self.end_date, "%Y-%m-%d")
        if end <= start:
            raise ValueError("end_date must be after start_date")
        if self.max_days and (end - start).days > self.max_days:
            raise ValueError(f"Range exceeds {self.max_days} days")
        return self
```

---

## 6. Structured LLM Output

**Q: How do you use Pydantic to extract structured data from an LLM response reliably?**

**A:**
Pass the Pydantic schema to the model as a JSON schema and validate the output:

```python
from pydantic import BaseModel
from openai import OpenAI

class ProductInfo(BaseModel):
    name: str
    price_usd: float
    in_stock: bool
    categories: list[str]

client = OpenAI()

def extract_product(text: str) -> ProductInfo:
    response = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Extract product information from the text."},
            {"role": "user", "content": text},
        ],
        response_format=ProductInfo,   # Pydantic model passed directly
    )
    return response.choices[0].message.parsed  # already a ProductInfo instance

product = extract_product("The Sony WH-1000XM5 headphones cost $279.99 and are available now in Electronics and Audio.")
print(product.price_usd)     # 279.99
print(product.in_stock)      # True
```

---

## 7. Pydantic v1 vs v2

**Q: What are the main breaking changes between Pydantic v1 and v2? How would you migrate?**

**A:**
Key v2 changes:
| v1 | v2 |
|---|---|
| `dict()` | `model_dump()` |
| `json()` | `model_dump_json()` |
| `parse_obj(data)` | `model_validate(data)` |
| `parse_raw(json_str)` | `model_validate_json(json_str)` |
| `@validator` | `@field_validator` |
| `class Config:` | `model_config = ConfigDict(...)` |
| `schema()` | `model_json_schema()` |

Migration strategy:
1. Run `pydantic.v1` compatibility shim for gradual migration.
2. Use the `bump-pydantic` codemod: `pip install bump-pydantic && bump_pydantic .`
3. Update imports and method names project-wide.
4. v2 is 5–50x faster than v1 due to the Rust core (pydantic-core).
