"""
03 - POST JSON body
"""

from __future__ import annotations

import requests


def main() -> None:
    url = "https://httpbin.org/post"
    data = {"name": "Vinod", "topic": "requests", "ok": True}

    try:
        r = requests.post(url, json=data, timeout=10)
        r.raise_for_status()
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return

    payload = r.json()
    print("Status:", r.status_code)
    print("JSON echoed by server:", payload.get("json"))


if __name__ == "__main__":
    main()
