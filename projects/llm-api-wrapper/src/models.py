from enum import Enum
from typing import List, Optional, Any
from pydantic import BaseModel, Field

class Role(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"

class Message(BaseModel):
    role: Role
    content: str

class LLMRequest(BaseModel):
    messages: List[Message]
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    stream: bool = False
    stop_sequences: Optional[List[str]] = None

class TokenUsage(BaseModel):
    input_tokens: int
    output_tokens: int
    total_tokens: int

class LLMResponse(BaseModel):
    content: str
    usage: Optional[TokenUsage] = None
    provider: str
    model_name: str
    raw_response: Any = Field(default=None, exclude=True)

class LLMResponseChunk(BaseModel):
    content_delta: str
    provider: str
    model_name: str
    usage: Optional[TokenUsage] = None
