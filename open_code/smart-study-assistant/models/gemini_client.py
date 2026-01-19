from typing import List, Dict, Optional
import google.generativeai as genai
from config import settings
from models.base_model import BaseLLMClient


class GeminiClient(BaseLLMClient):
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or settings.gemini_api_key
        self.model = model or settings.gemini_model
        if self._validate_api_key():
            genai.configure(api_key=self.api_key)
            self.client = genai.GenerativeModel(self.model)
        else:
            self.client = None

    def generate_response(
        self,
        prompt: str,
        history: Optional[List[Dict[str, str]]] = None,
        temperature: Optional[float] = None
    ) -> str:
        if not self.client:
            raise ValueError("Gemini client not initialized. Please check API key.")

        try:
            response = self.client.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature or settings.default_temperature
                )
            )
            return response.text
        except Exception as e:
            raise Exception(f"Gemini API error: {str(e)}")

    async def generate_response_async(
        self,
        prompt: str,
        history: Optional[List[Dict[str, str]]] = None,
        temperature: Optional[float] = None
    ) -> str:
        if not self.client:
            raise ValueError("Gemini client not initialized. Please check API key.")

        try:
            response = await self.client.generate_content_async(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature or settings.default_temperature
                )
            )
            return response.text
        except Exception as e:
            raise Exception(f"Gemini API error: {str(e)}")

    def stream_response(
        self,
        prompt: str,
        history: Optional[List[Dict[str, str]]] = None,
        temperature: Optional[float] = None
    ) -> str:
        if not self.client:
            raise ValueError("Gemini client not initialized. Please check API key.")

        try:
            response = self.client.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature or settings.default_temperature
                ),
                stream=True
            )

            full_response = ""
            for chunk in response:
                if chunk.text:
                    full_response += chunk.text
            return full_response
        except Exception as e:
            raise Exception(f"Gemini API error: {str(e)}")

    def _build_messages(
        self,
        prompt: str,
        history: Optional[List[Dict[str, str]]] = None
    ) -> List[Dict[str, str]]:
        messages = []
        if history:
            messages = history
        messages.append({"role": "user", "content": prompt})
        return messages
