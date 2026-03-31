# Async Programming & Performance — Interview Questions & Ideal Answers

---

## 1. Async Fundamentals

**Q: Explain the difference between `threading`, `multiprocessing`, and `asyncio`. Which is best for LLM applications?**

**A:**

| Model | Parallelism | Best for | Limitation |
|---|---|---|---|
| `threading` | Concurrent (GIL limits true parallel) | I/O-bound tasks | GIL prevents CPU parallelism in CPython |
| `multiprocessing` | True parallel | CPU-bound tasks (ML inference) | High memory overhead; slow IPC |
| `asyncio` | Cooperative concurrency | Many concurrent I/O-bound tasks | Single-threaded; blocking code freezes all |

For LLM applications, **asyncio is the right choice** because:
- LLM API calls are I/O-bound (waiting for the network).
- You can make hundreds of concurrent API calls with a single thread.
- Python's async ecosystem (httpx, asyncpg, aiofiles) is mature.

```python
import asyncio
import httpx

async def call_llm(client: httpx.AsyncClient, prompt: str) -> str:
    resp = await client.post("/v1/chat/completions", json={"messages": [{"role": "user", "content": prompt}]})
    return resp.json()["choices"][0]["message"]["content"]

async def batch_process(prompts: list[str]) -> list[str]:
    async with httpx.AsyncClient(base_url="https://api.openai.com", timeout=60) as client:
        tasks = [call_llm(client, p) for p in prompts]
        return await asyncio.gather(*tasks)

# Process 50 prompts concurrently
results = asyncio.run(batch_process(my_prompts))
```

---

## 2. Event Loop & Blocking

**Q: What happens when you call a blocking function inside an async function? How do you fix it?**

**A:**
A blocking call (e.g., `time.sleep`, `requests.get`, CPU-heavy computation) **freezes the entire event loop** — no other coroutines can run until it returns.

```python
# BAD — blocks event loop for 2 seconds
async def bad_handler(query: str) -> str:
    time.sleep(2)         # blocks everything
    return process(query)

# GOOD — option 1: use async equivalent
async def good_handler_io(query: str) -> str:
    await asyncio.sleep(2)   # yields control
    return process(query)

# GOOD — option 2: run blocking code in thread pool
async def good_handler_cpu(data: bytes) -> str:
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, cpu_heavy_function, data)
    return result
```

---

## 3. Semaphores & Rate Limiting

**Q: How do you rate-limit concurrent API calls without a dedicated library?**

**A:**
Use `asyncio.Semaphore` to cap concurrency, and a token bucket or sliding window for requests-per-second limits:

```python
import asyncio
import time
from collections import deque

class RateLimiter:
    """Token bucket: max `rate` calls per second."""
    def __init__(self, rate: int):
        self.rate = rate
        self.tokens = rate
        self.last_refill = time.monotonic()
        self._lock = asyncio.Lock()

    async def acquire(self):
        async with self._lock:
            now = time.monotonic()
            elapsed = now - self.last_refill
            self.tokens = min(self.rate, self.tokens + elapsed * self.rate)
            self.last_refill = now
            if self.tokens < 1:
                wait = (1 - self.tokens) / self.rate
                await asyncio.sleep(wait)
                self.tokens = 0
            else:
                self.tokens -= 1

limiter = RateLimiter(rate=10)  # 10 requests/second
semaphore = asyncio.Semaphore(20)  # max 20 concurrent

async def safe_call(client, prompt: str) -> str:
    async with semaphore:
        await limiter.acquire()
        return await call_llm(client, prompt)
```

---

## 4. Generator-based Streaming

**Q: How do you pipe a streaming LLM response to a user in real time with FastAPI?**

**A:**
Use `StreamingResponse` with an async generator:

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import httpx

app = FastAPI()

async def llm_stream(prompt: str):
    async with httpx.AsyncClient(timeout=None) as client:
        async with client.stream(
            "POST",
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={"model": "gpt-4o", "stream": True, "messages": [{"role": "user", "content": prompt}]},
        ) as response:
            async for line in response.aiter_lines():
                if line.startswith("data: ") and line != "data: [DONE]":
                    import json
                    chunk = json.loads(line[6:])
                    delta = chunk["choices"][0]["delta"].get("content", "")
                    if delta:
                        yield f"data: {delta}\n\n"

@app.post("/stream")
async def stream_endpoint(prompt: str):
    return StreamingResponse(
        llm_stream(prompt),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
```

---

## 5. Caching

**Q: How would you implement prompt-response caching to reduce API costs by 40–60%?**

**A:**
Cache identical prompts (at temperature=0) using a hash key:

```python
import hashlib
import json
import redis.asyncio as redis

class LLMCache:
    def __init__(self, ttl_seconds: int = 3600):
        self.redis = redis.Redis.from_url("redis://localhost:6379")
        self.ttl = ttl_seconds

    def _key(self, prompt: str, model: str) -> str:
        payload = json.dumps({"prompt": prompt, "model": model}, sort_keys=True)
        return f"llm:{hashlib.sha256(payload.encode()).hexdigest()}"

    async def get(self, prompt: str, model: str) -> str | None:
        return await self.redis.get(self._key(prompt, model))

    async def set(self, prompt: str, model: str, response: str) -> None:
        await self.redis.setex(self._key(prompt, model), self.ttl, response)

cache = LLMCache()

async def cached_llm_call(prompt: str, model: str = "gpt-4o-mini") -> str:
    cached = await cache.get(prompt, model)
    if cached:
        return cached.decode()  # cache hit

    response = await async_call_llm(prompt, model)
    await cache.set(prompt, model, response)
    return response
```

**Note:** Only cache deterministic calls (temperature=0). Never cache personalised or time-sensitive responses.

---

## 6. Performance Profiling

**Q: How do you identify performance bottlenecks in a Python GenAI application?**

**A:**

**1. Profile CPU:**
```python
import cProfile
cProfile.run("my_function()", sort="cumulative")
# or use py-spy for production without code changes:
# py-spy top --pid <pid>
```

**2. Profile async code:**
```python
# Use asyncio debug mode
import asyncio
asyncio.run(main(), debug=True)
# Logs coroutines that take > 0.1s — reveals blocking calls
```

**3. Trace LLM latency components:**
```
Total latency = network_to_api + queue_time + time_to_first_token + generation_time
```
- `time_to_first_token` (TTFT): measures prompt processing latency.
- `tokens_per_second`: measures generation throughput.

**4. Key metrics to monitor in production:**
- P50/P95/P99 latency per endpoint.
- Token throughput (tokens/second).
- Cache hit rate.
- Error rate by type (429, 500, timeout).
- Cost per request (tokens × price).

---

## 7. Memory Leaks

**Q: What are common memory leaks in Python async LLM applications and how do you detect them?**

**A:**

**Common causes:**
1. **Unclosed HTTP clients** — `httpx.AsyncClient` not used as context manager leaks connections.
2. **Growing conversation history** — unbounded list of messages in memory.
3. **Task references** — `asyncio.create_task()` results not awaited or cancelled leak tasks.
4. **Circular references with closures** — callbacks capturing large objects.

**Detection:**
```python
import tracemalloc

tracemalloc.start()

# ... run workload ...

snapshot = tracemalloc.take_snapshot()
top = snapshot.statistics("lineno")
for stat in top[:10]:
    print(stat)
# Shows top memory allocators by file/line
```

**Prevention:**
```python
# Always use context manager for clients
async with httpx.AsyncClient() as client:
    ...

# Cap conversation history
MAX_MESSAGES = 20
messages = messages[-MAX_MESSAGES:]

# Cancel dangling tasks on shutdown
async def shutdown():
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    for task in tasks:
        task.cancel()
    await asyncio.gather(*tasks, return_exceptions=True)
```
