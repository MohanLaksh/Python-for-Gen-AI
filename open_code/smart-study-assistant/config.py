import os
from dotenv import load_dotenv
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    openai_api_key: str = Field(default="", env="OPENAI_API_KEY")
    gemini_api_key: str = Field(default="", env="GEMINI_API_KEY")
    anthropic_api_key: str = Field(default="", env="ANTHROPIC_API_KEY")

    openai_model: str = Field(default="gpt-4o-mini", env="OPENAI_MODEL")
    openai_advanced_model: str = Field(default="gpt-4o", env="OPENAI_ADVANCED_MODEL")
    gemini_model: str = Field(default="gemini-1.5-flash", env="GEMINI_MODEL")
    anthropic_model: str = Field(default="claude-3-5-sonnet-20240620", env="ANTHROPIC_MODEL")

    max_history_length: int = Field(default=10, env="MAX_HISTORY_LENGTH")
    default_temperature: float = Field(default=0.7, env="DEFAULT_TEMPERATURE")
    default_timeout: int = Field(default=30, env="DEFAULT_TIMEOUT")

    @field_validator("default_temperature")
    @classmethod
    def validate_temperature(cls, v: float) -> float:
        if not 0 <= v <= 2:
            raise ValueError("Temperature must be between 0 and 2")
        return v

    @field_validator("max_history_length")
    @classmethod
    def validate_history_length(cls, v: int) -> int:
        if v < 0:
            raise ValueError("History length must be non-negative")
        return v


settings = Settings()
