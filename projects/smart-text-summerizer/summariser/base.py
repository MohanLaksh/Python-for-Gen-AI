from abc import ABC, abstractmethod
from typing import Dict, Any
from schemas.summary_schema import SummaryOutput

class BaseLLMClient(ABC):
    @abstractmethod
    def summarize(self, text: str, tone: str = "neutral", schema: str = "") -> SummaryOutput:
        """
        Summarize the given text using the specific LLM provider.
        
        Args:
            text: The input text to summarize.
            tone: The desired tone of the summary.
            schema: The JSON schema to enforce for the output.
            
        Returns:
            SummaryOutput: The structured summary output.
        """
        pass
