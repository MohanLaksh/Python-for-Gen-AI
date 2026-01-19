# Python for Gen AI

A hands-on learning workspace for Python fundamentals and the building blocks commonly used in Gen AI apps (HTTP clients, FastAPI, Pydantic, notebooks).

## Repository map

- **`1_python_basics/`**: Core Python (types, strings, collections, control flow, functions, files, exceptions, OOP, decorators).
- **`2_packages/`**: A tiny package + unit tests (good for learning imports + tests).
- **`3_fastapi/`**: A small FastAPI app demonstrating common API patterns.
- **`4_requests_basics/`**: Runnable `requests` examples (auth, retries, sessions).
- **`5_basic_pydantic/`**: Pydantic basics + a few advanced patterns.
- **`6_httpx_basics/`**: `httpx` sync/async/streaming patterns, plus LLM-style examples.
- **`7_jupyter_notebook/`**: Notebook(s) for interactive exploration.
- **`open_code/`**: Larger “open code” sample projects (complete mini-apps you can run end-to-end).

## Open code projects

### Smart Study Assistant (`open_code/smart-study-assistant/`)

Multi-role CLI assistant that routes tasks between OpenAI / Gemini / Claude based on the query type/complexity.

```bash
cd "open_code/smart-study-assistant"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Set at least one API key (recommended: use a local .env file)
# OPENAI_API_KEY=...
# GEMINI_API_KEY=...
# ANTHROPIC_API_KEY=...

python main.py chat
```

## Setup (recommended)

Create a virtual environment **per module** (each folder may have its own `requirements.txt`).

```bash
# From this repo root
cd "3_fastapi"  # or 4_requests_basics / 6_httpx_basics / ...

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt  # if this module has one
```

## Run examples

### Python scripts

```bash
python3 1_python_basics/1_print_functions.py
python3 4_requests_basics/01_get_json.py
python3 6_httpx_basics/01_httpx-basics.py
```

### FastAPI

```bash
cd "3_fastapi"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

uvicorn main:app --reload
```

Then open:
- **Docs**: `http://127.0.0.1:8000/docs`
- **Health**: `http://127.0.0.1:8000/health`

## Notes

- **Internet required** for many HTTP examples (`requests`/`httpx`).
- **API keys**: if you run any LLM/OpenAI-style examples, prefer environment variables (e.g. `OPENAI_API_KEY`) and keep secrets out of git.

