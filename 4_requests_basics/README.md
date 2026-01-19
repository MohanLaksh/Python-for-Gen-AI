# Requests Basics (Simple, Runnable Examples)

This folder contains small scripts demonstrating the most common patterns in Python's `requests` library.

Most examples use [`httpbin`](https://httpbin.org/) because it echoes back what you sent (great for learning).

## Setup

```bash
cd "/Users/vinod/Desktop/Python for Gen AI/6_requests_basics"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run an example

```bash
python3 01_get_json.py
```

## Examples included

- `01_get_json.py`: basic GET + JSON parsing + `raise_for_status()`
- `02_params_headers.py`: query params + custom headers
- `03_post_json.py`: POST JSON body
- `04_form_and_files.py`: multipart form + file upload
- `05_basic_auth.py`: Basic Auth
- `06_api_key_auth.py`: API Key based auth (headers)
- `07_timeouts_and_retries.py`: timeouts + simple retry strategy
- `08_session_cookies.py`: `requests.Session()` + cookies

## Notes

- These examples require internet access.
- If you get blocked by a network/corporate proxy, set standard env vars like `HTTP_PROXY` / `HTTPS_PROXY`.
