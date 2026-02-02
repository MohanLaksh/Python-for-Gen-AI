import os
from typing import Iterator, AsyncIterator, List
import openai
from openai import OpenAI, AsyncOpenAI
from ..core import LLMProvider
from ..models import LLMRequest, LLMResponse, LLMResponseChunk, TokenUsage, Role, Message

class OpenAIProvider(LLMProvider):
    def __init__(self, api_key: str = None, model: str = "gpt-3.5-turbo"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
        self.client = OpenAI(api_key=self.api_key)
        self.async_client = AsyncOpenAI(api_key=self.api_key)
        self.model = model

    def _convert_messages(self, messages: List[Message]) -> List[dict]:
        return [{"role": msg.role.value, "content": msg.content} for msg in messages]

    def _convert_usage(self, usage) -> TokenUsage:
        return TokenUsage(
            input_tokens=usage.prompt_tokens,
            output_tokens=usage.completion_tokens,
            total_tokens=usage.total_tokens
        )

    def generate(self, request: LLMRequest) -> LLMResponse:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self._convert_messages(request.messages),
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            stop=request.stop_sequences,
            stream=False
        )
        
        return LLMResponse(
            content=response.choices[0].message.content,
            usage=self._convert_usage(response.usage),
            provider="openai",
            model_name=self.model,
            raw_response=response
        )

    def stream(self, request: LLMRequest) -> Iterator[LLMResponseChunk]:
        stream = self.client.chat.completions.create(
            model=self.model,
            messages=self._convert_messages(request.messages),
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            stop=request.stop_sequences,
            stream=True,
            stream_options={"include_usage": True}
        )

        for chunk in stream:
            usage = None
            if chunk.usage:
                usage = self._convert_usage(chunk.usage)
            
            content = chunk.choices[0].delta.content if chunk.choices and chunk.choices[0].delta.content else ""
            
            if content or usage:
                yield LLMResponseChunk(
                    content_delta=content,
                    provider="openai",
                    model_name=self.model,
                    usage=usage
                )

    async def generate_async(self, request: LLMRequest) -> LLMResponse:
        response = await self.async_client.chat.completions.create(
            model=self.model,
            messages=self._convert_messages(request.messages),
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            stop=request.stop_sequences,
            stream=False
        )
        
        return LLMResponse(
            content=response.choices[0].message.content,
            usage=self._convert_usage(response.usage),
            provider="openai",
            model_name=self.model,
            raw_response=response
        )

    async def stream_async(self, request: LLMRequest) -> AsyncIterator[LLMResponseChunk]:
        stream = await self.async_client.chat.completions.create(
            model=self.model,
            messages=self._convert_messages(request.messages),
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            stop=request.stop_sequences,
            stream=True,
            stream_options={"include_usage": True}
        )

        async for chunk in stream:
            usage = None
            if chunk.usage:
                usage = self._convert_usage(chunk.usage)
                
            content = chunk.choices[0].delta.content if chunk.choices and chunk.choices[0].delta.content else ""
            
            if content or usage:
                yield LLMResponseChunk(
                    content_delta=content,
                    provider="openai",
                    model_name=self.model,
                    usage=usage
                )
