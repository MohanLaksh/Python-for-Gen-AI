"""
06 - API Key based auth (headers)

Many APIs accept API keys/tokens in headers, commonly:
- Authorization: Bearer <token>
- X-API-Key: <api_key>

This uses httpbin.org to echo back what we sent.
"""

from __future__ import annotations

import os

import requests


def main() -> None:
    api_key = os.getenv("DEMO_API_KEY", "demo_api_key_123")

    # Example A: Bearer token (very common for modern APIs)
    try:
        r = requests.get(
            "https://httpbin.org/bearer",
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=10,
        )
        r.raise_for_status()
        print("Bearer auth response:", r.json())
    except requests.RequestException as e:
        print(f"Bearer auth request failed: {e}")

    # Example B: X-API-Key header (also common)
    try:
        r2 = requests.get(
            "https://httpbin.org/headers",
            headers={"X-API-Key": api_key},
            timeout=10,
        )
        r2.raise_for_status()
        headers = (r2.json() or {}).get("headers", {}) or {}

        # Header casing can vary; find it case-insensitively.
        echoed = None
        for k, v in headers.items():
            if k.lower() == "x-api-key":
                echoed = v
                break

        print("X-API-Key echoed by server:", echoed)
    except requests.RequestException as e:
        print(f"X-API-Key request failed: {e}")


if __name__ == "__main__":
    main()
