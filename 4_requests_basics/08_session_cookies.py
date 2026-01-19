"""
08 - requests.Session() + cookies

Sessions persist cookies and default headers across requests.
"""

from __future__ import annotations

import requests


def main() -> None:
    with requests.Session() as session:
        session.headers.update({"X-Demo": "session-example"})

        try:
            # Set a cookie on the server side
            session.get("https://httpbin.org/cookies/set?course=python", timeout=10).raise_for_status()

            # Read cookies back
            r = session.get("https://httpbin.org/cookies", timeout=10)
            r.raise_for_status()
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            return

        print("Cookies stored in session:", session.cookies.get_dict())
        print("Cookies echoed by server:", r.json().get("cookies"))


if __name__ == "__main__":
    main()
