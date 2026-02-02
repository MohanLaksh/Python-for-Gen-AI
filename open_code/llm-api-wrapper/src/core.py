from abc import ABC, abstractmethod
from typing import Iterator, AsyncIterator
from .models import LLMRequest, LLMResponse, LLMResponseChunk

class LLMProvider(ABC):
    """Abstract base class for LLM providers."""

    @abstractmethod
    def generate(self, request: LLMRequest) -> LLMResponse:
        """
        Generate a complete response from the LLM.
        
        Args:
            request (LLMRequest): The unified request object.
            
        Returns:
            LLMResponse: The unified response object including usage stats.
        """
        pass

    @abstractmethod
    def stream(self, request: LLMRequest) -> Iterator[LLMResponseChunk]:
        """
        Stream the response from the LLM.
        
        Args:
            request (LLMRequest): The unified request object.
            
        Returns:
            Iterator[LLMResponseChunk]: An iterator yielding response chunks.
        """
        pass
    
    @abstractmethod
    async def generate_async(self, request: LLMRequest) -> LLMResponse:
        """
        Asynchronously generate a complete response from the LLM.
        
        Args:
            request (LLMRequest): The unified request object.
            
        Returns:
            LLMResponse: The unified response object including usage stats.
        """
        pass

    @abstractmethod
    async def stream_async(self, request: LLMRequest) -> AsyncIterator[LLMResponseChunk]:
        """
        Asynchronously stream the response from the LLM.
        
        Args:
            request (LLMRequest): The unified request object.
            
        Returns:
            AsyncIterator[LLMResponseChunk]: An async iterator yielding response chunks.
        """
        pass
