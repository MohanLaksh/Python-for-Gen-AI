from __future__ import annotations

import json
import os
from typing import Any, Dict, Optional

import requests
from dotenv import load_dotenv
from openai import OpenAI


WEATHER_API_BASE_URL = "https://api.openweathermap.org/data/2.5"
DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
DEBUG = os.getenv("DEBUG", "").strip().lower() in {"1", "true", "yes", "y"}


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a city name (OpenWeatherMap).",
            "parameters": {
                "type": "object",
                "properties": {
                    "q": {"type": "string", "description": "City name (e.g. Bengaluru)"},
                    "unit": {
                        "type": "string",
                        "description": "Temperature unit to return",
                        "enum": ["celsius", "fahrenheit"],
                    },
                },
                "required": ["q"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather_by_zip",
            "description": (
                "Get current weather for a ZIP/postal code and country code (OpenWeatherMap). "
                "Use this when the user provides a zip/postal code."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "zip_code": {"type": "string", "description": "ZIP/postal code (e.g. 94040)"},
                    "country_code": {"type": "string", "description": "Country code (e.g. US, IN)"},
                    "unit": {
                        "type": "string",
                        "description": "Temperature unit to return",
                        "enum": ["celsius", "fahrenheit"],
                    },
                },
                "required": ["zip_code", "country_code"],
                "additionalProperties": False,
            },
        },
    },
]


def _safe_json_loads(text: Optional[str]) -> Dict[str, Any]:
    if not text:
        return {}
    try:
        parsed = json.loads(text)
        return parsed if isinstance(parsed, dict) else {}
    except json.JSONDecodeError:
        return {}


def _unit_to_openweather_units(unit: str) -> str:
    return "imperial" if unit == "fahrenheit" else "metric"


def _require_env(name: str) -> Optional[str]:
    value = os.getenv(name)
    return value if value else None


def _openweather_get(session: requests.Session, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
    api_key = _require_env("WEATHER_API_KEY")
    if not api_key:
        return {"error": "WEATHER_API_KEY is not set in the environment."}

    url = f"{WEATHER_API_BASE_URL}/{endpoint.lstrip('/')}"
    params_with_key = dict(params)
    params_with_key["appid"] = api_key

    try:
        response = session.get(url, params=params_with_key, timeout=10)
        response.raise_for_status()
        payload = response.json()
        return payload if isinstance(payload, dict) else {"data": payload}
    except requests.HTTPError as e:
        body: Any = None
        try:
            body = response.json()
        except Exception:
            body = getattr(response, "text", None)
        return {
            "error": "OpenWeatherMap request failed.",
            "status_code": getattr(response, "status_code", None),
            "details": body,
        }
    except requests.RequestException as e:
        return {"error": "Network error calling OpenWeatherMap.", "details": str(e)}


def get_weather(q: str, unit: str = "celsius") -> Dict[str, Any]:
    units = _unit_to_openweather_units(unit)
    with requests.Session() as session:
        return _openweather_get(session, "weather", {"q": q, "units": units})


def get_weather_by_zip(zip_code: str, country_code: str, unit: str = "celsius") -> Dict[str, Any]:
    units = _unit_to_openweather_units(unit)
    # https://api.openweathermap.org/data/2.5/weather?zip={zip code},{country code}&appid={API key}
    with requests.Session() as session:
        return _openweather_get(
            session,
            "weather",
            {"zip": f"{zip_code},{country_code}", "units": units},
        )


def _dispatch_tool_call(tool_name: str, tool_args: Dict[str, Any]) -> Dict[str, Any]:
    if tool_name == "get_weather":
        return get_weather(**tool_args)
    if tool_name == "get_weather_by_zip":
        return get_weather_by_zip(**tool_args)
    return {"error": f"Unknown tool: {tool_name}"}


def run_once(prompt: str) -> str:
    openai_api_key = _require_env("OPENAI_API_KEY")
    if not openai_api_key:
        return "Error: OPENAI_API_KEY is not set in the environment."

    client = OpenAI(api_key=openai_api_key)

    messages: list[Dict[str, Any]] = [{"role": "user", "content": prompt}]

    response = client.chat.completions.create(
        model=DEFAULT_MODEL,
        messages=messages,
        tools=TOOLS,
        tool_choice="auto",
    )

    msg = response.choices[0].message
    messages.append(msg)

    if DEBUG:
        print("assistant_message:", msg)

    if msg.tool_calls:
        for tool_call in msg.tool_calls:
            if tool_call.type != "function":
                continue

            tool_name = tool_call.function.name
            tool_args = _safe_json_loads(tool_call.function.arguments)
            result = _dispatch_tool_call(tool_name, tool_args)

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result),
                }
            )

        final = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=messages,
            tools=TOOLS,
        )
        return final.choices[0].message.content or ""

    return msg.content or ""


def main() -> None:
    load_dotenv()
    prompt = input("Enter your prompt: ").strip()
    if not prompt:
        print("No prompt provided.")
        return
    print(run_once(prompt))


if __name__ == "__main__":
    main()
