# HTTPX Tutorial for Gen AI Developers

A comprehensive guide to using the `httpx` Python library for Gen AI applications, with practical examples for working with LLM APIs like OpenAI, Anthropic Claude, and more.

## 📚 Table of Contents

1. [What is httpx?](#what-is-httpx)
2. [Why httpx for Gen AI?](#why-httpx-for-gen-ai)
3. [Installation](#installation)
4. [Quick Start](#quick-start)
5. [File Structure](#file-structure)
6. [Key Concepts](#key-concepts)
7. [Running the Examples](#running-the-examples)
8. [Best Practices](#best-practices)

## What is httpx?

`httpx` is a modern, feature-rich HTTP client for Python that offers:

- **Async/await support** - Perfect for concurrent API calls
- **HTTP/2 support** - Better performance
- **Streaming responses** - Essential for LLM APIs
- **Connection pooling** - Efficient resource usage
- **Type hints** - Better IDE support and code quality

## Why httpx for Gen AI?

Gen AI applications have unique requirements that make httpx ideal:

### 1. **Streaming Responses**
LLM APIs (OpenAI, Anthropic) stream responses token-by-token. httpx handles this elegantly:

```python
async with client.stream('POST', url, json=payload) as response:
    async for line in response.aiter_lines():
        # Process each token as it arrives
        print(line, end='', flush=True)
```

### 2. **Async/Await for Concurrent Calls**
Process multiple prompts simultaneously:

```python
tasks = [call_llm(prompt) for prompt in prompts]
results = await asyncio.gather(*tasks)  # All run concurrently!
```

### 3. **Proper Timeout Handling**
LLM responses can take time. Configure timeouts appropriately:

```python
timeout = httpx.Timeout(connect=5.0, read=60.0)  # 60s for LLM response
client = httpx.AsyncClient(timeout=timeout)
```

### 4. **Connection Pooling**
Reuse connections for better performance:

```python
async with httpx.AsyncClient() as client:
    # All requests reuse the same connection pool
    for prompt in prompts:
        response = await client.post(url, json=payload)
```

## Installation

### Setup Virtual Environment

```bash
# Navigate to the httpx_basics directory
cd "/Users/vinod/Desktop/Desktop - Vinod's MacBook Air/Python for Gen AI/httpx_basics"

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows

# Install httpx
pip install httpx

# Optional: Install additional packages for examples
pip install python-dotenv  # For environment variables
```

### Requirements File

Create a `requirements.txt`:

```txt
httpx>=0.25.0
python-dotenv>=1.0.0
```

Install with:
```bash
pip install -r requirements.txt
```

## Quick Start

### Basic GET Request

```python
import httpx

response = httpx.get('https://api.github.com/users/octocat')
print(response.json())
```

### Basic POST Request (LLM-style)

```python
import httpx

payload = {
    "model": "gpt-4",
    "messages": [{"role": "user", "content": "Hello!"}]
}

response = httpx.post('https://api.openai.com/v1/chat/completions', json=payload)
print(response.json())
```

### Async Request

```python
import httpx
import asyncio

async def main():
    async with httpx.AsyncClient() as client:
        response = await client.get('https://api.github.com/users/octocat')
        print(response.json())

asyncio.run(main())
```

## File Structure

```
httpx_basics/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── 01_httpx-basics.py          # Fundamental httpx operations
├── 04_httpx-async.py           # Async/await patterns
├── 05_httpx-streaming.py       # Streaming responses (crucial for LLMs)
├── 06_httpx-openai.py          # OpenAI API integration
└── venv/                       # Virtual environment (create this)
```

## Key Concepts

### 1. Synchronous vs Asynchronous

**Synchronous** (blocking):
```python
response = httpx.get(url)  # Waits for response
```

**Asynchronous** (non-blocking):
```python
async with httpx.AsyncClient() as client:
    response = await client.get(url)  # Can do other work while waiting
```

### 2. Client Context Managers

**Always use context managers** for automatic resource cleanup:

```python
# Good ✓
async with httpx.AsyncClient() as client:
    response = await client.get(url)

# Bad ✗
client = httpx.AsyncClient()
response = await client.get(url)
# Forgot to close client!
```

### 3. Timeouts

**Always set timeouts** to prevent hanging:

```python
timeout = httpx.Timeout(
    connect=5.0,   # Time to establish connection
    read=60.0,     # Time to read response (important for LLMs!)
    write=5.0,     # Time to send request
    pool=5.0       # Time to get connection from pool
)

client = httpx.AsyncClient(timeout=timeout)
```

### 4. Error Handling

```python
try:
    response = await client.post(url, json=payload)
    response.raise_for_status()  # Raises exception for 4xx/5xx
    
except httpx.HTTPStatusError as e:
    print(f"HTTP error: {e.response.status_code}")
    
except httpx.TimeoutException:
    print("Request timed out")
    
except httpx.RequestError as e:
    print(f"Request failed: {e}")
```

### 5. Streaming

**Essential for LLM APIs:**

```python
async with client.stream('POST', url, json=payload) as response:
    async for line in response.aiter_lines():
        if line.startswith('data: '):
            data = json.loads(line[6:])
            print(data['content'], end='', flush=True)
```

## Running the Examples

### 1. Basic Examples

```bash
# Activate virtual environment
source venv/bin/activate

# Run basic examples
python 01_httpx-basics.py
```

### 2. Async Examples

```bash
python 04_httpx-async.py
```

### 3. Streaming Examples

```bash
python 05_httpx-streaming.py
```

### 4. OpenAI Examples

**Important:** Set your API key first!

```bash
# Set environment variable
export OPENAI_API_KEY='your-api-key-here'

# Or create a .env file
echo "OPENAI_API_KEY=your-api-key-here" > .env

# Run examples
python 06_httpx-openai.py
```

## Best Practices

### 1. Use Async for Gen AI Applications

```python
# ✓ Good - Concurrent API calls
async def process_prompts(prompts):
    async with httpx.AsyncClient() as client:
        tasks = [call_llm(client, p) for p in prompts]
        return await asyncio.gather(*tasks)

# ✗ Bad - Sequential API calls
def process_prompts(prompts):
    results = []
    for prompt in prompts:
        results.append(call_llm(prompt))  # Slow!
    return results
```

### 2. Configure Clients Properly

```python
# ✓ Good - Reusable client with proper config
client = httpx.AsyncClient(
    base_url='https://api.openai.com/v1',
    headers={'Authorization': f'Bearer {api_key}'},
    timeout=httpx.Timeout(60.0, read=120.0),
    limits=httpx.Limits(max_keepalive_connections=5)
)

# ✗ Bad - Creating new client for each request
for prompt in prompts:
    client = httpx.AsyncClient()  # Inefficient!
    response = await client.post(...)
```

### 3. Handle Errors Gracefully

```python
# ✓ Good - Comprehensive error handling
async def call_api_with_retry(url, payload, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            return response.json()
            
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:  # Rate limit
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
            else:
                raise
                
        except httpx.TimeoutException:
            if attempt == max_retries - 1:
                raise
            await asyncio.sleep(1)
```

### 4. Use Streaming for Better UX

```python
# ✓ Good - Stream responses for immediate feedback
async def stream_response(prompt):
    async with client.stream('POST', url, json=payload) as response:
        print("AI: ", end='', flush=True)
        async for chunk in response.aiter_lines():
            print(chunk, end='', flush=True)
        print()

# ✗ Bad - Wait for entire response
async def wait_for_response(prompt):
    response = await client.post(url, json=payload)
    print(response.json())  # User waits for entire response
```

### 5. Manage Conversation History

```python
class ChatSession:
    def __init__(self, api_key):
        self.messages = []
        self.client = httpx.AsyncClient(
            headers={'Authorization': f'Bearer {api_key}'}
        )
    
    async def send_message(self, content):
        self.messages.append({'role': 'user', 'content': content})
        
        response = await self.client.post(url, json={
            'messages': self.messages  # Include history
        })
        
        assistant_msg = response.json()['choices'][0]['message']
        self.messages.append(assistant_msg)
        
        return assistant_msg['content']
```

## Common Patterns for Gen AI

### Pattern 1: Batch Processing

```python
async def process_batch(prompts, batch_size=5):
    """Process prompts in batches to avoid rate limits"""
    results = []
    
    for i in range(0, len(prompts), batch_size):
        batch = prompts[i:i + batch_size]
        batch_results = await asyncio.gather(*[
            call_llm(prompt) for prompt in batch
        ])
        results.extend(batch_results)
        
        # Rate limiting
        if i + batch_size < len(prompts):
            await asyncio.sleep(1)
    
    return results
```

### Pattern 2: Fallback to Different Models

```python
async def call_with_fallback(prompt, models=['gpt-4', 'gpt-3.5-turbo']):
    """Try multiple models if one fails"""
    for model in models:
        try:
            return await call_llm(prompt, model=model)
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:
                continue  # Try next model
            raise
    
    raise Exception("All models failed")
```

### Pattern 3: Caching Responses

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def cache_key(prompt):
    return hash(prompt)

async def call_with_cache(prompt):
    """Cache LLM responses to save costs"""
    key = cache_key(prompt)
    
    if key in cache:
        return cache[key]
    
    response = await call_llm(prompt)
    cache[key] = response
    return response
```

## Troubleshooting

### Issue: "Connection pool is full"

**Solution:** Increase connection limits

```python
limits = httpx.Limits(
    max_keepalive_connections=10,
    max_connections=20
)
client = httpx.AsyncClient(limits=limits)
```

### Issue: "Request timed out"

**Solution:** Increase timeout for LLM responses

```python
timeout = httpx.Timeout(connect=5.0, read=120.0)  # 2 minutes for read
```

### Issue: "Rate limit exceeded"

**Solution:** Implement exponential backoff

```python
async def call_with_backoff(url, payload, max_retries=5):
    for i in range(max_retries):
        try:
            return await client.post(url, json=payload)
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:
                wait = (2 ** i) + random.random()
                await asyncio.sleep(wait)
            else:
                raise
```

## Additional Resources

- [httpx Documentation](https://www.python-httpx.org/)
- [OpenAI API Documentation](https://platform.openai.com/docs/api-reference)
- [Anthropic API Documentation](https://docs.anthropic.com/)
- [Python asyncio Documentation](https://docs.python.org/3/library/asyncio.html)

## Next Steps

1. ✅ Complete the basic examples in `01_httpx-basics.py`
2. ✅ Learn async patterns in `04_httpx-async.py`
3. ✅ Master streaming in `05_httpx-streaming.py`
4. ✅ Try OpenAI integration in `06_httpx-openai.py`
5. 🚀 Build your own Gen AI application!

---

**Happy coding! 🎉**

For questions or issues, refer to the [httpx documentation](https://www.python-httpx.org/) or the example files in this directory.
