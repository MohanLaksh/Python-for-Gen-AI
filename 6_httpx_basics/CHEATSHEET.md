# HTTPX Quick Reference for Gen AI Developers

## Installation
```bash
pip install httpx
```

## Basic Requests

### GET Request
```python
import httpx

# Sync
response = httpx.get('https://api.example.com/data')

# Async
async with httpx.AsyncClient() as client:
    response = await client.get('https://api.example.com/data')
```

### POST Request
```python
# Sync
response = httpx.post('https://api.example.com/endpoint', json={"key": "value"})

# Async
async with httpx.AsyncClient() as client:
    response = await client.post(url, json=payload)
```

## Headers & Authentication

```python
headers = {
    'Authorization': 'Bearer YOUR_API_KEY',
    'Content-Type': 'application/json'
}

response = httpx.get(url, headers=headers)
```

## Timeouts

```python
# Simple timeout (seconds)
response = httpx.get(url, timeout=30.0)

# Advanced timeout
timeout = httpx.Timeout(
    connect=5.0,   # Connection timeout
    read=60.0,     # Read timeout (important for LLMs!)
    write=5.0,     # Write timeout
    pool=5.0       # Pool timeout
)

client = httpx.AsyncClient(timeout=timeout)
```

## Client Configuration

```python
client = httpx.AsyncClient(
    base_url='https://api.openai.com/v1',
    headers={'Authorization': f'Bearer {api_key}'},
    timeout=httpx.Timeout(30.0, read=60.0),
    limits=httpx.Limits(
        max_keepalive_connections=5,
        max_connections=10
    )
)

# Use relative URLs
async with client:
    response = await client.post('/chat/completions', json=payload)
```

## Concurrent Requests

```python
import asyncio

async def fetch_all(urls):
    async with httpx.AsyncClient() as client:
        tasks = [client.get(url) for url in urls]
        responses = await asyncio.gather(*tasks)
        return responses

# Run it
responses = asyncio.run(fetch_all(urls))
```

## Streaming Responses (LLM APIs)

```python
async with httpx.AsyncClient() as client:
    async with client.stream('POST', url, json=payload) as response:
        async for line in response.aiter_lines():
            if line.startswith('data: '):
                data = json.loads(line[6:])
                print(data['content'], end='', flush=True)
```

## Error Handling

```python
try:
    response = await client.post(url, json=payload)
    response.raise_for_status()  # Raises exception for 4xx/5xx
    
except httpx.HTTPStatusError as e:
    print(f"HTTP error: {e.response.status_code}")
    print(f"Details: {e.response.text}")
    
except httpx.TimeoutException:
    print("Request timed out")
    
except httpx.RequestError as e:
    print(f"Request failed: {e}")
```

## Retry with Exponential Backoff

```python
async def call_with_retry(url, payload, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            return response.json()
            
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:  # Rate limit
                wait_time = 2 ** attempt
                await asyncio.sleep(wait_time)
            else:
                raise
                
        except httpx.TimeoutException:
            if attempt == max_retries - 1:
                raise
            await asyncio.sleep(1)
```

## OpenAI Chat Completion

### Non-Streaming
```python
headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}

payload = {
    'model': 'gpt-4',
    'messages': [
        {'role': 'system', 'content': 'You are helpful.'},
        {'role': 'user', 'content': 'Hello!'}
    ],
    'temperature': 0.7
}

async with httpx.AsyncClient(timeout=30.0) as client:
    response = await client.post(
        'https://api.openai.com/v1/chat/completions',
        headers=headers,
        json=payload
    )
    result = response.json()
    print(result['choices'][0]['message']['content'])
```

### Streaming
```python
payload['stream'] = True  # Enable streaming

async with httpx.AsyncClient(timeout=60.0) as client:
    async with client.stream('POST', url, headers=headers, json=payload) as response:
        async for line in response.aiter_lines():
            if line.startswith('data: '):
                data_str = line[6:]
                if data_str == '[DONE]':
                    break
                data = json.loads(data_str)
                content = data['choices'][0]['delta'].get('content', '')
                if content:
                    print(content, end='', flush=True)
```

## Rate Limiting with Semaphore

```python
async def fetch_with_rate_limit(client, url, semaphore):
    async with semaphore:
        return await client.get(url)

# Limit to 5 concurrent requests
semaphore = asyncio.Semaphore(5)

async with httpx.AsyncClient() as client:
    tasks = [
        fetch_with_rate_limit(client, url, semaphore)
        for url in urls
    ]
    results = await asyncio.gather(*tasks)
```

## Response Methods

```python
response = httpx.get(url)

# Status
response.status_code        # 200
response.is_success         # True for 2xx
response.is_error           # True for 4xx/5xx

# Content
response.json()             # Parse as JSON
response.text               # As string
response.content            # As bytes

# Headers
response.headers            # All headers
response.headers['content-type']  # Specific header
```

## Common Patterns

### Batch Processing
```python
async def process_batch(items, batch_size=5):
    results = []
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        batch_results = await asyncio.gather(*[
            process_item(item) for item in batch
        ])
        results.extend(batch_results)
        await asyncio.sleep(1)  # Rate limiting
    return results
```

### Chat Session with History
```python
class ChatSession:
    def __init__(self, api_key):
        self.messages = []
        self.headers = {'Authorization': f'Bearer {api_key}'}
    
    async def send(self, content):
        self.messages.append({'role': 'user', 'content': content})
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=self.headers, json={
                'model': 'gpt-4',
                'messages': self.messages
            })
            
            result = response.json()
            assistant_msg = result['choices'][0]['message']
            self.messages.append(assistant_msg)
            
            return assistant_msg['content']
```

## httpx vs requests

| Feature | httpx | requests |
|---------|-------|----------|
| Async support | ✅ Yes | ❌ No |
| HTTP/2 | ✅ Yes | ❌ No |
| Streaming | ✅ Excellent | ⚠️ Basic |
| Connection pooling | ✅ Built-in | ✅ Built-in |
| Type hints | ✅ Yes | ❌ No |
| API similarity | ✅ Similar to requests | - |

## Quick Tips

1. **Always use async for Gen AI** - LLM APIs benefit from concurrent requests
2. **Set appropriate timeouts** - LLM responses can take 30-60+ seconds
3. **Use streaming for better UX** - Show responses as they're generated
4. **Implement retry logic** - Handle rate limits and transient errors
5. **Reuse clients** - Use context managers for connection pooling
6. **Handle errors gracefully** - Always catch HTTPStatusError and TimeoutException

## Environment Variables

Create a `.env` file:
```bash
OPENAI_API_KEY=your-api-key-here
ANTHROPIC_API_KEY=your-anthropic-key-here
```

Load with python-dotenv:
```python
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
```

---

**For full examples, see the tutorial files in this directory!**
