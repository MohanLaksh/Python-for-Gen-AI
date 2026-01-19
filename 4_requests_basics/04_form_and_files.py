"""
04 - Multipart form + file upload

`files=` sends multipart/form-data. We create an in-memory file for a clean demo.
"""

from __future__ import annotations

import io

import requests


def main() -> None:
    url = "https://httpbin.org/post"

    form_fields = {"description": "hello from requests"}
    fake_file = io.BytesIO(b"this is a tiny file content\nline2\n")

    files = {
        # field_name: (filename, fileobj/bytes, content_type)
        "upload": ("demo.txt", fake_file, "text/plain"),
    }

    try:
        r = requests.post(url, data=form_fields, files=files, timeout=10)
        r.raise_for_status()
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return

    payload = r.json()
    print("form echoed:", payload.get("form"))
    print("files echoed keys:", list((payload.get("files") or {}).keys()))
    print("files.upload content preview:", (payload.get("files") or {}).get("upload", "")[:60])


if __name__ == "__main__":
    main()
