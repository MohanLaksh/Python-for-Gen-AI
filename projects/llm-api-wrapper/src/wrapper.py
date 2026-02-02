import logging
from typing import List, Optional, Iterator, AsyncIterator
from .core import LLMProvider
from .models import LLMRequest, LLMResponse, LLMResponseChunk
from .providers.openai_provider import OpenAIProvider
from .providers.anthropic_provider import AnthropicProvider
from .providers.gemini_provider import GeminiProvider

# Configure logging
logger = logging.getLogger(__name__)

class UnifiedLLM(LLMProvider):
    def __init__(self, providers: List[LLMProvider] = None, retry_attempts: int = 1):
        """
        Initialize the UnifiedLLM wrapper.
        
        Args:
            providers (List[LLMProvider]): A list of initialized provider instances.
                                           The order determines the fallback priority.
        """
        self.providers = providers or []
        self.retry_attempts = retry_attempts
        
        # If no providers given, try to initialize all standard ones if keys exist
        if not self.providers:
            try:
                self.providers.append(OpenAIProvider())
            except ValueError:
                pass
            
            try:
                self.providers.append(AnthropicProvider())
            except ValueError:
                pass
                
            try:
                self.providers.append(GeminiProvider())
            except ValueError:
                pass
                
        if not self.providers:
            logger.warning("No providers could be initialized. Please check API keys.")

    def get_provider(self, name: str) -> Optional[LLMProvider]:
        for p in self.providers:
            # Simplistic check - assuming class name or adding a name property to ABC would be better
            # For now, let's assume the provider instance has a 'provider' attribute or we check type
            if isinstance(p, OpenAIProvider) and name == "openai":
                return p
            if isinstance(p, AnthropicProvider) and name == "anthropic":
                return p
            if isinstance(p, GeminiProvider) and name == "gemini":
                return p
        return None

    def _get_providers_chain(self, provider_name: str = None) -> List[LLMProvider]:
        """
        Get the list of providers to try, prioritizing the requested one if valid.
        """
        if not provider_name:
            return self.providers
            
        specific_provider = self.get_provider(provider_name)
        if not specific_provider:
            logger.warning(f"Requested provider '{provider_name}' not available (not initialized). Falling back to other active providers.")
            return self.providers
            
        # Prioritize specific provider, then others
        return [specific_provider] + [p for p in self.providers if p != specific_provider]

    def generate(self, request: LLMRequest, provider_name: str = None) -> LLMResponse:
        """
        Generate response with fallback logic.
        
        Args:
            request: The LLMRequest
            provider_name: Optional specific provider to prioritize.
        """
        providers_to_try = self._get_providers_chain(provider_name)
        
        last_error = None
        
        for provider in providers_to_try:
            try:
                logger.info(f"Attempting generation with provider: {provider.__class__.__name__}")
                return provider.generate(request)
            except Exception as e:
                logger.error(f"Provider {provider.__class__.__name__} failed: {e}")
                last_error = e
                continue
        
        raise RuntimeError("All providers failed to generate response.") from last_error

    def stream(self, request: LLMRequest, provider_name: str = None) -> Iterator[LLMResponseChunk]:
        """
        Stream response with fallback logic.
        """
        providers_to_try = self._get_providers_chain(provider_name)

        last_error = None
        
        for provider in providers_to_try:
            try:
                logger.info(f"Attempting streaming with provider: {provider.__class__.__name__}")
                yield from provider.stream(request)
                return # Success
            except Exception as e:
                logger.error(f"Provider {provider.__class__.__name__} failed: {e}")
                last_error = e
                continue
        
        raise RuntimeError("All providers failed to stream response.") from last_error

    async def generate_async(self, request: LLMRequest, provider_name: str = None) -> LLMResponse:
        providers_to_try = self._get_providers_chain(provider_name)

        last_error = None
        
        for provider in providers_to_try:
            try:
                logger.info(f"Attempting async generation with provider: {provider.__class__.__name__}")
                return await provider.generate_async(request)
            except Exception as e:
                logger.error(f"Provider {provider.__class__.__name__} failed: {e}")
                last_error = e
                continue
        
        raise RuntimeError("All providers failed to generate response.") from last_error

    async def stream_async(self, request: LLMRequest, provider_name: str = None) -> AsyncIterator[LLMResponseChunk]:
        providers_to_try = self._get_providers_chain(provider_name)

        last_error = None
        
        for provider in providers_to_try:
            try:
                logger.info(f"Attempting async streaming with provider: {provider.__class__.__name__}")
                async for chunk in provider.stream_async(request):
                    yield chunk
                return
            except Exception as e:
                logger.error(f"Provider {provider.__class__.__name__} failed: {e}")
                last_error = e
                continue
        
        raise RuntimeError("All providers failed to stream response.") from last_error
