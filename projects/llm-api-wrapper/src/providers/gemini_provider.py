import os
from typing import Iterator, AsyncIterator, List
import asyncio
from google import genai
from google.genai import types
from ..core import LLMProvider
from ..models import LLMRequest, LLMResponse, LLMResponseChunk, TokenUsage, Role, Message

class GeminiProvider(LLMProvider):
    def __init__(self, api_key: str = None, model: str = "gemini-3-flash-preview"):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("Gemini API key is required")
        self.client = genai.Client(api_key=self.api_key)
        self.model = model

    def _convert_messages(self, messages: List[Message]):
        system_instruction = None
        contents = []
        
        for msg in messages:
            if msg.role == Role.SYSTEM:
                # System prompt usually comes first; if multiple, we concat or use last.
                # Gemini SDK expects a single string for system_instruction usually.
                if system_instruction:
                    system_instruction += "\n" + msg.content
                else:
                    system_instruction = msg.content
            elif msg.role == Role.USER:
                contents.append(types.Content(
                    role="user",
                    parts=[types.Part.from_text(text=msg.content)]
                ))
            elif msg.role == Role.ASSISTANT:
                contents.append(types.Content(
                    role="model",
                    parts=[types.Part.from_text(text=msg.content)]
                ))
                
        return system_instruction, contents

    def generate(self, request: LLMRequest) -> LLMResponse:
        system_instruction, contents = self._convert_messages(request.messages)
        
        # Mapping config
        config = types.GenerateContentConfig(
            temperature=request.temperature,
            max_output_tokens=request.max_tokens,
            stop_sequences=request.stop_sequences,
            candidate_count=1,
            system_instruction=system_instruction
        )

        response = self.client.models.generate_content(
            model=self.model,
            contents=contents,
            config=config
        )
        
        usage = TokenUsage(
             input_tokens=response.usage_metadata.prompt_token_count if response.usage_metadata else 0,
             output_tokens=response.usage_metadata.candidates_token_count if response.usage_metadata else 0,
             total_tokens=response.usage_metadata.total_token_count if response.usage_metadata else 0,
        )

        return LLMResponse(
            content=response.text,
            usage=usage,
            provider="gemini",
            model_name=self.model,
            raw_response=response
        )

    def stream(self, request: LLMRequest) -> Iterator[LLMResponseChunk]:
        system_instruction, contents = self._convert_messages(request.messages)
        
        config = types.GenerateContentConfig(
            temperature=request.temperature,
            max_output_tokens=request.max_tokens,
            stop_sequences=request.stop_sequences,
            candidate_count=1,
            system_instruction=system_instruction
        )

        for chunk in self.client.models.generate_content_stream(
            model=self.model,
            contents=contents,
            config=config
        ):
            usage = None
            if chunk.usage_metadata:
                usage = TokenUsage(
                    input_tokens=chunk.usage_metadata.prompt_token_count,
                    output_tokens=chunk.usage_metadata.candidates_token_count,
                    total_tokens=chunk.usage_metadata.total_token_count
                )
                
            if chunk.text or usage:
                yield LLMResponseChunk(
                    content_delta=chunk.text if chunk.text else "",
                    provider="gemini",
                    model_name=self.model,
                    usage=usage
                )

    async def generate_async(self, request: LLMRequest) -> LLMResponse:
        system_instruction, contents = self._convert_messages(request.messages)
        
        config = types.GenerateContentConfig(
            temperature=request.temperature,
            max_output_tokens=request.max_tokens,
            stop_sequences=request.stop_sequences,
            candidate_count=1,
            system_instruction=system_instruction
        )

        # Use client.aio for true async
        response = await self.client.aio.models.generate_content(
            model=self.model,
            contents=contents,
            config=config
        )
        
        usage = TokenUsage(
             input_tokens=response.usage_metadata.prompt_token_count if response.usage_metadata else 0,
             output_tokens=response.usage_metadata.candidates_token_count if response.usage_metadata else 0,
             total_tokens=response.usage_metadata.total_token_count if response.usage_metadata else 0,
        )

        return LLMResponse(
            content=response.text,
            usage=usage,
            provider="gemini",
            model_name=self.model,
            raw_response=response
        )

    async def stream_async(self, request: LLMRequest) -> AsyncIterator[LLMResponseChunk]:
        system_instruction, contents = self._convert_messages(request.messages)
        
        config = types.GenerateContentConfig(
            temperature=request.temperature,
            max_output_tokens=request.max_tokens,
            stop_sequences=request.stop_sequences,
            candidate_count=1,
            system_instruction=system_instruction
        )
        
        # Use client.aio for true async streaming
        async for chunk in await self.client.aio.models.generate_content_stream(
            model=self.model,
            contents=contents,
            config=config
        ):
            usage = None
            if chunk.usage_metadata:
                usage = TokenUsage(
                    input_tokens=chunk.usage_metadata.prompt_token_count,
                    output_tokens=chunk.usage_metadata.candidates_token_count,
                    total_tokens=chunk.usage_metadata.total_token_count
                )
                
            if chunk.text or usage:
                yield LLMResponseChunk(
                    content_delta=chunk.text if chunk.text else "",
                    provider="gemini",
                    model_name=self.model,
                    usage=usage
                )
