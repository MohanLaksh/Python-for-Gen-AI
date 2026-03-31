# FastAPI — Interview Questions & Ideal Answers

---

## 1. Core Concepts

**Q: What makes FastAPI different from Flask or Django REST Framework?**

**A:**
| Feature | Flask | Django REST | FastAPI |
|---|---|---|---|
| Type hints | Optional | Optional | Native / required |
| Validation | Manual / marshmallow | Serializers | Pydantic (built-in) |
| Async support | Limited | Limited | First-class |
| Auto docs | No | No | Swagger + ReDoc auto-generated |
| Performance | Moderate | Moderate | High (Starlette + uvicorn) |

FastAPI generates OpenAPI 3.x docs automatically from type annotations and Pydantic models, eliminating an entire category of documentation drift. It's also one of the fastest Python frameworks in benchmarks because it runs on Starlette + uvicorn (ASGI).

---

## 2. Path & Query Parameters

**Q: What is the difference between a path parameter and a query parameter in FastAPI? Write an endpoint that uses both.**

**A:**
- **Path parameter**: part of the URL path (`/items/{item_id}`), always required.
- **Query parameter**: appended after `?` (`/items?skip=0&limit=10`), optional by default if a default is provided.

```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

fake_db = {1: "Laptop", 2: "Mouse", 3: "Keyboard"}

@app.get("/items/{item_id}")
def get_item(item_id: int, include_metadata: bool = False):
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="Item not found")
    result = {"id": item_id, "name": fake_db[item_id]}
    if include_metadata:
        result["total_items"] = len(fake_db)
    return result
```

`GET /items/2?include_metadata=true` → `{"id": 2, "name": "Mouse", "total_items": 3}`

---

## 3. Pydantic Request/Response Models

**Q: Why use Pydantic models for request bodies instead of reading `request.json()` directly?**

**A:**
Using Pydantic models provides:
1. **Automatic validation** — FastAPI returns HTTP 422 with field-level errors if data is invalid.
2. **Type coercion** — `"42"` becomes `42` for an `int` field.
3. **Documentation** — the model appears in the generated OpenAPI schema.
4. **Editor support** — IDE autocomplete on the parsed object.

```python
from pydantic import BaseModel, Field

class CreateItemRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    price: float = Field(gt=0, description="Price in USD")
    in_stock: bool = True

class ItemResponse(BaseModel):
    id: int
    name: str
    price: float

@app.post("/items", response_model=ItemResponse, status_code=201)
def create_item(item: CreateItemRequest):
    new_id = max(fake_db.keys(), default=0) + 1
    fake_db[new_id] = item.name
    return ItemResponse(id=new_id, name=item.name, price=item.price)
```

---

## 4. Dependency Injection

**Q: Explain FastAPI's dependency injection system. Give a practical example.**

**A:**
FastAPI uses `Depends()` to inject shared resources — database sessions, authenticated users, config, caching clients — into route handlers without global state.

```python
from fastapi import Depends, Header, HTTPException

def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != "secret-key":
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key

def get_db():
    # Simulates a DB session
    db = {"connection": "active"}
    try:
        yield db
    finally:
        db["connection"] = "closed"

@app.get("/secure-items", dependencies=[Depends(verify_api_key)])
def secure_items(db=Depends(get_db)):
    return {"db_status": db["connection"], "items": list(fake_db.values())}
```

Dependencies are:
- **Reusable** across many endpoints.
- **Composable** — a dependency can have its own dependencies.
- **Testable** — easily overridden in tests with `app.dependency_overrides`.

---

## 5. Async Endpoints

**Q: When should you use `async def` vs `def` in FastAPI route handlers?**

**A:**
- Use `async def` when your handler calls **async I/O** (async database drivers like `asyncpg`, `motor`; async HTTP clients like `httpx.AsyncClient`).
- Use `def` (sync) when calling **blocking I/O** or CPU-heavy code. FastAPI automatically runs sync functions in a thread pool so they don't block the event loop.

```python
import httpx

@app.get("/weather/{city}")
async def get_weather(city: str):
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"https://wttr.in/{city}?format=j1")
        resp.raise_for_status()
        return resp.json()
```

**Never call blocking I/O inside `async def`** — e.g., `time.sleep()`, synchronous `requests.get()` — these stall the event loop and kill performance.

---

## 6. Error Handling

**Q: How do you return custom error responses in FastAPI? What HTTP status codes should you use for common scenarios?**

**A:**
Use `HTTPException` for standard errors, or a custom exception handler for application-wide patterns.

```python
from fastapi import Request
from fastapi.responses import JSONResponse

class InsufficientStockError(Exception):
    def __init__(self, item_id: int, available: int):
        self.item_id = item_id
        self.available = available

@app.exception_handler(InsufficientStockError)
async def stock_error_handler(request: Request, exc: InsufficientStockError):
    return JSONResponse(
        status_code=409,
        content={
            "error": "insufficient_stock",
            "item_id": exc.item_id,
            "available": exc.available,
        },
    )
```

Common status codes:
| Scenario | Code |
|---|---|
| Created successfully | 201 |
| Bad input | 400 |
| Not authenticated | 401 |
| Forbidden | 403 |
| Resource not found | 404 |
| Conflict (duplicate, stock) | 409 |
| Validation error | 422 |
| Server error | 500 |

---

## 7. Background Tasks

**Q: How do you run a task in the background after returning a response in FastAPI?**

**A:**
Use `BackgroundTasks`. The response is sent immediately; the task runs after in the same process.

```python
from fastapi import BackgroundTasks
import smtplib

def send_welcome_email(email: str):
    # simulate email sending
    print(f"Sending welcome email to {email}")

@app.post("/register")
def register_user(email: str, background_tasks: BackgroundTasks):
    # save user to DB...
    background_tasks.add_task(send_welcome_email, email)
    return {"message": "Registration successful"}
```

For heavy or long-running tasks (video processing, ML inference), prefer a task queue like **Celery + Redis** or **arq** rather than `BackgroundTasks`.

---

## 8. Testing FastAPI

**Q: How do you write integration tests for a FastAPI application?**

**A:**
Use `TestClient` (based on `httpx`) and override dependencies to isolate the test from real databases or external services.

```python
from fastapi.testclient import TestClient
from main import app, get_db

def override_get_db():
    return {"connection": "test-mock"}

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

def test_create_item():
    response = client.post("/items", json={"name": "Tablet", "price": 299.99})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Tablet"
    assert "id" in data

def test_get_missing_item():
    response = client.get("/items/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"
```
