import os
from typing import Iterator, AsyncIterator, List
import anthropic
from anthropic import Anthropic, AsyncAnthropic
from ..core import LLMProvider
from ..models import LLMRequest, LLMResponse, LLMResponseChunk, TokenUsage, Role, Message

class AnthropicProvider(LLMProvider):
    def __init__(self, api_key: str = None, model: str = "claude-sonnet-4-5"):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("Anthropic API key is required")
        self.client = Anthropic(api_key=self.api_key)
        self.async_client = AsyncAnthropic(api_key=self.api_key)
        self.model = model

    def _convert_messages(self, messages: List[Message]) -> List[dict]:
        # Anthropic requires system prompt to be top-level parameter, not in messages list
        # This is a simplification; handling system messages specifically might be needed
        # depending on strictness, but for now we separate them.
        return [{"role": msg.role.value if msg.role.value != "system" else "user", "content": msg.content} for msg in messages if msg.role.value != "system"]

    def _extract_system_message(self, messages: List[Message]) -> str:
        system_msgs = [msg.content for msg in messages if msg.role == Role.SYSTEM]
        return system_msgs[0] if system_msgs else None

    def _convert_usage(self, usage) -> TokenUsage:
        return TokenUsage(
            input_tokens=usage.input_tokens,
            output_tokens=usage.output_tokens,
            total_tokens=usage.input_tokens + usage.output_tokens
        )

    def generate(self, request: LLMRequest) -> LLMResponse:
        system_msg = self._extract_system_message(request.messages)
        kwargs = {
            "model": self.model,
            "messages": self._convert_messages(request.messages),
            "max_tokens": request.max_tokens or 1024, # Anthropic requires max_tokens
            "temperature": request.temperature,
            "stop_sequences": request.stop_sequences or [],
        }
        if system_msg:
            kwargs["system"] = system_msg

        response = self.client.messages.create(**kwargs)
        
        return LLMResponse(
            content=response.content[0].text,
            usage=self._convert_usage(response.usage),
            provider="anthropic",
            model_name=self.model,
            raw_response=response
        )

    def stream(self, request: LLMRequest) -> Iterator[LLMResponseChunk]:
        system_msg = self._extract_system_message(request.messages)
        kwargs = {
            "model": self.model,
            "messages": self._convert_messages(request.messages),
            "max_tokens": request.max_tokens or 1024,
            "temperature": request.temperature,
            "stop_sequences": request.stop_sequences or [],
            "stream": True # Not strictly needed as we iterate
        }
        if system_msg:
            kwargs["system"] = system_msg

        with self.client.messages.stream(**kwargs) as stream:
            for text in stream.text_stream:
                yield LLMResponseChunk(
                    content_delta=text,
                    provider="anthropic",
                    model_name=self.model
                )

        final_msg = stream.get_final_message()
        if final_msg.usage:
            usage = self._convert_usage(final_msg.usage)
            yield LLMResponseChunk(
                content_delta="",
                provider="anthropic",
                model_name=self.model,
                usage=usage
            )

    async def generate_async(self, request: LLMRequest) -> LLMResponse:
        system_msg = self._extract_system_message(request.messages)
        kwargs = {
            "model": self.model,
            "messages": self._convert_messages(request.messages),
            "max_tokens": request.max_tokens or 1024,
            "temperature": request.temperature,
            "stop_sequences": request.stop_sequences or [],
        }
        if system_msg:
            kwargs["system"] = system_msg

        response = await self.async_client.messages.create(**kwargs)
        
        return LLMResponse(
            content=response.content[0].text,
            usage=self._convert_usage(response.usage),
            provider="anthropic",
            model_name=self.model,
            raw_response=response
        )

    async def stream_async(self, request: LLMRequest) -> AsyncIterator[LLMResponseChunk]:
        system_msg = self._extract_system_message(request.messages)
        kwargs = {
            "model": self.model,
            "messages": self._convert_messages(request.messages),
            "max_tokens": request.max_tokens or 1024,
            "temperature": request.temperature,
            "stop_sequences": request.stop_sequences or [],
        }
        if system_msg:
            kwargs["system"] = system_msg

        async with self.async_client.messages.stream(**kwargs) as stream:
            async for text in stream.text_stream:
                yield LLMResponseChunk(
                    content_delta=text,
                    provider="anthropic",
                    model_name=self.model
                )
            
            final_msg = await stream.get_final_message()
            if final_msg.usage:
                usage = self._convert_usage(final_msg.usage)
                yield LLMResponseChunk(
                    content_delta="",
                    provider="anthropic",
                    model_name=self.model,
                    usage=usage
                )
