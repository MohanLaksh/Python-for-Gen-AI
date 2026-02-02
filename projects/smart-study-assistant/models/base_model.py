from abc import ABC, abstractmethod
from typing import List, Dict, Any, AsyncGenerator, Optional


class BaseLLMClient(ABC):
    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model

    @abstractmethod
    def generate_response(
        self,
        prompt: str,
        history: Optional[List[Dict[str, str]]] = None,
        temperature: Optional[float] = None
    ) -> str:
        pass

    @abstractmethod
    async def generate_response_async(
        self,
        prompt: str,
        history: Optional[List[Dict[str, str]]] = None,
        temperature: Optional[float] = None
    ) -> str:
        pass

    @abstractmethod
    def stream_response(
        self,
        prompt: str,
        history: Optional[List[Dict[str, str]]] = None,
        temperature: Optional[float] = None
    ) -> str:
        pass

    def _validate_api_key(self) -> bool:
        return bool(self.api_key)

    def _format_history(self, history: Optional[List[Dict[str, str]]]) -> List[Dict[str, str]]:
        if history is None:
            return []
        return history
