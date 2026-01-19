"""
HTTPX Streaming for Gen AI Developers
======================================
Streaming is CRITICAL for Gen AI applications because:
1. LLM responses can be very long
2. Users want to see responses as they're generated (better UX)
3. Reduces perceived latency
4. Allows processing data as it arrives

This is how ChatGPT, Claude, and other AI chatbots show responses word-by-word!
"""

import httpx
import asyncio
import json
import time
from typing import AsyncIterator, Iterator


# ============================================================================
# 1. BASIC STREAMING (Sync)
# ============================================================================

def basic_streaming():
    """Simple synchronous streaming example"""
    print("\n" + "="*60)
    print("1. BASIC STREAMING (SYNC)")
    print("="*60)
    
    with httpx.Client() as client:
        with client.stream('GET', 'https://httpbin.org/stream/10') as response:
            print(f"Status: {response.status_code}")
            print("Streaming chunks:\n")
            
            for line in response.iter_lines():
                if line:
                    data = json.loads(line)
                    print(f"  Chunk {data['id']}: {data['url']}")


# ============================================================================
# 2. STREAMING BYTES
# ============================================================================

def streaming_bytes():
    """Stream response as raw bytes - useful for large files"""
    print("\n" + "="*60)
    print("2. STREAMING BYTES")
    print("="*60)
    
    with httpx.Client() as client:
        with client.stream('GET', 'https://httpbin.org/bytes/1024') as response:
            print(f"Status: {response.status_code}")
            print(f"Content-Length: {response.headers.get('content-length')}")
            
            total_bytes = 0
            for chunk in response.iter_bytes(chunk_size=256):
                total_bytes += len(chunk)
                print(f"  Received {len(chunk)} bytes (total: {total_bytes})")


# ============================================================================
# 3. ASYNC STREAMING (Most Important for Gen AI!)
# ============================================================================

async def async_streaming():
    """Async streaming - the pattern used by LLM APIs"""
    print("\n" + "="*60)
    print("3. ASYNC STREAMING")
    print("="*60)
    
    async with httpx.AsyncClient() as client:
        async with client.stream('GET', 'https://httpbin.org/stream/5') as response:
            print(f"Status: {response.status_code}")
            print("Streaming asynchronously:\n")
            
            async for line in response.aiter_lines():
                if line:
                    data = json.loads(line)
                    print(f"  Chunk {data['id']}: Received at {time.time():.2f}")


# ============================================================================
# 4. STREAMING WITH TIMEOUT
# ============================================================================

async def streaming_with_timeout():
    """Streaming with proper timeout handling"""
    print("\n" + "="*60)
    print("4. STREAMING WITH TIMEOUT")
    print("="*60)
    
    timeout = httpx.Timeout(
        connect=5.0,
        read=30.0,    # Important: longer timeout for streaming
        write=5.0,
        pool=5.0
    )
    
    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            async with client.stream('GET', 'https://httpbin.org/stream/3') as response:
                print(f"Status: {response.status_code}")
                
                async for line in response.aiter_lines():
                    if line:
                        print(f"  Received: {line[:50]}...")
                        
        except httpx.TimeoutException:
            print("Stream timed out!")


# ============================================================================
# 5. MOCK OPENAI STREAMING PATTERN
# ============================================================================

async def mock_openai_streaming():
    """
    Simulating OpenAI's streaming response pattern.
    Real OpenAI streaming sends Server-Sent Events (SSE) format.
    """
    print("\n" + "="*60)
    print("5. MOCK OPENAI STREAMING PATTERN")
    print("="*60)
    
    # This simulates how you'd structure an OpenAI streaming call
    async def stream_openai_response():
        """Simulate streaming LLM response"""
        # In real OpenAI API, you'd use:
        # async with client.stream('POST', 'https://api.openai.com/v1/chat/completions', ...)
        
        # Simulated response chunks (like OpenAI's format)
        chunks = [
            {"choices": [{"delta": {"content": "Hello"}}]},
            {"choices": [{"delta": {"content": " there"}}]},
            {"choices": [{"delta": {"content": "!"}}]},
            {"choices": [{"delta": {"content": " How"}}]},
            {"choices": [{"delta": {"content": " can"}}]},
            {"choices": [{"delta": {"content": " I"}}]},
            {"choices": [{"delta": {"content": " help"}}]},
            {"choices": [{"delta": {"content": " you"}}]},
            {"choices": [{"delta": {"content": "?"}}]},
        ]
        
        print("Streaming LLM response:")
        print("AI: ", end="", flush=True)
        
        for chunk in chunks:
            content = chunk["choices"][0]["delta"].get("content", "")
            print(content, end="", flush=True)
            await asyncio.sleep(0.1)  # Simulate network delay
        
        print()  # New line
    
    await stream_openai_response()


# ============================================================================
# 6. REAL OPENAI STREAMING EXAMPLE (Template)
# ============================================================================

async def real_openai_streaming_template():
    """
    Template for actual OpenAI API streaming.
    You'll need to install openai library and have an API key.
    """
    print("\n" + "="*60)
    print("6. REAL OPENAI STREAMING TEMPLATE")
    print("="*60)
    
    print("""
# Real OpenAI Streaming Code (requires: pip install openai)

import openai
import os

async def stream_openai():
    client = openai.AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    stream = await client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": "Write a short poem about AI"}
        ],
        stream=True
    )
    
    print("AI: ", end="", flush=True)
    async for chunk in stream:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
    print()

# Run it:
# asyncio.run(stream_openai())
    """)


# ============================================================================
# 7. HTTPX STREAMING WITH SSE (Server-Sent Events)
# ============================================================================

async def streaming_sse_pattern():
    """
    Server-Sent Events pattern - used by OpenAI, Anthropic, etc.
    """
    print("\n" + "="*60)
    print("7. STREAMING SSE PATTERN")
    print("="*60)
    
    # Simulating SSE format parsing
    def parse_sse_line(line: str) -> dict:
        """Parse a Server-Sent Event line"""
        if line.startswith('data: '):
            data_str = line[6:]  # Remove 'data: ' prefix
            if data_str == '[DONE]':
                return {'done': True}
            try:
                return json.loads(data_str)
            except json.JSONDecodeError:
                return {}
        return {}
    
    # Simulated SSE stream
    sse_lines = [
        'data: {"content": "The"}',
        'data: {"content": " future"}',
        'data: {"content": " of"}',
        'data: {"content": " AI"}',
        'data: {"content": " is"}',
        'data: {"content": " bright"}',
        'data: [DONE]',
    ]
    
    print("Parsing SSE stream:")
    print("Response: ", end="", flush=True)
    
    for line in sse_lines:
        data = parse_sse_line(line)
        if data.get('done'):
            break
        if 'content' in data:
            print(data['content'], end="", flush=True)
            await asyncio.sleep(0.1)
    
    print()


# ============================================================================
# 8. STREAMING POST REQUEST
# ============================================================================

async def streaming_post_request():
    """Streaming response from a POST request"""
    print("\n" + "="*60)
    print("8. STREAMING POST REQUEST")
    print("="*60)
    
    payload = {
        "model": "gpt-4",
        "messages": [{"role": "user", "content": "Hello!"}],
        "stream": True  # Enable streaming
    }
    
    async with httpx.AsyncClient() as client:
        # Using httpbin to demonstrate (won't actually stream, but shows pattern)
        async with client.stream(
            'POST',
            'https://httpbin.org/post',
            json=payload,
            timeout=30.0
        ) as response:
            print(f"Status: {response.status_code}")
            print(f"Headers: {dict(response.headers)}")
            
            # In real LLM API, you'd process chunks here
            content = await response.aread()
            print(f"Response size: {len(content)} bytes")


# ============================================================================
# 9. ADVANCED: Custom Streaming Iterator
# ============================================================================

class StreamingLLMResponse:
    """Custom class to handle streaming LLM responses"""
    
    def __init__(self, response: httpx.Response):
        self.response = response
        self.full_text = ""
    
    async def stream_content(self) -> AsyncIterator[str]:
        """Stream content chunks and accumulate full text"""
        async for line in self.response.aiter_lines():
            if line.startswith('data: '):
                data_str = line[6:]
                
                if data_str == '[DONE]':
                    break
                
                try:
                    data = json.loads(data_str)
                    content = data.get('choices', [{}])[0].get('delta', {}).get('content', '')
                    
                    if content:
                        self.full_text += content
                        yield content
                        
                except json.JSONDecodeError:
                    continue
    
    def get_full_text(self) -> str:
        """Get the complete accumulated text"""
        return self.full_text


async def custom_streaming_iterator():
    """Using a custom streaming iterator"""
    print("\n" + "="*60)
    print("9. CUSTOM STREAMING ITERATOR")
    print("="*60)
    
    # Simulated usage
    print("This demonstrates the pattern for a custom streaming handler.")
    print("In production, you'd use this with actual LLM API responses.")


# ============================================================================
# 10. PRACTICAL EXAMPLE: Streaming Multiple Responses
# ============================================================================

async def stream_multiple_responses():
    """Stream multiple LLM responses concurrently"""
    print("\n" + "="*60)
    print("10. STREAMING MULTIPLE RESPONSES")
    print("="*60)
    
    async def stream_single_response(prompt: str, response_id: int):
        """Stream a single response"""
        print(f"\n[Response {response_id}] Prompt: {prompt}")
        print(f"[Response {response_id}] AI: ", end="", flush=True)
        
        # Simulate streaming
        words = ["This", "is", "a", "simulated", "streaming", "response"]
        for word in words:
            print(word, end=" ", flush=True)
            await asyncio.sleep(0.2)
        print()
    
    # Stream multiple responses concurrently
    prompts = [
        "Explain machine learning",
        "What is deep learning?",
        "Describe neural networks"
    ]
    
    tasks = [
        stream_single_response(prompt, i)
        for i, prompt in enumerate(prompts, 1)
    ]
    
    await asyncio.gather(*tasks)


# ============================================================================
# 11. ERROR HANDLING IN STREAMING
# ============================================================================

async def streaming_error_handling():
    """Proper error handling for streaming responses"""
    print("\n" + "="*60)
    print("11. STREAMING ERROR HANDLING")
    print("="*60)
    
    async with httpx.AsyncClient() as client:
        try:
            async with client.stream(
                'GET',
                'https://httpbin.org/stream/3',
                timeout=30.0
            ) as response:
                response.raise_for_status()
                
                async for line in response.aiter_lines():
                    if line:
                        try:
                            data = json.loads(line)
                            print(f"  Chunk: {data['id']}")
                        except json.JSONDecodeError as e:
                            print(f"  Error parsing chunk: {e}")
                            continue
                            
        except httpx.HTTPStatusError as e:
            print(f"HTTP Error: {e.response.status_code}")
        except httpx.TimeoutException:
            print("Stream timed out")
        except Exception as e:
            print(f"Unexpected error: {e}")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

async def main():
    """Run all streaming examples"""
    print("\n" + "="*60)
    print("HTTPX STREAMING FOR GEN AI DEVELOPERS")
    print("="*60)
    
    basic_streaming()
    streaming_bytes()
    await async_streaming()
    await streaming_with_timeout()
    await mock_openai_streaming()
    await real_openai_streaming_template()
    await streaming_sse_pattern()
    await streaming_post_request()
    await custom_streaming_iterator()
    await stream_multiple_responses()
    await streaming_error_handling()
    
    print("\n" + "="*60)
    print("ALL STREAMING EXAMPLES COMPLETED!")
    print("="*60)


if __name__ == "__main__":
    asyncio.run(main())
