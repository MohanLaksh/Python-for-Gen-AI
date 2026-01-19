"""
07 - Timeouts + (simple) retries

Requests doesn't have built-in retries for all cases, but you can add a retry policy
via urllib3's Retry + a mounted HTTPAdapter.
"""

from __future__ import annotations

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def build_session_with_retries() -> requests.Session:
    retry = Retry(
        total=3,
        backoff_factor=0.5,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset({"GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS"}),
        raise_on_status=False,
    )

    adapter = HTTPAdapter(max_retries=retry)
    session = requests.Session()
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def main() -> None:
    # Timeout can be float (total) or tuple: (connect_timeout, read_timeout)
    timeout = (3, 5)

    # A slow endpoint for demonstration.
    url = "https://httpbin.org/delay/2"

    # 1) Simple timeout demo
    try:
        r = requests.get(url, timeout=timeout)
        r.raise_for_status()
        print("No timeout. Status:", r.status_code)
    except requests.Timeout:
        print("Timed out (as expected). Try increasing timeout or check network.")
    except requests.RequestException as e:
        print(f"Request failed: {e}")

    # 2) Retry demo (useful for transient 5xx / 429)
    session = build_session_with_retries()
    try:
        r2 = session.get("https://httpbin.org/status/500", timeout=timeout)
        print("Retry demo status:", r2.status_code)
        print(
            "Note: httpbin/status/500 always returns 500, so retries won't 'fix' it; "
            "this just demonstrates the mechanism."
        )
    except requests.RequestException as e:
        print(f"Request failed: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    main()
