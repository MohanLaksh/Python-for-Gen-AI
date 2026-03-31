# Python for Gen AI — Interview Questions Index

Real-world interview questions with ideal answers covering the full stack from Python fundamentals to production GenAI systems.

---

## Topics

| # | File | Topic | Questions |
|---|------|--------|-----------|
| 1 | [01_python_basics.md](01_python_basics.md) | Python Basics | Data types, strings, functions, OOP, decorators, generators, file handling |
| 2 | [02_packages_and_testing.md](02_packages_and_testing.md) | Packages & Testing | Package structure, pytest, fixtures, mocking, code coverage, pyproject.toml |
| 3 | [03_fastapi.md](03_fastapi.md) | FastAPI | Path/query params, Pydantic models, dependency injection, async endpoints, error handling |
| 4 | [04_requests_and_httpx.md](04_requests_and_httpx.md) | HTTP Clients (requests & httpx) | HTTP methods, session management, streaming SSE, retry/backoff, async concurrency |
| 5 | [05_pydantic.md](05_pydantic.md) | Pydantic | Model definition, nested models, field aliases, validators, structured LLM output, v1→v2 migration |
| 6 | [06_langchain.md](06_langchain.md) | LangChain | LCEL, chat models, prompt templates, output parsers, embeddings, memory, agents, callbacks |
| 7 | [07_rag_systems.md](07_rag_systems.md) | RAG Systems | Architecture, chunking strategy, hybrid search, re-ranking, hallucination prevention, RAGAS evaluation |
| 8 | [08_function_calling_and_agents.md](08_function_calling_and_agents.md) | Function Calling & Agents | Tool design, multi-tool agents, parallel tool calling, ReAct/Plan-and-Execute patterns, safety |
| 9 | [09_llm_api_design.md](09_llm_api_design.md) | LLM API Design | Provider abstraction, cost tracking, prompt engineering, context window management, observability |
| 10 | [10_async_and_performance.md](10_async_and_performance.md) | Async & Performance | asyncio vs threading, rate limiting, streaming responses, caching, profiling, memory leaks |
| 11 | [11_genai_system_design.md](11_genai_system_design.md) | GenAI System Design | Study assistant, code debugger, FAQ RAG system, LLM gateway design, scaling to 10K req/day |

---

## Learning Path

```
Python Basics (1)
    └── Packages & Testing (2)
            └── FastAPI (3)
                    └── HTTP Clients (4)
                            └── Pydantic (5)
                                    └── LangChain (6)
                                            ├── RAG Systems (7)
                                            ├── Function Calling & Agents (8)
                                            └── LLM API Design (9)
                                                        └── Async & Performance (10)
                                                                    └── System Design (11)
```

---

## Quick Reference by Interview Role

### Junior Python Developer
- [01 Python Basics](01_python_basics.md)
- [02 Packages & Testing](02_packages_and_testing.md)
- [03 FastAPI](03_fastapi.md)

### Mid-level AI/ML Engineer
- [05 Pydantic](05_pydantic.md)
- [06 LangChain](06_langchain.md)
- [07 RAG Systems](07_rag_systems.md)
- [04 HTTP Clients](04_requests_and_httpx.md)

### Senior GenAI Engineer / Architect
- [08 Function Calling & Agents](08_function_calling_and_agents.md)
- [09 LLM API Design](09_llm_api_design.md)
- [10 Async & Performance](10_async_and_performance.md)
- [11 GenAI System Design](11_genai_system_design.md)
