# LangChain v0.3 Components — Examples

Examples based on the **LangChain v0.3 Main Components Guide** (PPTX/DOCX).

## 13 Essential Building Blocks

| # | File | Component |
|---|------|-----------|
| 1 | `1_chat_models.py` | LLMs & Chat Models — invoke, streaming |
| 2 | `2_prompts.py` | Prompt Templates — ChatPromptTemplate, MessagesPlaceholder, partial |
| 3 | `3_chains.py` | Classic chains (LLMChain, SequentialChain) |
| 4 | `4_parsers.py` | Output Parsers — Str, Json, Pydantic, CommaSeparatedList |
| 5 | `5_lcel_runnables.py` | LCEL & Runnables — pipe, RunnableParallel, RunnablePassthrough |
| 6 | `6_document_loaders.py` | Document Loaders — Text, PDF, Web, Directory |
| 7 | `7_text_splitters.py` | Text Splitters — RecursiveCharacterTextSplitter |
| 8 | `8_embeddings.py` | Embeddings — OpenAIEmbeddings |
| 9 | `9_vector_stores.py` | Vector Stores — FAISS |
| 10 | `10_retrievers.py` | Retrievers — similarity, MMR, RAG chain |
| 11 | `11_memory.py` | Memory & History — RunnableWithMessageHistory |
| 12 | `12_tools_agents.py` | Tools & Agents — create_react_agent |
| 13 | `13_callbacks.py` | Callbacks — streaming, custom TokenCounter |
| 14 | `14_ecosystem.py` | Ecosystem — LangSmith, LangGraph, LangServe |

## Setup

```bash
cd 8_langchain
pip install -r requirements.txt

# For full examples (loaders, vector stores, etc.):
pip install langchain-community langchain-text-splitters faiss-cpu pypdf beautifulsoup4 python-dotenv
```

Create `.env` with `OPENAI_API_KEY` (and optionally `ANTHROPIC_API_KEY`).

## Run

```bash
python 1_chat_models.py
python 2_prompts.py
python 4_parsers.py
python 5_lcel_runnables.py
# ... etc
```
