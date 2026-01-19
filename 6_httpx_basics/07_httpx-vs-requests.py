"""
HTTPX vs Requests - Side-by-Side Comparison
===========================================
This file demonstrates the differences between httpx and requests library.
Both are excellent HTTP clients, but httpx offers modern features crucial for Gen AI.
"""

import httpx
import requests
import asyncio
import time


# ============================================================================
# 1. BASIC GET REQUEST - Nearly Identical!
# ============================================================================

def basic_get_comparison():
    """Basic GET requests look almost identical"""
    print("\n" + "="*60)
    print("1. BASIC GET REQUEST")
    print("="*60)
    
    # requests
    print("\nUsing requests:")
    response = requests.get('https://api.github.com/users/octocat')
    print(f"Status: {response.status_code}")
    print(f"User: {response.json()['login']}")
    
    # httpx (sync)
    print("\nUsing httpx (sync):")
    response = httpx.get('https://api.github.com/users/octocat')
    print(f"Status: {response.status_code}")
    print(f"User: {response.json()['login']}")
    
    print("\n✓ Syntax is nearly identical!")


# ============================================================================
# 2. ASYNC SUPPORT - httpx's Superpower!
# ============================================================================

async def async_comparison():
    """Async support - httpx wins here!"""
    print("\n" + "="*60)
    print("2. ASYNC SUPPORT")
    print("="*60)
    
    users = ['octocat', 'torvalds', 'gvanrossum']
    
    # requests - Must be sequential (slow)
    print("\nUsing requests (sequential only):")
    start = time.time()
    for user in users:
        response = requests.get(f'https://api.github.com/users/{user}')
        print(f"  {response.json()['login']}")
    requests_time = time.time() - start
    
    # httpx - Can be concurrent (fast!)
    print("\nUsing httpx (concurrent):")
    start = time.time()
    async with httpx.AsyncClient() as client:
        tasks = [client.get(f'https://api.github.com/users/{user}') for user in users]
        responses = await asyncio.gather(*tasks)
        for response in responses:
            print(f"  {response.json()['login']}")
    httpx_time = time.time() - start
    
    print(f"\nrequests time: {requests_time:.2f}s")
    print(f"httpx time: {httpx_time:.2f}s")
    print(f"✓ httpx is {requests_time/httpx_time:.1f}x faster with async!")


# ============================================================================
# 3. STREAMING - Both Support It
# ============================================================================

def streaming_comparison():
    """Both support streaming, but httpx has better async streaming"""
    print("\n" + "="*60)
    print("3. STREAMING RESPONSES")
    print("="*60)
    
    # requests
    print("\nUsing requests:")
    with requests.get('https://httpbin.org/stream/3', stream=True) as response:
        for line in response.iter_lines():
            if line:
                print(f"  Chunk received")
    
    # httpx (sync)
    print("\nUsing httpx (sync):")
    with httpx.Client() as client:
        with client.stream('GET', 'https://httpbin.org/stream/3') as response:
            for line in response.iter_lines():
                if line:
                    print(f"  Chunk received")
    
    print("\n✓ Both support streaming!")
    print("  But httpx also has async streaming (better for LLMs)")


# ============================================================================
# 4. CLIENT CONFIGURATION - Similar
# ============================================================================

def client_configuration_comparison():
    """Client configuration is similar in both"""
    print("\n" + "="*60)
    print("4. CLIENT CONFIGURATION")
    print("="*60)
    
    # requests
    print("\nUsing requests.Session:")
    session = requests.Session()
    session.headers.update({'User-Agent': 'MyApp/1.0'})
    response = session.get('https://httpbin.org/headers')
    print(f"  Headers sent: {response.json()['headers']['User-Agent']}")
    session.close()
    
    # httpx
    print("\nUsing httpx.Client:")
    with httpx.Client(headers={'User-Agent': 'MyApp/1.0'}) as client:
        response = client.get('https://httpbin.org/headers')
        print(f"  Headers sent: {response.json()['headers']['User-Agent']}")
    
    print("\n✓ Both support client configuration!")


# ============================================================================
# 5. TIMEOUT HANDLING - httpx is More Granular
# ============================================================================

def timeout_comparison():
    """httpx offers more granular timeout control"""
    print("\n" + "="*60)
    print("5. TIMEOUT HANDLING")
    print("="*60)
    
    # requests - Simple timeout
    print("\nUsing requests (simple timeout):")
    try:
        response = requests.get('https://httpbin.org/delay/1', timeout=5.0)
        print(f"  Status: {response.status_code}")
    except requests.Timeout:
        print("  Timed out!")
    
    # httpx - Granular timeout
    print("\nUsing httpx (granular timeout):")
    timeout = httpx.Timeout(
        connect=5.0,
        read=30.0,
        write=5.0,
        pool=5.0
    )
    try:
        response = httpx.get('https://httpbin.org/delay/1', timeout=timeout)
        print(f"  Status: {response.status_code}")
    except httpx.TimeoutException:
        print("  Timed out!")
    
    print("\n✓ httpx offers more granular timeout control!")


# ============================================================================
# 6. HTTP/2 SUPPORT - httpx Only!
# ============================================================================

def http2_comparison():
    """httpx supports HTTP/2, requests doesn't"""
    print("\n" + "="*60)
    print("6. HTTP/2 SUPPORT")
    print("="*60)
    
    print("\nrequests: HTTP/2 not supported ❌")
    
    print("\nhttpx: HTTP/2 supported ✓")
    print("  (Enable with: httpx.Client(http2=True))")
    
    # Note: HTTP/2 requires additional dependencies
    # pip install httpx[http2]


# ============================================================================
# 7. TYPE HINTS - httpx Has Better Support
# ============================================================================

def type_hints_comparison():
    """httpx has better type hint support"""
    print("\n" + "="*60)
    print("7. TYPE HINTS")
    print("="*60)
    
    print("\nrequests: Limited type hints")
    print("httpx: Full type hint support ✓")
    print("\nThis means better IDE autocomplete and type checking!")


# ============================================================================
# 8. PRACTICAL EXAMPLE: LLM API Call
# ============================================================================

async def llm_api_comparison():
    """Comparing LLM API calls"""
    print("\n" + "="*60)
    print("8. LLM API CALL PATTERN")
    print("="*60)
    
    url = "https://httpbin.org/post"
    payload = {
        "model": "gpt-4",
        "messages": [{"role": "user", "content": "Hello!"}]
    }
    
    # requests - Sequential only
    print("\nUsing requests (sequential):")
    prompts = ["Hello", "How are you?", "Goodbye"]
    start = time.time()
    for prompt in prompts:
        payload["messages"][0]["content"] = prompt
        response = requests.post(url, json=payload)
        print(f"  Prompt: {prompt} - Status: {response.status_code}")
    requests_time = time.time() - start
    
    # httpx - Concurrent
    print("\nUsing httpx (concurrent):")
    start = time.time()
    
    async def call_api(client, prompt):
        payload["messages"][0]["content"] = prompt
        response = await client.post(url, json=payload)
        return prompt, response.status_code
    
    async with httpx.AsyncClient() as client:
        tasks = [call_api(client, prompt) for prompt in prompts]
        results = await asyncio.gather(*tasks)
        for prompt, status in results:
            print(f"  Prompt: {prompt} - Status: {status}")
    
    httpx_time = time.time() - start
    
    print(f"\nrequests time: {requests_time:.2f}s")
    print(f"httpx time: {httpx_time:.2f}s")
    print(f"✓ httpx is {requests_time/httpx_time:.1f}x faster!")


# ============================================================================
# 9. MIGRATION GUIDE
# ============================================================================

def migration_guide():
    """How to migrate from requests to httpx"""
    print("\n" + "="*60)
    print("9. MIGRATION GUIDE: requests → httpx")
    print("="*60)
    
    print("""
Most code is identical! Just replace:

requests.get()     → httpx.get()
requests.post()    → httpx.post()
requests.Session() → httpx.Client()

For async (the main benefit):

# Before (requests)
def get_data():
    response = requests.get(url)
    return response.json()

# After (httpx)
async def get_data():
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()

# Run it
result = asyncio.run(get_data())
    """)


# ============================================================================
# 10. WHEN TO USE WHICH?
# ============================================================================

def when_to_use():
    """Decision guide"""
    print("\n" + "="*60)
    print("10. WHEN TO USE WHICH?")
    print("="*60)
    
    print("""
Use httpx when:
✓ Building Gen AI applications (async is crucial!)
✓ Need to make concurrent API calls
✓ Working with streaming responses (LLM APIs)
✓ Want HTTP/2 support
✓ Need better type hints
✓ Starting a new project

Use requests when:
✓ Simple, one-off scripts
✓ Legacy codebase already using requests
✓ Don't need async functionality
✓ Team is more familiar with requests

For Gen AI Development: httpx is HIGHLY RECOMMENDED! 🚀
    """)


# ============================================================================
# SUMMARY TABLE
# ============================================================================

def print_summary():
    """Print comparison summary"""
    print("\n" + "="*60)
    print("SUMMARY: httpx vs requests")
    print("="*60)
    
    print("""
Feature              | requests | httpx
---------------------|----------|-------
Async/await support  | ❌       | ✅
HTTP/2 support       | ❌       | ✅
Streaming            | ✅       | ✅ (better async)
Type hints           | ⚠️       | ✅
API similarity       | -        | ✅ (similar to requests)
Maturity             | ✅       | ✅
Documentation        | ✅       | ✅
Performance (sync)   | ✅       | ✅
Performance (async)  | ❌       | ✅
Connection pooling   | ✅       | ✅
Timeout control      | ✅       | ✅ (more granular)

Recommendation for Gen AI: httpx ✅
    """)


# ============================================================================
# MAIN EXECUTION
# ============================================================================

async def main():
    """Run all comparisons"""
    print("\n" + "="*60)
    print("HTTPX vs REQUESTS - COMPREHENSIVE COMPARISON")
    print("="*60)
    
    basic_get_comparison()
    await async_comparison()
    streaming_comparison()
    client_configuration_comparison()
    timeout_comparison()
    http2_comparison()
    type_hints_comparison()
    await llm_api_comparison()
    migration_guide()
    when_to_use()
    print_summary()
    
    print("\n" + "="*60)
    print("COMPARISON COMPLETED!")
    print("="*60)


if __name__ == "__main__":
    asyncio.run(main())
