"""
HTTPX Async Operations for Gen AI Developers
=============================================
Asynchronous HTTP requests are crucial for Gen AI applications because:
1. LLM APIs can take seconds to respond
2. You often need to make multiple API calls concurrently
3. Async patterns prevent blocking your application

This module demonstrates async/await patterns with httpx.
"""

import httpx
import asyncio
import time
import json
from typing import List, Dict, Any


# ============================================================================
# 1. BASIC ASYNC REQUEST
# ============================================================================

async def basic_async_request():
    """Simple async GET request"""
    print("\n" + "="*60)
    print("1. BASIC ASYNC REQUEST")
    print("="*60)
    
    async with httpx.AsyncClient() as client:
        response = await client.get('https://api.github.com/users/octocat')
        data = response.json()
        print(f"User: {data['login']}")
        print(f"Followers: {data['followers']}")


# ============================================================================
# 2. CONCURRENT REQUESTS (The Power of Async!)
# ============================================================================

async def concurrent_requests():
    """Making multiple requests concurrently - huge performance boost"""
    print("\n" + "="*60)
    print("2. CONCURRENT REQUESTS")
    print("="*60)
    
    users = ['octocat', 'torvalds', 'gvanrossum', 'tj', 'sindresorhus']
    
    async with httpx.AsyncClient() as client:
        # Sequential (slow)
        start_time = time.time()
        for user in users[:2]:
            response = await client.get(f'https://api.github.com/users/{user}')
            print(f"Sequential: {response.json()['login']}")
        sequential_time = time.time() - start_time
        
        # Concurrent (fast!)
        start_time = time.time()
        tasks = [
            client.get(f'https://api.github.com/users/{user}')
            for user in users
        ]
        responses = await asyncio.gather(*tasks)
        
        for response in responses:
            data = response.json()
            print(f"Concurrent: {data['login']} - {data['public_repos']} repos")
        
        concurrent_time = time.time() - start_time
        
        print(f"\nSequential time: {sequential_time:.2f}s")
        print(f"Concurrent time: {concurrent_time:.2f}s")
        print(f"Speedup: {sequential_time/concurrent_time:.2f}x faster!")


# ============================================================================
# 3. ASYNC POST REQUESTS (For LLM APIs)
# ============================================================================

async def async_post_request():
    """Async POST request - typical pattern for AI API calls"""
    print("\n" + "="*60)
    print("3. ASYNC POST REQUEST")
    print("="*60)
    
    url = "https://httpbin.org/post"
    
    payload = {
        "model": "gpt-4",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What is async programming?"}
        ],
        "temperature": 0.7
    }
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(url, json=payload)
        result = response.json()
        print(f"Status: {response.status_code}")
        print(f"Payload sent: {json.dumps(result['json'], indent=2)}")


# ============================================================================
# 4. ERROR HANDLING IN ASYNC
# ============================================================================

async def async_error_handling():
    """Proper error handling in async context"""
    print("\n" + "="*60)
    print("4. ASYNC ERROR HANDLING")
    print("="*60)
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                'https://api.github.com/users/thisuserdoesnotexist12345'
            )
            response.raise_for_status()
            
        except httpx.HTTPStatusError as e:
            print(f"HTTP Error: {e.response.status_code}")
            
        except httpx.RequestError as e:
            print(f"Request failed: {e}")
            
        except httpx.TimeoutException:
            print("Request timed out")


# ============================================================================
# 5. CONCURRENT API CALLS WITH ERROR HANDLING
# ============================================================================

async def fetch_user(client: httpx.AsyncClient, username: str) -> Dict[str, Any]:
    """Fetch a single user with error handling"""
    try:
        response = await client.get(f'https://api.github.com/users/{username}')
        response.raise_for_status()
        return {
            'success': True,
            'username': username,
            'data': response.json()
        }
    except Exception as e:
        return {
            'success': False,
            'username': username,
            'error': str(e)
        }


async def concurrent_with_error_handling():
    """Making multiple concurrent requests with proper error handling"""
    print("\n" + "="*60)
    print("5. CONCURRENT REQUESTS WITH ERROR HANDLING")
    print("="*60)
    
    users = ['octocat', 'torvalds', 'invaliduser12345', 'gvanrossum']
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        tasks = [fetch_user(client, user) for user in users]
        results = await asyncio.gather(*tasks)
        
        for result in results:
            if result['success']:
                data = result['data']
                print(f"✓ {result['username']}: {data['public_repos']} repos")
            else:
                print(f"✗ {result['username']}: {result['error']}")


# ============================================================================
# 6. RATE LIMITING WITH ASYNC
# ============================================================================

async def rate_limited_requests():
    """Implementing rate limiting for API calls"""
    print("\n" + "="*60)
    print("6. RATE LIMITED REQUESTS")
    print("="*60)
    
    async def fetch_with_rate_limit(
        client: httpx.AsyncClient,
        url: str,
        semaphore: asyncio.Semaphore
    ):
        """Fetch URL with rate limiting using semaphore"""
        async with semaphore:
            response = await client.get(url)
            return response.json()
    
    # Limit to 3 concurrent requests
    semaphore = asyncio.Semaphore(3)
    
    users = ['octocat', 'torvalds', 'gvanrossum', 'tj', 'sindresorhus']
    
    async with httpx.AsyncClient() as client:
        tasks = [
            fetch_with_rate_limit(
                client,
                f'https://api.github.com/users/{user}',
                semaphore
            )
            for user in users
        ]
        
        results = await asyncio.gather(*tasks)
        
        for result in results:
            print(f"User: {result['login']}, Repos: {result['public_repos']}")


# ============================================================================
# 7. TIMEOUT CONFIGURATION IN ASYNC
# ============================================================================

async def async_timeout_handling():
    """Advanced timeout handling for async requests"""
    print("\n" + "="*60)
    print("7. ASYNC TIMEOUT HANDLING")
    print("="*60)
    
    # Configure different timeouts
    timeout = httpx.Timeout(
        connect=5.0,   # Connection timeout
        read=30.0,     # Read timeout (important for LLM responses)
        write=5.0,     # Write timeout
        pool=5.0       # Pool timeout
    )
    
    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            response = await client.get('https://httpbin.org/delay/2')
            print(f"Request completed: {response.status_code}")
        except httpx.TimeoutException as e:
            print(f"Timeout occurred: {e}")


# ============================================================================
# 8. STREAMING RESPONSES (Preview - detailed in 05_httpx-streaming.py)
# ============================================================================

async def async_streaming_preview():
    """Preview of streaming responses - crucial for LLM APIs"""
    print("\n" + "="*60)
    print("8. ASYNC STREAMING PREVIEW")
    print("="*60)
    
    async with httpx.AsyncClient() as client:
        async with client.stream('GET', 'https://httpbin.org/stream/5') as response:
            print(f"Status: {response.status_code}")
            print("Streaming response chunks:")
            
            async for chunk in response.aiter_lines():
                if chunk:
                    data = json.loads(chunk)
                    print(f"  Chunk {data['id']}: {data['url']}")


# ============================================================================
# 9. PRACTICAL EXAMPLE: Multiple LLM API Calls
# ============================================================================

async def mock_multiple_llm_calls():
    """Simulating multiple concurrent LLM API calls"""
    print("\n" + "="*60)
    print("9. MULTIPLE CONCURRENT LLM API CALLS")
    print("="*60)
    
    prompts = [
        "Explain quantum computing",
        "What is machine learning?",
        "Describe neural networks",
    ]
    
    async def call_llm_api(client: httpx.AsyncClient, prompt: str) -> Dict:
        """Simulate an LLM API call"""
        payload = {
            "model": "gpt-4",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7
        }
        
        # Using httpbin to simulate the API
        response = await client.post(
            'https://httpbin.org/post',
            json=payload,
            timeout=30.0
        )
        
        return {
            'prompt': prompt,
            'status': response.status_code,
            'response_time': response.elapsed.total_seconds()
        }
    
    async with httpx.AsyncClient() as client:
        start_time = time.time()
        
        tasks = [call_llm_api(client, prompt) for prompt in prompts]
        results = await asyncio.gather(*tasks)
        
        total_time = time.time() - start_time
        
        print(f"\nProcessed {len(prompts)} prompts concurrently:")
        for result in results:
            print(f"  • '{result['prompt'][:30]}...' - {result['status']} "
                  f"({result['response_time']:.2f}s)")
        
        print(f"\nTotal time: {total_time:.2f}s")
        print(f"Average time per request: {total_time/len(prompts):.2f}s")


# ============================================================================
# 10. ASYNC CLIENT CONFIGURATION
# ============================================================================

async def async_client_configuration():
    """Configuring an async client for a specific API"""
    print("\n" + "="*60)
    print("10. ASYNC CLIENT CONFIGURATION")
    print("="*60)
    
    # Configure client for OpenAI-like API
    client = httpx.AsyncClient(
        base_url='https://api.github.com',
        headers={
            'User-Agent': 'GenAI-App/1.0',
            'Accept': 'application/json'
        },
        timeout=httpx.Timeout(30.0, read=60.0),  # Longer read timeout for LLMs
        limits=httpx.Limits(
            max_keepalive_connections=5,
            max_connections=10
        )
    )
    
    async with client:
        # Use relative URLs
        response = await client.get('/users/octocat')
        print(f"User: {response.json()['login']}")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

async def main():
    """Run all async examples"""
    print("\n" + "="*60)
    print("HTTPX ASYNC OPERATIONS FOR GEN AI DEVELOPERS")
    print("="*60)
    
    await basic_async_request()
    await concurrent_requests()
    await async_post_request()
    await async_error_handling()
    await concurrent_with_error_handling()
    await rate_limited_requests()
    await async_timeout_handling()
    await async_streaming_preview()
    await mock_multiple_llm_calls()
    await async_client_configuration()
    
    print("\n" + "="*60)
    print("ALL ASYNC EXAMPLES COMPLETED!")
    print("="*60)


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
