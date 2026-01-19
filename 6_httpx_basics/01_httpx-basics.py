"""
HTTPX Basics for Gen AI Developers
===================================
This module covers fundamental httpx operations essential for working with AI APIs.

httpx is a modern, async-capable HTTP client for Python that's perfect for:
- Making requests to LLM APIs (OpenAI, Anthropic, etc.)
- Handling streaming responses
- Managing connection pools efficiently
- Supporting both sync and async patterns
"""

import httpx
import json
import os
from typing import Dict, Any


# ============================================================================
# 1. BASIC GET REQUESTS
# ============================================================================

def basic_get_request():
    """Simple GET request - the foundation of API calls"""
    print("\n" + "="*60)
    print("1. BASIC GET REQUEST")
    print("="*60)
    
    # Create a client and make a request
    response = httpx.get('https://api.github.com/users/octocat')
    
    print(f"Status Code: {response.status_code}")
    print(f"Headers: {dict(response.headers)}")
    print(f"Response Body: {response.json()}")
    
    # Check if request was successful
    if response.status_code == 200:
        data = response.json()
        print(f"\nUser: {data['name']}")
        print(f"Bio: {data['bio']}")


# ============================================================================
# 2. BASIC POST REQUESTS
# ============================================================================

def basic_post_request():
    """POST request with JSON payload - common for AI APIs"""
    print("\n" + "="*60)
    print("2. BASIC POST REQUEST")
    print("="*60)
    
    # Example: Simulating an API call structure similar to LLM APIs
    url = "https://httpbin.org/post"
    
    payload = {
        "model": "gpt-4",
        "messages": [
            {"role": "user", "content": "Hello, AI!"}
        ],
        "temperature": 0.7
    }
    
    response = httpx.post(url, json=payload)
    
    print(f"Status Code: {response.status_code}")
    print(f"Request sent: {json.dumps(payload, indent=2)}")
    print(f"Response: {response.json()['json']}")


# ============================================================================
# 3. USING CLIENT CONTEXT MANAGER
# ============================================================================

def using_client_context():
    """Using httpx.Client for connection reuse - more efficient"""
    print("\n" + "="*60)
    print("3. USING CLIENT CONTEXT MANAGER")
    print("="*60)
    
    # Client reuses connections - important for multiple API calls
    with httpx.Client() as client:
        # Make multiple requests efficiently
        urls = [
            'https://api.github.com/users/octocat',
            'https://api.github.com/users/torvalds',
        ]
        
        for url in urls:
            response = client.get(url)
            data = response.json()
            print(f"User: {data['login']}, Repos: {data['public_repos']}")


# ============================================================================
# 4. CUSTOM HEADERS (Essential for API Authentication)
# ============================================================================

def custom_headers():
    """Adding custom headers - crucial for API authentication"""
    print("\n" + "="*60)
    print("4. CUSTOM HEADERS")
    print("="*60)
    
    headers = {
        'Authorization': 'Bearer YOUR_API_KEY_HERE',
        'Content-Type': 'application/json',
        'User-Agent': 'MyGenAIApp/1.0',
    }
    
    # Example with httpbin to echo back our headers
    response = httpx.get('https://httpbin.org/headers', headers=headers)
    
    print("Headers sent:")
    print(json.dumps(response.json()['headers'], indent=2))


# ============================================================================
# 5. QUERY PARAMETERS
# ============================================================================

def query_parameters():
    """Using query parameters in requests"""
    print("\n" + "="*60)
    print("5. QUERY PARAMETERS")
    print("="*60)
    
    # Two ways to add query parameters
    
    # Method 1: In URL
    response1 = httpx.get('https://httpbin.org/get?key1=value1&key2=value2')
    
    # Method 2: Using params argument (preferred)
    params = {
        'key1': 'value1',
        'key2': 'value2',
        'search': 'artificial intelligence'
    }
    response2 = httpx.get('https://httpbin.org/get', params=params)
    
    print("Query parameters sent:")
    print(json.dumps(response2.json()['args'], indent=2))


# ============================================================================
# 6. TIMEOUT HANDLING (Critical for AI APIs)
# ============================================================================

def timeout_handling():
    """Setting timeouts - essential for AI API calls that may take time"""
    print("\n" + "="*60)
    print("6. TIMEOUT HANDLING")
    print("="*60)
    
    # Set timeout to 10 seconds
    try:
        response = httpx.get(
            'https://httpbin.org/delay/2',
            timeout=10.0  # 10 seconds timeout
        )
        print(f"Request completed in time: {response.status_code}")
    except httpx.TimeoutException:
        print("Request timed out!")
    
    # Different timeouts for connect vs read
    timeout_config = httpx.Timeout(
        connect=5.0,  # 5 seconds to establish connection
        read=30.0,    # 30 seconds to read response (important for LLMs)
        write=5.0,    # 5 seconds to write request
        pool=5.0      # 5 seconds to get connection from pool
    )
    
    with httpx.Client(timeout=timeout_config) as client:
        response = client.get('https://httpbin.org/delay/1')
        print(f"Request with custom timeout config: {response.status_code}")


# ============================================================================
# 7. ERROR HANDLING
# ============================================================================

def error_handling():
    """Proper error handling for robust applications"""
    print("\n" + "="*60)
    print("7. ERROR HANDLING")
    print("="*60)
    
    try:
        response = httpx.get('https://api.github.com/users/nonexistentuser12345')
        response.raise_for_status()  # Raises exception for 4xx/5xx status codes
        
    except httpx.HTTPStatusError as e:
        print(f"HTTP Error: {e.response.status_code}")
        print(f"Response: {e.response.text}")
        
    except httpx.RequestError as e:
        print(f"Request Error: {e}")
        
    except httpx.TimeoutException:
        print("Request timed out")


# ============================================================================
# 8. RESPONSE METHODS
# ============================================================================

def response_methods():
    """Understanding different ways to access response data"""
    print("\n" + "="*60)
    print("8. RESPONSE METHODS")
    print("="*60)
    
    response = httpx.get('https://api.github.com/users/octocat')
    
    # Different ways to access response
    print(f"Status Code: {response.status_code}")
    print(f"Is Success (2xx): {response.is_success}")
    print(f"Is Error (4xx/5xx): {response.is_error}")
    
    # Response content in different formats
    print(f"\nAs JSON: {type(response.json())}")
    print(f"As Text: {type(response.text)}")
    print(f"As Bytes: {type(response.content)}")
    
    # Access specific headers
    print(f"\nContent-Type: {response.headers.get('content-type')}")
    print(f"Rate Limit Remaining: {response.headers.get('x-ratelimit-remaining')}")


# ============================================================================
# 9. BASE URL AND CLIENT CONFIGURATION
# ============================================================================

def client_configuration():
    """Configuring a client for a specific API - best practice for Gen AI apps"""
    print("\n" + "="*60)
    print("9. CLIENT CONFIGURATION")
    print("="*60)
    
    # Configure a client for a specific API
    client = httpx.Client(
        base_url='https://api.github.com',
        headers={
            'User-Agent': 'MyGenAIApp/1.0',
            'Accept': 'application/json'
        },
        timeout=30.0
    )
    
    # Now you can use relative URLs
    with client:
        response = client.get('/users/octocat')
        print(f"User: {response.json()['login']}")
        
        response = client.get('/users/torvalds')
        print(f"User: {response.json()['login']}")


# ============================================================================
# 10. PRACTICAL EXAMPLE: Mock LLM API Call
# ============================================================================

def mock_llm_api_call():
    """Simulating a typical LLM API call pattern"""
    print("\n" + "="*60)
    print("10. MOCK LLM API CALL")
    print("="*60)
    
    # This simulates the structure you'd use with OpenAI, Anthropic, etc.
    api_endpoint = "https://httpbin.org/post"
    
    headers = {
        # Never hardcode secrets in code. Use environment variables instead.
        # Example: export OPENAI_API_KEY='your-api-key-here'
        'Authorization': f"Bearer {os.getenv('OPENAI_API_KEY', 'your-api-key-here')}",
        'Content-Type': 'application/json'
    }
    
    payload = {
        'model': 'gpt-4',
        'messages': [
            {
                'role': 'system',
                'content': 'You are a helpful AI assistant.'
            },
            {
                'role': 'user',
                'content': 'Explain quantum computing in simple terms.'
            }
        ],
        'temperature': 0.7,
        'max_tokens': 500
    }
    
    try:
        with httpx.Client(timeout=60.0) as client:
            response = client.post(
                api_endpoint,
                headers=headers,
                json=payload
            )
            
            response.raise_for_status()
            
            print(f"Status: {response.status_code}")
            print(f"Request payload structure:")
            print(json.dumps(payload, indent=2))
            
    except httpx.HTTPStatusError as e:
        print(f"API Error: {e.response.status_code}")
        print(f"Error details: {e.response.text}")
    except httpx.TimeoutException:
        print("API request timed out")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*60)
    print("HTTPX BASICS FOR GEN AI DEVELOPERS")
    print("="*60)
    
    # Run all examples
    basic_get_request()
    basic_post_request()
    using_client_context()
    custom_headers()
    query_parameters()
    timeout_handling()
    error_handling()
    response_methods()
    client_configuration()
    mock_llm_api_call()
    
    print("\n" + "="*60)
    print("ALL EXAMPLES COMPLETED!")
    print("="*60)
