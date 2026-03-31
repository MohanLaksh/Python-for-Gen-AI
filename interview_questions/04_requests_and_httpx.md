# HTTP Clients: requests & httpx — Interview Questions & Ideal Answers

---

## 1. Basic HTTP

**Q: What is the difference between GET, POST, PUT, PATCH, and DELETE? When would you use each when calling an AI API?**

**A:**
| Method | Semantics | Idempotent | Body |
|---|---|---|---|
| GET | Read a resource | Yes | No |
| POST | Create / trigger action | No | Yes |
| PUT | Replace entire resource | Yes | Yes |
| PATCH | Partial update | No | Yes |
| DELETE | Remove resource | Yes | No |

In AI API contexts:
- `POST /v1/chat/completions` — send a prompt and get a response (create a completion).
- `GET /v1/models` — list available models.
- `DELETE /v1/files/{id}` — remove an uploaded fine-tune dataset.

---

## 2. requests vs httpx

**Q: Why might you choose `httpx` over `requests` for an AI application?**

**A:**
| Feature | requests | httpx |
|---|---|---|
| Async support | ❌ | ✅ `AsyncClient` |
| HTTP/2 | ❌ | ✅ |
| Streaming | Basic | First-class |
| Timeouts | Global only | Connect + read separate |
| Type hints | Partial | Full |

For GenAI apps:
- LLM streaming responses need efficient chunk-by-chunk processing — `httpx` handles this with `iter_lines()` / `iter_bytes()`.
- Calling multiple LLM endpoints concurrently uses `httpx.AsyncClient` with `asyncio.gather()`.
- OpenAI's Python SDK switched its HTTP layer to `httpx` for these reasons.

---

## 3. Session Management

**Q: What is the benefit of using a `Session` (requests) or `Client` (httpx) instead of module-level functions?**

**A:**
Module-level functions like `requests.get()` create a new connection for every call. A `Session`/`Client`:
- **Reuses TCP connections** (connection pooling) — dramatic speedup for many calls to the same host.
- **Shares configuration** — base URL, default headers, auth, timeout — set once, applied everywhere.
- **Handles cookies** automatically across calls.

```python
import httpx

client = httpx.Client(
    base_url="https://api.openai.com",
    headers={"Authorization": f"Bearer {API_KEY}"},
    timeout=httpx.Timeout(connect=5.0, read=60.0),
)

# All calls reuse the connection pool
response1 = client.post("/v1/embeddings", json={...})
response2 = client.post("/v1/chat/completions", json={...})
client.close()
```

---

## 4. Streaming Responses

**Q: How do you process a streaming response from an LLM API (Server-Sent Events) using httpx?**

**A:**
LLMs like GPT-4 stream tokens via SSE: each line is `data: {...}` with a JSON payload.

```python
import httpx
import json

def stream_completion(prompt: str):
    with httpx.Client(timeout=None) as client:
        with client.stream(
            "POST",
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={
                "model": "gpt-4o",
                "stream": True,
                "messages": [{"role": "user", "content": prompt}],
            },
        ) as response:
            for line in response.iter_lines():
                if line.startswith("data: ") and line != "data: [DONE]":
                    chunk = json.loads(line[6:])
                    delta = chunk["choices"][0]["delta"].get("content", "")
                    print(delta, end="", flush=True)

stream_completion("Explain transformers in one paragraph")
```

---

## 5. Retry Logic

**Q: Implement exponential backoff retry logic for API calls that may hit rate limits (HTTP 429).**

**A:**
```python
import time
import httpx
from typing import Any

def call_with_retry(
    client: httpx.Client,
    method: str,
    url: str,
    max_retries: int = 5,
    **kwargs: Any,
) -> httpx.Response:
    for attempt in range(max_retries):
        response = client.request(method, url, **kwargs)

        if response.status_code == 429:
            wait = 2 ** attempt          # 1, 2, 4, 8, 16 seconds
            retry_after = response.headers.get("Retry-After")
            wait = int(retry_after) if retry_after else wait
            print(f"Rate limited. Waiting {wait}s (attempt {attempt + 1})")
            time.sleep(wait)
            continue

        response.raise_for_status()
        return response

    raise RuntimeError(f"Failed after {max_retries} retries")
```

Production tip: the `tenacity` library provides battle-tested retry decorators with jitter, which prevents thundering-herd problems when many clients retry simultaneously.

---

## 6. Authentication Patterns

**Q: Describe three authentication patterns used in AI APIs and how to implement them with httpx.**

**A:**

**1. Bearer Token (most common — OpenAI, Anthropic)**
```python
headers = {"Authorization": f"Bearer {api_key}"}
```

**2. API Key in Header (Cohere, Hugging Face)**
```python
headers = {"X-API-Key": api_key}
# or
headers = {"api-key": api_key}  # Azure OpenAI
```

**3. API Key in Query Parameter (some legacy APIs)**
```python
params = {"api_key": api_key}
response = client.get("/models", params=params)
```

Best practice — never hardcode keys; read from environment:
```python
import os
api_key = os.environ["OPENAI_API_KEY"]
```

---

## 7. Async Concurrency

**Q: You need to embed 1,000 documents using an embeddings API. How would you do this efficiently with httpx?**

**A:**
Use `asyncio.gather` with a semaphore to batch concurrent requests without overwhelming the API.

```python
import asyncio
import httpx

async def embed_document(client: httpx.AsyncClient, text: str, sem: asyncio.Semaphore) -> list[float]:
    async with sem:
        resp = await client.post(
            "https://api.openai.com/v1/embeddings",
            json={"model": "text-embedding-3-small", "input": text},
        )
        resp.raise_for_status()
        return resp.json()["data"][0]["embedding"]

async def embed_all(documents: list[str]) -> list[list[float]]:
    sem = asyncio.Semaphore(20)  # max 20 concurrent requests
    async with httpx.AsyncClient(
        headers={"Authorization": f"Bearer {API_KEY}"},
        timeout=30.0,
    ) as client:
        tasks = [embed_document(client, doc, sem) for doc in documents]
        return await asyncio.gather(*tasks)

embeddings = asyncio.run(embed_all(my_documents))
```

This reduces 1,000 sequential calls (~100s) to ~5s with 20 concurrent requests.

---

## 8. Timeouts

**Q: What is the difference between a connection timeout and a read timeout? Why is this distinction critical for LLM APIs?**

**A:**
- **Connection timeout**: how long to wait to establish the TCP connection to the server. Should be short (3–10s) — a long wait means the server is unreachable.
- **Read timeout**: how long to wait for the next byte of the response after the connection is open. For LLMs, this must be long (60–300s) because the model may take minutes to generate a long response.

```python
client = httpx.Client(
    timeout=httpx.Timeout(
        connect=5.0,    # fail fast if server unreachable
        read=120.0,     # allow 2 min for LLM generation
        write=10.0,     # sending large prompts
        pool=5.0,       # waiting for a connection from the pool
    )
)
```

Using a single global timeout of 10s would cause premature failures on long-form generation tasks.
