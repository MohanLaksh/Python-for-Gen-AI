from typing import List, Optional
from pydantic import BaseModel, Field

class SummaryOutput(BaseModel):
    title: str = Field(..., description="A concise title for the summary")
    summary: str = Field(..., description="The main summary of the text")
    key_points: List[str] = Field(..., description="A list of key points extracted from the text")
    confidence: Optional[float] = Field(None, description="Confidence score of the summarization (0.0 to 1.0)")
