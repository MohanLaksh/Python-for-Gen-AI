# Smart Text Summariser

A Python-based multi-LLM summarisation engine supporting OpenAI, Anthropic, Gemini, and LM Studio.

## Setup

1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Configure API Keys:**
    Copy `.env.example` to `.env` and fill in your API keys.
    ```bash
    cp .env.example .env
    ```

## Usage

Run the summariser via CLI:

```bash
# Summarize a file using OpenAI (default)
python main.py --input-file path/to/article.txt

# Summarize raw text using Anthropic with 'executive' tone
python main.py --provider anthropic --text "Your long text here..." --tone executive

# Summarize using local LM Studio
python main.py --provider lmstudio --input-file path/to/article.txt
```

## Options

-   `--provider`: `openai` (default), `anthropic`, `gemini`, `lmstudio`
-   `--input-file`: Path to text file to summarize
-   `--text`: Raw text string to summarize
-   `--tone`: Tone of the summary (neutral, simple, executive, etc.)
