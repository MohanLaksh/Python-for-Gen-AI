from typing import List, Dict, Optional
import openai
from config import settings
from models.base_model import BaseLLMClient


class OpenAIClient(BaseLLMClient):
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or settings.openai_api_key
        self.model = model or settings.openai_model
        if self._validate_api_key():
            self.client = openai.OpenAI(api_key=self.api_key)
        else:
            self.client = None

    def generate_response(
        self,
        prompt: str,
        history: Optional[List[Dict[str, str]]] = None,
        temperature: Optional[float] = None
    ) -> str:
        if not self.client:
            raise ValueError("OpenAI client not initialized. Please check API key.")

        messages = self._build_messages(prompt, history)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature or settings.default_temperature,
                timeout=settings.default_timeout
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")

    async def generate_response_async(
        self,
        prompt: str,
        history: Optional[List[Dict[str, str]]] = None,
        temperature: Optional[float] = None
    ) -> str:
        if not self.client:
            raise ValueError("OpenAI client not initialized. Please check API key.")

        messages = self._build_messages(prompt, history)

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature or settings.default_temperature,
                timeout=settings.default_timeout
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")

    def stream_response(
        self,
        prompt: str,
        history: Optional[List[Dict[str, str]]] = None,
        temperature: Optional[float] = None
    ) -> str:
        if not self.client:
            raise ValueError("OpenAI client not initialized. Please check API key.")

        messages = self._build_messages(prompt, history)

        try:
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature or settings.default_temperature,
                stream=True,
                timeout=settings.default_timeout
            )

            full_response = ""
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
            return full_response
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")

    def _build_messages(
        self,
        prompt: str,
        history: Optional[List[Dict[str, str]]] = None
    ) -> List[Dict[str, str]]:
        messages = self._format_history(history)
        messages.append({"role": "user", "content": prompt})
        return messages
