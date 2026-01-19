"""
05 - Basic Auth

httpbin has a basic-auth endpoint that returns 200 only if auth matches.
"""

from __future__ import annotations

import requests


def main() -> None:
    user = "user"
    passwd = "passwd"
    url = f"https://httpbin.org/basic-auth/{user}/{passwd}"

    try:
        r = requests.get(url, auth=(user, passwd), timeout=10)
        r.raise_for_status()
    except requests.HTTPError as e:
        print("Auth failed or endpoint returned an error.")
        print("Status:", getattr(e.response, "status_code", None))
        return
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return

    print("Status:", r.status_code)
    print("Response JSON:", r.json())


if __name__ == "__main__":
    main()
