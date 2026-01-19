from typing import List, Dict, Optional
import anthropic
from config import settings
from models.base_model import BaseLLMClient


class ClaudeClient(BaseLLMClient):
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or settings.anthropic_api_key
        self.model = model or settings.anthropic_model
        if self._validate_api_key():
            self.client = anthropic.Anthropic(api_key=self.api_key)
        else:
            self.client = None

    def generate_response(
        self,
        prompt: str,
        history: Optional[List[Dict[str, str]]] = None,
        temperature: Optional[float] = None
    ) -> str:
        if not self.client:
            raise ValueError("Claude client not initialized. Please check API key.")

        messages = self._build_messages(prompt, history)

        try:
            response = self.client.messages.create(
                model=self.model,
                messages=messages,
                temperature=temperature or settings.default_temperature,
                timeout=settings.default_timeout
            )
            return response.content[0].text
        except Exception as e:
            raise Exception(f"Claude API error: {str(e)}")

    async def generate_response_async(
        self,
        prompt: str,
        history: Optional[List[Dict[str, str]]] = None,
        temperature: Optional[float] = None
    ) -> str:
        if not self.client:
            raise ValueError("Claude client not initialized. Please check API key.")

        messages = self._build_messages(prompt, history)

        try:
            response = await self.client.messages.create(
                model=self.model,
                messages=messages,
                temperature=temperature or settings.default_temperature,
                timeout=settings.default_timeout
            )
            return response.content[0].text
        except Exception as e:
            raise Exception(f"Claude API error: {str(e)}")

    def stream_response(
        self,
        prompt: str,
        history: Optional[List[Dict[str, str]]] = None,
        temperature: Optional[float] = None
    ) -> str:
        if not self.client:
            raise ValueError("Claude client not initialized. Please check API key.")

        messages = self._build_messages(prompt, history)

        try:
            stream = self.client.messages.create(
                model=self.model,
                messages=messages,
                temperature=temperature or settings.default_temperature,
                stream=True,
                timeout=settings.default_timeout
            )

            full_response = ""
            for chunk in stream:
                if hasattr(chunk, 'delta') and hasattr(chunk.delta, 'text'):
                    full_response += chunk.delta.text
            return full_response
        except Exception as e:
            raise Exception(f"Claude API error: {str(e)}")

    def _build_messages(
        self,
        prompt: str,
        history: Optional[List[Dict[str, str]]] = None
    ) -> List[Dict[str, str]]:
        messages = self._format_history(history)
        messages.append({"role": "user", "content": prompt})
        return messages
