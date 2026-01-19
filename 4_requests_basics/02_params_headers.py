"""
02 - Query params + custom headers

httpbin.org/get echoes back the query params and headers you sent.
"""

from __future__ import annotations

import requests


def main() -> None:
    url = "https://httpbin.org/get"

    params = {"q": "python requests", "page": 1}
    headers = {"X-Demo": "requests-basics", "Accept": "application/json"}

    try:
        r = requests.get(url, params=params, headers=headers, timeout=10)
        r.raise_for_status()
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return

    payload = r.json()
    print("URL that httpbin saw:", payload.get("url"))
    print("args (query params):", payload.get("args"))
    print("X-Demo header:", payload.get("headers", {}).get("X-Demo"))


if __name__ == "__main__":
    main()
