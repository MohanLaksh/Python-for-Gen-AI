"""
01 - Basic GET + JSON parsing + error handling
"""

from __future__ import annotations

import requests


def main() -> None:
    url = "https://api.github.com/users/octocat"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.Timeout:
        print("Timed out. Check your internet connection and try again.")
        return
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return

    data = response.json()
    print("Status:", response.status_code)
    print("login:", data.get("login"))
    print("name:", data.get("name"))
    print("public_repos:", data.get("public_repos"))


if __name__ == "__main__":
    main()
