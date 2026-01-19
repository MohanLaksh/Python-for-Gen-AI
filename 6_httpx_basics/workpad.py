"""
HTTPX Async Behavior Demonstration
===================================
This script demonstrates the key async behaviors of httpx:
1. Sequential vs Concurrent execution
2. Performance comparison
3. Error handling in async context
4. Practical patterns for API calls
"""

import httpx
import asyncio
import time
import json
import os
from typing import List, Dict, Any


def openAPI():
    # Never hardcode API keys. Use an environment variable instead:
    # export OPENAI_API_KEY='your-api-key-here'
    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key:
        raise RuntimeError(
            "Missing OPENAI_API_KEY. Set it in your environment, e.g.:\n"
            "  export OPENAI_API_KEY='your-api-key-here'"
        )
    headers = {
        "Authorization": f"Bearer {api_key}",
        "content-type": "application/json"
    }
    with httpx.Client(timeout=60.0) as client:
        # Correct Endpoint for Chat Completions
        url = "https://api.openai.com/v1/chat/completions"
        
        # Correct Payload structure for Chat API
        payload = {
            "model": "gpt-4o",  # Using a valid model name
            "messages": [
                {"role": "user", "content": "Hello, AI! Give me some long response on Gen AI developer"}
            ],
            "temperature": 0.7,
            "stream": True # Functionally required for streaming response in the body
        }
        
        with client.stream("POST", url, headers=headers, json=payload) as response:
            response.raise_for_status()
            for line in response.iter_lines():
                if line:
                    print(line)


openAPI()
