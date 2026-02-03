import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    
    # LM Studio defaults
    LMSTUDIO_BASE_URL = os.getenv("lmstudio_base_url", "http://localhost:1234/v1")
    
    # Defaults
    DEFAULT_MODEL_OPENAI = "gpt-4-turbo" # Or gpt-3.5-turbo
    DEFAULT_MODEL_ANTHROPIC = "claude-sonnet-4-5" # Example
    DEFAULT_MODEL_GEMINI = "gemini-pro"
    DEFAULT_MODEL_LMSTUDIO = "local-model" # Placeholder

config = Config()
