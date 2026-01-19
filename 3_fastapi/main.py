from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Annotated

from fastapi import Body, FastAPI, HTTPException, Path, Query, status
from pydantic import BaseModel, Field

app = FastAPI(
    title="FastAPI Examples",
    description=(
        "Small API showcasing common FastAPI patterns:\n"
        "- Path + query parameters\n"
        "- Request body + validation\n"
        "- Response models\n"
        "- Helpful examples in the OpenAPI docs\n"
    ),
    version="1.0.0",
)


class HealthResponse(BaseModel):
    status: str = Field(examples=["ok"])
    time_utc: datetime = Field(examples=["2026-01-19T12:34:56Z"])


class ItemCategory(str, Enum):
    book = "book"
    gadget = "gadget"
    grocery = "grocery"


class ItemCreate(BaseModel):
    name: str = Field(min_length=1, max_length=60, examples=["Wireless Mouse"])
    price: float = Field(gt=0, examples=[24.99])
    category: ItemCategory = Field(examples=["gadget"])
    tags: list[str] = Field(default_factory=list, examples=[["office", "sale"]])


class Item(ItemCreate):
    id: int = Field(ge=1, examples=[1])
    created_at_utc: datetime = Field(examples=["2026-01-19T12:34:56Z"])


# Simple in-memory "database" for demo purposes.
ITEMS: dict[int, Item] = {}
NEXT_ID = 1


@app.get(
    "/",
    summary="Welcome",
    description="Basic root endpoint with a tiny payload example.",
)
def read_root() -> dict[str, str]:
    return {"message": "Hello, World"}


@app.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
    tags=["ops"],
)
def health() -> HealthResponse:
    return HealthResponse(status="ok", time_utc=datetime.now(timezone.utc))


@app.get(
    "/items/{item_id}",
    response_model=Item,
    summary="Get an item by id",
    tags=["items"],
)
def get_item(
    item_id: Annotated[int, Path(ge=1, examples=[1])],
    q: Annotated[
        str | None,
        Query(
            description="Optional search string to echo back (demo).",
            examples={"simple": {"value": "red"}, "multi": {"value": "wireless mouse"}},
        ),
    ] = None,
) -> Item:
    item = ITEMS.get(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} not found",
        )
    # q is intentionally unused besides showing query-params in docs.
    _ = q
    return item


@app.get(
    "/items",
    response_model=list[Item],
    summary="List items",
    tags=["items"],
)
def list_items(
    limit: Annotated[int, Query(ge=1, le=100, examples=[10])] = 10,
    offset: Annotated[int, Query(ge=0, examples=[0])] = 0,
    category: Annotated[ItemCategory | None, Query(examples=["gadget"])] = None,
) -> list[Item]:
    items = list(ITEMS.values())
    if category is not None:
        items = [i for i in items if i.category == category]
    return items[offset : offset + limit]


@app.post(
    "/items",
    response_model=Item,
    status_code=status.HTTP_201_CREATED,
    summary="Create an item",
    tags=["items"],
)
def create_item(
    payload: Annotated[
        ItemCreate,
        Body(
            examples={
                "gadget": {
                    "summary": "A gadget",
                    "value": {
                        "name": "Wireless Mouse",
                        "price": 24.99,
                        "category": "gadget",
                        "tags": ["office", "sale"],
                    },
                },
                "book": {
                    "summary": "A book",
                    "value": {
                        "name": "Deep Learning 101",
                        "price": 39.5,
                        "category": "book",
                        "tags": ["ml", "study"],
                    },
                },
            }
        ),
    ],
) -> Item:
    global NEXT_ID
    item = Item(
        id=NEXT_ID,
        created_at_utc=datetime.now(timezone.utc),
        **payload.model_dump(),
    )
    ITEMS[item.id] = item
    NEXT_ID += 1
    return item


@app.delete(
    "/items/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an item",
    tags=["items"],
)
def delete_item(item_id: Annotated[int, Path(ge=1, examples=[1])]) -> None:
    if item_id not in ITEMS:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} not found",
        )
    del ITEMS[item_id]
    return None


# Run the server:
# - fastapi dev main.py
# - fastapi run main.py