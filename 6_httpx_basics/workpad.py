"""
HTTPX Async Behavior Demonstration
===================================
This script demonstrates the key async behaviors of httpx:
1. Sequential vs Concurrent execution
2. Performance comparison
3. Error handling in async context
4. Practical patterns for API calls
"""

import httpx
import asyncio
import time
import json
import os
from typing import List, Dict, Any, AsyncIterator
from dotenv import load_dotenv

OPENAI_BASE_URL = "https://api.openai.com/v1"


load_dotenv()


class ChatSession:
    """Manage a chat session with conversation history"""
    
    def __init__(self, api_key: str, model: str = 'gpt-3.5-turbo'):
        if not api_key:
            raise RuntimeError(
                "Missing OPENAI_API_KEY. Set it in your environment or a local .env file."
            )
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
    
    chat = ChatSession(os.getenv("OPENAI_API_KEY"))
    chat.add_system_message("You are a helpful Python programming assistant.")
    
    # First message
    print("\nUser: What is httpx?")
    response1 = await chat.send_message("What is httpx?")
    print(f"AI: {response1}...")
    
    # Follow-up message (uses conversation history)
    print("\nUser: How is it different from requests?")
    response2 = await chat.send_message("How is it different from requests?")
    print(f"AI: {response2}...")
    
    print(f"\nTotal messages in history: {len(chat.messages)}")

asyncio.run(chat_session_example())