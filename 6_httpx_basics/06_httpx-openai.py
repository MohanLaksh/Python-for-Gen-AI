"""
HTTPX with OpenAI API - Practical Examples
==========================================
Real-world examples of using httpx with OpenAI's API.

Note: You'll need an OpenAI API key. Set it as an environment variable:
export OPENAI_API_KEY='your-api-key-here'

Or use a .env file with python-dotenv
"""

import httpx
import asyncio
import json
import os
from typing import AsyncIterator, Dict, Any, List


# ============================================================================
# CONFIGURATION
# ============================================================================

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'your-api-key-here')
OPENAI_BASE_URL = 'https://api.openai.com/v1'


# ============================================================================
# 1. BASIC CHAT COMPLETION (Non-Streaming)
# ============================================================================

async def basic_chat_completion():
    """Simple chat completion request"""
    print("\n" + "="*60)
    print("1. BASIC CHAT COMPLETION")
    print("="*60)
    
    headers = {
        'Authorization': f'Bearer {OPENAI_API_KEY}',
        'Content-Type': 'application/json'
    }
    
    payload = {
        'model': 'gpt-3.5-turbo',
        'messages': [
            {
                'role': 'system',
                'content': 'You are a helpful AI assistant.'
            },
            {
                'role': 'user',
                'content': 'Explain what httpx is in one sentence.'
            }
        ],
        'temperature': 0.7,
        'max_tokens': 100
    }
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(
                f'{OPENAI_BASE_URL}/chat/completions',
                headers=headers,
                json=payload
            )
            
            response.raise_for_status()
            result = response.json()
            
            print(f"Model: {result['model']}")
            print(f"Response: {result['choices'][0]['message']['content']}")
            print(f"Tokens used: {result['usage']['total_tokens']}")
            
        except httpx.HTTPStatusError as e:
            print(f"API Error: {e.response.status_code}")
            print(f"Details: {e.response.text}")


# ============================================================================
# 2. STREAMING CHAT COMPLETION
# ============================================================================

async def streaming_chat_completion():
    """Streaming chat completion - see responses as they're generated"""
    print("\n" + "="*60)
    print("2. STREAMING CHAT COMPLETION")
    print("="*60)
    
    headers = {
        'Authorization': f'Bearer {OPENAI_API_KEY}',
        'Content-Type': 'application/json'
    }
    
    payload = {
        'model': 'gpt-3.5-turbo',
        'messages': [
            {
                'role': 'user',
                'content': 'Write a haiku about artificial intelligence.'
            }
        ],
        'stream': True  # Enable streaming!
    }
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            async with client.stream(
                'POST',
                f'{OPENAI_BASE_URL}/chat/completions',
                headers=headers,
                json=payload
            ) as response:
                response.raise_for_status()
                
                print("AI: ", end="", flush=True)
                
                async for line in response.aiter_lines():
                    if line.startswith('data: '):
                        data_str = line[6:]  # Remove 'data: ' prefix
                        
                        if data_str == '[DONE]':
                            break
                        
                        try:
                            data = json.loads(data_str)
                            content = data['choices'][0]['delta'].get('content', '')
                            if content:
                                print(content, end="", flush=True)
                        except json.JSONDecodeError:
                            continue
                
                print()  # New line
                
        except httpx.HTTPStatusError as e:
            print(f"API Error: {e.response.status_code}")
            print(f"Details: {e.response.text}")


# ============================================================================
# 3. MULTIPLE CONCURRENT COMPLETIONS
# ============================================================================

async def concurrent_completions():
    """Make multiple API calls concurrently"""
    print("\n" + "="*60)
    print("3. CONCURRENT COMPLETIONS")
    print("="*60)
    
    headers = {
        'Authorization': f'Bearer {OPENAI_API_KEY}',
        'Content-Type': 'application/json'
    }
    
    prompts = [
        "What is machine learning?",
        "What is deep learning?",
        "What is neural network?"
    ]
    
    async def get_completion(client: httpx.AsyncClient, prompt: str) -> Dict:
        """Get a single completion"""
        payload = {
            'model': 'gpt-3.5-turbo',
            'messages': [{'role': 'user', 'content': prompt}],
            'max_tokens': 50
        }
        
        response = await client.post(
            f'{OPENAI_BASE_URL}/chat/completions',
            headers=headers,
            json=payload
        )
        
        result = response.json()
        return {
            'prompt': prompt,
            'response': result['choices'][0]['message']['content'],
            'tokens': result['usage']['total_tokens']
        }
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        tasks = [get_completion(client, prompt) for prompt in prompts]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for i, result in enumerate(results, 1):
            if isinstance(result, Exception):
                print(f"\n{i}. Error: {result}")
            else:
                print(f"\n{i}. Prompt: {result['prompt']}")
                print(f"   Response: {result['response'][:100]}...")
                print(f"   Tokens: {result['tokens']}")


# ============================================================================
# 4. CHAT WITH CONVERSATION HISTORY
# ============================================================================

class ChatSession:
    """Manage a chat session with conversation history"""
    
    def __init__(self, api_key: str, model: str = 'gpt-3.5-turbo'):
        self.api_key = api_key
        self.model = model
        self.messages: List[Dict[str, str]] = []
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
    
    def add_system_message(self, content: str):
        """Add a system message"""
        self.messages.append({'role': 'system', 'content': content})
    
    async def send_message(self, content: str) -> str:
        """Send a message and get response"""
        # Add user message to history
        self.messages.append({'role': 'user', 'content': content})
        
        payload = {
            'model': self.model,
            'messages': self.messages,
            'temperature': 0.7
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f'{OPENAI_BASE_URL}/chat/completions',
                headers=self.headers,
                json=payload
            )
            
            response.raise_for_status()
            result = response.json()
            
            # Add assistant response to history
            assistant_message = result['choices'][0]['message']['content']
            self.messages.append({'role': 'assistant', 'content': assistant_message})
            
            return assistant_message
    
    async def stream_message(self, content: str) -> AsyncIterator[str]:
        """Send a message and stream the response"""
        self.messages.append({'role': 'user', 'content': content})
        
        payload = {
            'model': self.model,
            'messages': self.messages,
            'stream': True
        }
        
        full_response = ""
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            async with client.stream(
                'POST',
                f'{OPENAI_BASE_URL}/chat/completions',
                headers=self.headers,
                json=payload
            ) as response:
                response.raise_for_status()
                
                async for line in response.aiter_lines():
                    if line.startswith('data: '):
                        data_str = line[6:]
                        
                        if data_str == '[DONE]':
                            break
                        
                        try:
                            data = json.loads(data_str)
                            content_chunk = data['choices'][0]['delta'].get('content', '')
                            if content_chunk:
                                full_response += content_chunk
                                yield content_chunk
                        except json.JSONDecodeError:
                            continue
        
        # Add complete response to history
        self.messages.append({'role': 'assistant', 'content': full_response})


async def chat_session_example():
    """Example of using ChatSession"""
    print("\n" + "="*60)
    print("4. CHAT SESSION WITH HISTORY")
    print("="*60)
    
    chat = ChatSession(OPENAI_API_KEY)
    chat.add_system_message("You are a helpful Python programming assistant.")
    
    # First message
    print("\nUser: What is httpx?")
    response1 = await chat.send_message("What is httpx?")
    print(f"AI: {response1[:150]}...")
    
    # Follow-up message (uses conversation history)
    print("\nUser: How is it different from requests?")
    response2 = await chat.send_message("How is it different from requests?")
    print(f"AI: {response2[:150]}...")
    
    print(f"\nTotal messages in history: {len(chat.messages)}")


# ============================================================================
# 5. FUNCTION CALLING
# ============================================================================

async def function_calling_example():
    """Example of OpenAI function calling"""
    print("\n" + "="*60)
    print("5. FUNCTION CALLING")
    print("="*60)
    
    headers = {
        'Authorization': f'Bearer {OPENAI_API_KEY}',
        'Content-Type': 'application/json'
    }
    
    # Define available functions
    functions = [
        {
            "name": "get_weather",
            "description": "Get the current weather for a location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"]
                    }
                },
                "required": ["location"]
            }
        }
    ]
    
    payload = {
        'model': 'gpt-3.5-turbo',
        'messages': [
            {'role': 'user', 'content': 'What is the weather in San Francisco?'}
        ],
        'functions': functions,
        'function_call': 'auto'
    }
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            f'{OPENAI_BASE_URL}/chat/completions',
            headers=headers,
            json=payload
        )
        
        result = response.json()
        message = result['choices'][0]['message']
        
        if 'function_call' in message:
            function_name = message['function_call']['name']
            function_args = json.loads(message['function_call']['arguments'])
            
            print(f"Function called: {function_name}")
            print(f"Arguments: {json.dumps(function_args, indent=2)}")


# ============================================================================
# 6. EMBEDDINGS
# ============================================================================

async def create_embeddings():
    """Create embeddings for text"""
    print("\n" + "="*60)
    print("6. CREATE EMBEDDINGS")
    print("="*60)
    
    headers = {
        'Authorization': f'Bearer {OPENAI_API_KEY}',
        'Content-Type': 'application/json'
    }
    
    texts = [
        "Machine learning is a subset of AI",
        "Deep learning uses neural networks",
        "Python is great for data science"
    ]
    
    payload = {
        'model': 'text-embedding-ada-002',
        'input': texts
    }
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            f'{OPENAI_BASE_URL}/embeddings',
            headers=headers,
            json=payload
        )
        
        result = response.json()
        
        print(f"Model: {result['model']}")
        print(f"Number of embeddings: {len(result['data'])}")
        print(f"Embedding dimension: {len(result['data'][0]['embedding'])}")
        print(f"Total tokens: {result['usage']['total_tokens']}")


# ============================================================================
# 7. ERROR HANDLING AND RETRIES
# ============================================================================

async def api_call_with_retry(max_retries: int = 3):
    """API call with retry logic"""
    print("\n" + "="*60)
    print("7. API CALL WITH RETRY")
    print("="*60)
    
    headers = {
        'Authorization': f'Bearer {OPENAI_API_KEY}',
        'Content-Type': 'application/json'
    }
    
    payload = {
        'model': 'gpt-3.5-turbo',
        'messages': [{'role': 'user', 'content': 'Hello!'}]
    }
    
    for attempt in range(max_retries):
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f'{OPENAI_BASE_URL}/chat/completions',
                    headers=headers,
                    json=payload
                )
                
                response.raise_for_status()
                result = response.json()
                
                print(f"Success on attempt {attempt + 1}")
                print(f"Response: {result['choices'][0]['message']['content']}")
                return result
                
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:  # Rate limit
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Rate limited. Waiting {wait_time}s...")
                await asyncio.sleep(wait_time)
            else:
                print(f"HTTP Error: {e.response.status_code}")
                raise
                
        except httpx.TimeoutException:
            print(f"Timeout on attempt {attempt + 1}")
            if attempt == max_retries - 1:
                raise


# ============================================================================
# MAIN EXECUTION
# ============================================================================

async def main():
    """Run all examples"""
    print("\n" + "="*60)
    print("HTTPX WITH OPENAI API")
    print("="*60)
    
    if OPENAI_API_KEY == 'your-api-key-here':
        print("\n⚠️  WARNING: Please set your OPENAI_API_KEY environment variable")
        print("These examples will fail without a valid API key.\n")
        return
    
    await basic_chat_completion()
    await streaming_chat_completion()
    await concurrent_completions()
    await chat_session_example()
    await function_calling_example()
    await create_embeddings()
    await api_call_with_retry()
    
    print("\n" + "="*60)
    print("ALL EXAMPLES COMPLETED!")
    print("="*60)


if __name__ == "__main__":
    asyncio.run(main())
