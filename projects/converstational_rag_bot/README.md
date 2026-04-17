# Conversational RAG bot

Small LangChain demo that combines **retrieval-augmented generation (RAG)** with **chat memory**: each `session_id` keeps its own conversation, and every answer is grounded in snippets retrieved from a local **Chroma** vector store.

## What the script does

1. **Ingest** — A fixed list of `Document` objects (tutorial blurbs about LangChain, embeddings, MMR, etc.) is embedded and written to a persisted Chroma collection.
2. **Retrieve** — For each user question, a retriever pulls the top‑k most relevant chunks (default: similarity search, `k=2`).
3. **Generate** — A chat prompt includes: system instructions + retrieved **context** + prior **history** + the current **question**. An OpenAI chat model returns the answer.
4. **Remember** — `RunnableWithMessageHistory` loads history for the given `session_id`, injects it into the `"history"` slot, and after each call appends the new user and assistant messages automatically.

See the module docstring and `make_prepare_prompt_inputs` in `conv_rag_bot.py` for how each turn dict is turned into `context` / `question` / `history` before the prompt runs.

## Prerequisites

- Python 3.10+ (project tested with 3.14 in a local venv).
- An [OpenAI API key](https://platform.openai.com/api-keys) (used for embeddings via Chroma’s default embedding class and for the chat model).

## Setup

1. Create a virtual environment and install dependencies (adjust versions to match your course repo if needed):

   ```bash
   cd projects/converstational_rag_bot
   python -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   pip install python-dotenv langchain-chroma langchain-core langchain-openai langchain-community chromadb
   ```

2. Copy environment variables (do not commit real secrets):

   ```bash
   cp .env.example .env
   ```

   Then edit `.env` and set `OPENAI_API_KEY`.

3. Set at least:

   | Variable | Purpose |
   |----------|---------|
   | `OPENAI_API_KEY` | OpenAI authentication |
   | `CHROMA_COLLECTION_NAME` | Chroma collection name |
   | `CHROMA_PERSIST_DIRECTORY` | Folder for persisted Chroma data (e.g. `./chroma_db`) |

   Optional: `CHROMA_EMBEDDING_MODEL` if your embedding setup reads it from the environment.

4. Run:

   ```bash
   python conv_rag_bot.py
   ```

   Type questions at the prompt; enter `exit` to quit.

## Project layout

| Path | Role |
|------|------|
| `conv_rag_bot.py` | Full pipeline: ingest, chain, CLI |
| `.gitignore` | Ignores `.env`, `.venv`, `chroma_db/`, etc. |
| `conversational_rag_bot.excalidraw` | Optional architecture sketch (Excalidraw) |

## Retrieval modes (code)

`retrieve_documents` supports the same three strategies as before:

- `similarity` — vanilla top‑k similarity.
- `mmr` — Max Marginal Relevance (`k`, `fetch_k`).
- `multi_query` — LLM expands the query into several variants, then merges results.

`run_bot` currently wires **`similarity`** into `build_rag_chain`; change that string to experiment.

## Troubleshooting

- **`Expected document to be a str, got {...}` from Chroma** — The retriever was invoked with a dict instead of the question string. This repo uses an explicit `prepare_prompt_inputs` step that reads `turn["question"]` before retrieval to avoid that.
- **Empty or wrong retrieval** — Delete the local Chroma directory and run again so documents are re-ingested, or use a fresh `CHROMA_COLLECTION_NAME`.
- **API errors** — Confirm `OPENAI_API_KEY` in `.env` and billing/limits on the OpenAI dashboard.

## Security

Never commit `.env` or API keys. Rotate any key that was exposed in a screenshot, chat, or public repository.
