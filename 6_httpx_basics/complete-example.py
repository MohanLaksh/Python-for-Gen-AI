"""
Complete Gen AI Application Example
====================================
This file demonstrates a complete, production-ready Gen AI application
using httpx with all best practices:

- Async/await for performance
- Streaming for better UX
- Error handling and retries
- Rate limiting
- Conversation history
- Multiple LLM providers (OpenAI, Anthropic)

This is a template you can use for your own Gen AI projects!
"""

import httpx
import asyncio
import json
import os
from typing import AsyncIterator, List, Dict, Optional
from dataclasses import dataclass
from enum import Enum


# ============================================================================
# CONFIGURATION
# ============================================================================

class LLMProvider(Enum):
    """Supported LLM providers"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"


@dataclass
class LLMConfig:
    """Configuration for LLM API"""
    provider: LLMProvider
    api_key: str
    model: str
    base_url: str
    timeout: float = 60.0
    max_retries: int = 3


# Provider configurations
CONFIGS = {
    LLMProvider.OPENAI: LLMConfig(
        provider=LLMProvider.OPENAI,
        api_key=os.getenv('OPENAI_API_KEY', 'your-key-here'),
        model='gpt-4',
        base_url='https://api.openai.com/v1',
        timeout=60.0
    ),
    LLMProvider.ANTHROPIC: LLMConfig(
        provider=LLMProvider.ANTHROPIC,
        api_key=os.getenv('ANTHROPIC_API_KEY', 'your-key-here'),
        model='claude-3-opus-20240229',
        base_url='https://api.anthropic.com/v1',
        timeout=60.0
    )
}


# ============================================================================
# LLM CLIENT
# ============================================================================

class LLMClient:
    """
    Production-ready LLM client with:
    - Multiple provider support
    - Streaming and non-streaming
    - Automatic retries
    - Error handling
    - Rate limiting
    """
    
    def __init__(self, config: LLMConfig):
        self.config = config
        self.client = httpx.AsyncClient(
            base_url=config.base_url,
            timeout=httpx.Timeout(config.timeout, read=120.0),
            limits=httpx.Limits(
                max_keepalive_connections=5,
                max_connections=10
            )
        )
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
    
    def _get_headers(self) -> Dict[str, str]:
        """Get headers for the provider"""
        if self.config.provider == LLMProvider.OPENAI:
            return {
                'Authorization': f'Bearer {self.config.api_key}',
                'Content-Type': 'application/json'
            }
        elif self.config.provider == LLMProvider.ANTHROPIC:
            return {
                'x-api-key': self.config.api_key,
                'anthropic-version': '2023-06-01',
                'Content-Type': 'application/json'
            }
    
    def _format_messages(self, messages: List[Dict]) -> Dict:
        """Format messages for the provider"""
        if self.config.provider == LLMProvider.OPENAI:
            return {
                'model': self.config.model,
                'messages': messages
            }
        elif self.config.provider == LLMProvider.ANTHROPIC:
            # Anthropic has different format
            system_msg = next((m['content'] for m in messages if m['role'] == 'system'), None)
            user_messages = [m for m in messages if m['role'] != 'system']
            
            payload = {
                'model': self.config.model,
                'messages': user_messages,
                'max_tokens': 1024
            }
            
            if system_msg:
                payload['system'] = system_msg
            
            return payload
    
    async def complete(
        self,
        messages: List[Dict],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Get a completion (non-streaming)
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens to generate
        
        Returns:
            The completion text
        """
        payload = self._format_messages(messages)
        payload['temperature'] = temperature
        
        if max_tokens:
            payload['max_tokens'] = max_tokens
        
        for attempt in range(self.config.max_retries):
            try:
                response = await self.client.post(
                    '/chat/completions' if self.config.provider == LLMProvider.OPENAI else '/messages',
                    headers=self._get_headers(),
                    json=payload
                )
                
                response.raise_for_status()
                result = response.json()
                
                # Extract content based on provider
                if self.config.provider == LLMProvider.OPENAI:
                    return result['choices'][0]['message']['content']
                elif self.config.provider == LLMProvider.ANTHROPIC:
                    return result['content'][0]['text']
                
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 429:  # Rate limit
                    wait_time = 2 ** attempt
                    print(f"Rate limited. Waiting {wait_time}s...")
                    await asyncio.sleep(wait_time)
                else:
                    raise
                    
            except httpx.TimeoutException:
                if attempt == self.config.max_retries - 1:
                    raise
                print(f"Timeout on attempt {attempt + 1}. Retrying...")
                await asyncio.sleep(1)
        
        raise Exception("Max retries exceeded")
    
    async def stream_complete(
        self,
        messages: List[Dict],
        temperature: float = 0.7
    ) -> AsyncIterator[str]:
        """
        Stream a completion
        
        Args:
            messages: List of message dicts
            temperature: Sampling temperature
        
        Yields:
            Content chunks as they arrive
        """
        payload = self._format_messages(messages)
        payload['temperature'] = temperature
        payload['stream'] = True
        
        async with self.client.stream(
            'POST',
            '/chat/completions' if self.config.provider == LLMProvider.OPENAI else '/messages',
            headers=self._get_headers(),
            json=payload
        ) as response:
            response.raise_for_status()
            
            if self.config.provider == LLMProvider.OPENAI:
                # OpenAI SSE format
                async for line in response.aiter_lines():
                    if line.startswith('data: '):
                        data_str = line[6:]
                        
                        if data_str == '[DONE]':
                            break
                        
                        try:
                            data = json.loads(data_str)
                            content = data['choices'][0]['delta'].get('content', '')
                            if content:
                                yield content
                        except json.JSONDecodeError:
                            continue
            
            elif self.config.provider == LLMProvider.ANTHROPIC:
                # Anthropic SSE format
                async for line in response.aiter_lines():
                    if line.startswith('data: '):
                        data_str = line[6:]
                        
                        try:
                            data = json.loads(data_str)
                            if data['type'] == 'content_block_delta':
                                content = data['delta'].get('text', '')
                                if content:
                                    yield content
                        except json.JSONDecodeError:
                            continue


# ============================================================================
# CHAT SESSION
# ============================================================================

class ChatSession:
    """
    Manage a chat session with conversation history
    """
    
    def __init__(self, client: LLMClient, system_prompt: Optional[str] = None):
        self.client = client
        self.messages: List[Dict] = []
        
        if system_prompt:
            self.messages.append({
                'role': 'system',
                'content': system_prompt
            })
    
    async def send_message(self, content: str) -> str:
        """Send a message and get response"""
        self.messages.append({
            'role': 'user',
            'content': content
        })
        
        response = await self.client.complete(self.messages)
        
        self.messages.append({
            'role': 'assistant',
            'content': response
        })
        
        return response
    
    async def stream_message(self, content: str) -> AsyncIterator[str]:
        """Send a message and stream response"""
        self.messages.append({
            'role': 'user',
            'content': content
        })
        
        full_response = ""
        
        async for chunk in self.client.stream_complete(self.messages):
            full_response += chunk
            yield chunk
        
        self.messages.append({
            'role': 'assistant',
            'content': full_response
        })
    
    def get_history(self) -> List[Dict]:
        """Get conversation history"""
        return self.messages.copy()
    
    def clear_history(self, keep_system: bool = True):
        """Clear conversation history"""
        if keep_system and self.messages and self.messages[0]['role'] == 'system':
            self.messages = [self.messages[0]]
        else:
            self.messages = []


# ============================================================================
# BATCH PROCESSOR
# ============================================================================

class BatchProcessor:
    """
    Process multiple prompts concurrently with rate limiting
    """
    
    def __init__(self, client: LLMClient, batch_size: int = 5):
        self.client = client
        self.batch_size = batch_size
    
    async def process(
        self,
        prompts: List[str],
        system_prompt: Optional[str] = None
    ) -> List[str]:
        """
        Process multiple prompts concurrently
        
        Args:
            prompts: List of user prompts
            system_prompt: Optional system prompt for all requests
        
        Returns:
            List of responses
        """
        results = []
        
        for i in range(0, len(prompts), self.batch_size):
            batch = prompts[i:i + self.batch_size]
            
            # Create messages for each prompt
            messages_list = []
            for prompt in batch:
                messages = []
                if system_prompt:
                    messages.append({'role': 'system', 'content': system_prompt})
                messages.append({'role': 'user', 'content': prompt})
                messages_list.append(messages)
            
            # Process batch concurrently
            batch_results = await asyncio.gather(*[
                self.client.complete(messages)
                for messages in messages_list
            ])
            
            results.extend(batch_results)
            
            # Rate limiting between batches
            if i + self.batch_size < len(prompts):
                await asyncio.sleep(1)
        
        return results


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

async def example_basic_chat():
    """Example: Basic chat completion"""
    print("\n" + "="*60)
    print("EXAMPLE 1: Basic Chat")
    print("="*60)
    
    config = CONFIGS[LLMProvider.OPENAI]
    
    async with LLMClient(config) as client:
        messages = [
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'user', 'content': 'What is httpx?'}
        ]
        
        response = await client.complete(messages)
        print(f"\nAI: {response}")


async def example_streaming_chat():
    """Example: Streaming chat"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Streaming Chat")
    print("="*60)
    
    config = CONFIGS[LLMProvider.OPENAI]
    
    async with LLMClient(config) as client:
        messages = [
            {'role': 'user', 'content': 'Write a haiku about Python programming.'}
        ]
        
        print("\nAI: ", end="", flush=True)
        async for chunk in client.stream_complete(messages):
            print(chunk, end="", flush=True)
        print()


async def example_chat_session():
    """Example: Chat session with history"""
    print("\n" + "="*60)
    print("EXAMPLE 3: Chat Session with History")
    print("="*60)
    
    config = CONFIGS[LLMProvider.OPENAI]
    
    async with LLMClient(config) as client:
        session = ChatSession(
            client,
            system_prompt="You are a Python programming expert."
        )
        
        # First message
        print("\nUser: What is httpx?")
        response1 = await session.send_message("What is httpx?")
        print(f"AI: {response1[:100]}...")
        
        # Follow-up (uses history)
        print("\nUser: How is it different from requests?")
        response2 = await session.send_message("How is it different from requests?")
        print(f"AI: {response2[:100]}...")
        
        print(f"\nTotal messages in history: {len(session.get_history())}")


async def example_batch_processing():
    """Example: Batch processing"""
    print("\n" + "="*60)
    print("EXAMPLE 4: Batch Processing")
    print("="*60)
    
    config = CONFIGS[LLMProvider.OPENAI]
    
    async with LLMClient(config) as client:
        processor = BatchProcessor(client, batch_size=3)
        
        prompts = [
            "What is machine learning?",
            "What is deep learning?",
            "What is a neural network?",
            "What is NLP?",
            "What is computer vision?"
        ]
        
        print(f"\nProcessing {len(prompts)} prompts...")
        results = await processor.process(
            prompts,
            system_prompt="Answer in one sentence."
        )
        
        for i, (prompt, result) in enumerate(zip(prompts, results), 1):
            print(f"\n{i}. {prompt}")
            print(f"   → {result}")


async def example_streaming_session():
    """Example: Streaming in a session"""
    print("\n" + "="*60)
    print("EXAMPLE 5: Streaming Session")
    print("="*60)
    
    config = CONFIGS[LLMProvider.OPENAI]
    
    async with LLMClient(config) as client:
        session = ChatSession(client, system_prompt="You are a helpful assistant.")
        
        print("\nUser: Tell me about async programming in Python")
        print("AI: ", end="", flush=True)
        
        async for chunk in session.stream_message("Tell me about async programming in Python"):
            print(chunk, end="", flush=True)
        
        print()


# ============================================================================
# MAIN
# ============================================================================

async def main():
    """Run all examples"""
    print("\n" + "="*60)
    print("COMPLETE GEN AI APPLICATION EXAMPLES")
    print("="*60)
    
    # Check API key
    if CONFIGS[LLMProvider.OPENAI].api_key == 'your-key-here':
        print("\n⚠️  WARNING: Set your OPENAI_API_KEY environment variable")
        print("These examples require a valid API key.\n")
        print("Example usage patterns are shown below:")
        print("(They won't actually run without an API key)\n")
    
    try:
        await example_basic_chat()
        await example_streaming_chat()
        await example_chat_session()
        await example_batch_processing()
        await example_streaming_session()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure you have set your API key:")
        print("export OPENAI_API_KEY='your-key-here'")
    
    print("\n" + "="*60)
    print("EXAMPLES COMPLETED!")
    print("="*60)


if __name__ == "__main__":
    asyncio.run(main())
