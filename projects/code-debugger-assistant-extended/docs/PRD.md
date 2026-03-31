# Code Debugger Assistant
## Gen AI Web Application

**Product Requirements Document (PRD)**

| Field | Details |
|---|---|
| Product Name | Code Debugger Assistant (CDA) |
| Document Type | Product Requirements Document |
| Version | 1.0 — Initial Draft |
| Date | March 2026 |
| Status | In Review |
| Target Framework | Streamlit + LangChain + LangServe + FastAPI |
| Persistence Layer | PostgreSQL (chat history) + ChromaDB (vector store) |
| Primary LLM | OpenAI GPT-4 (via LangChain LCEL) |

---

## 1. Executive Summary

The Code Debugger Assistant (CDA) is an AI-powered web application that helps developers identify, understand, and resolve code bugs through a natural language chat interface. Leveraging LangChain's LCEL chain orchestration, LangServe for API gateway capabilities, OpenAI GPT-4 as the LLM backbone, ChromaDB for semantic code-snippet retrieval, and PostgreSQL for durable conversation history, CDA provides an intelligent debugging copilot accessible directly from the browser.

The application is delivered as a Streamlit single-page app, making it trivially deployable and easy to extend. The system is designed for software engineers, students, and teams that want a fast, context-aware debugging assistant without context loss across sessions.

---

## 2. Problem Statement

### 2.1 Pain Points

- Developers waste significant time context-switching between their IDE and generic LLM chat UIs, repeating error context with every new session.
- Existing chat-based AI tools lack persistent session memory — users cannot resume prior debugging threads.
- There is no semantic search over previously solved errors and code snippets within the same tool.
- Junior developers struggle to get structured, step-by-step explanations alongside the fix.

### 2.2 Opportunity

By combining a purpose-built Streamlit chat UI, a LangChain LCEL pipeline, a vector database of code/error patterns, and a PostgreSQL-backed conversation store, CDA eliminates context loss and delivers richer, more accurate debugging assistance than generic LLM interfaces.

---

## 3. Goals & Success Metrics

### 3.1 Goals

1. Deliver a chat interface where users paste code + error messages and receive structured debugging assistance.
2. Persist all conversations in PostgreSQL so sessions are resumable across browser refreshes and logins.
3. Use ChromaDB to store and retrieve semantically similar past errors and code snippets for RAG-augmented responses.
4. Provide an LCEL chain pipeline (Input Parser → Error Analyzer → Context Retriever → Code Fixer → Output Formatter) exposed via LangServe/FastAPI.
5. Enable in-session tool calls (AST Parser, Syntax Validator, Linter Integration) for deeper analysis.

### 3.2 Success Metrics

| Metric | Target | Measurement Method |
|---|---|---|
| Average response time (P95) | < 8 seconds | LangSmith latency tracing |
| Session resume success rate | > 98% | PostgreSQL integrity checks |
| RAG context retrieval precision | > 0.75 | Manual + automated eval |
| User-rated fix quality (1–5) | > 4.0 avg | In-app thumbs up/down |
| Streamlit app uptime | > 99.5% | Health check endpoint |

---

## 4. Scope

### 4.1 In Scope — v1.0

- Streamlit chat UI with multi-turn conversation support
- LangServe FastAPI gateway with endpoints: `POST /debug-code`, `POST /analyze-error`, `GET /fix-suggestions`, `POST /validate-fix`
- LCEL Chain: Input Parser → Error Analyzer → Context Retriever → Code Fixer → Test Validator → Output Formatter
- LLM Router: OpenAI GPT-4 (code generation & pattern recognition)
- Agent system: Input Validator, Error Classifier, Context Gatherer, Fix Generator, Solution Ranker, Explanation Builder, Feedback Processor
- Vector store: ChromaDB with code snippets and error patterns
- Persistence: PostgreSQL for conversation buffer, chat history, session state, user preferences
- Tools: AST Parser, Syntax Validator, Runtime Error Detector, Linter Integration (ESLint/Pylint), Code Formatter (Black/Prettier), Dependency Analyzer
- LangSmith tracing for observability

### 4.2 Out of Scope — v1.0

- AWS Bedrock integration (deferred to v2.0)
- Redis caching layer (deferred to v2.0)
- IDE plugin / VS Code extension
- GitHub PR integration
- Multi-user team workspaces

---

## 5. User Personas

| Persona | Role | Primary Need | Key Pain Point |
|---|---|---|---|
| Dev Dana | Mid-level Python / JS developer | Fast, context-aware bug fixes | Repeating error context in every chat session |
| Junior Jay | Bootcamp grad / junior engineer | Step-by-step explanations with fixes | Does not know where to start with cryptic stack traces |
| Tech Lead Priya | Senior engineer / team lead | Code review and pattern-based error spotting | Spending review cycles on repetitive bugs |
| Educator Raj | AI/coding instructor | Teaching debugging via AI interactions | No persistent session for student assignments |

---

## 6. System Architecture

### 6.1 High-Level Architecture Overview

The system is organised into five horizontal layers:

1. **User Interface Layer** — Streamlit web app delivering the chat interface.
2. **API Gateway Layer** — LangServe (FastAPI) exposing REST endpoints for debugging operations.
3. **Orchestration Layer** — LCEL Chain Orchestrator processing requests through a sequential pipeline.
4. **Intelligence Layer** — LLM Router directing requests to OpenAI GPT-4 with tool-augmented agent system.
5. **Persistence & Memory Layer** — PostgreSQL for relational conversation storage; ChromaDB for semantic vector retrieval.

### 6.2 LCEL Chain Pipeline

| # | Stage | Input | Output |
|---|---|---|---|
| 1 | Input Parser | Raw code + error string from user | Structured payload: language, error type, stack trace |
| 2 | Error Analyzer | Structured payload | Error classification, severity, root-cause hypothesis |
| 3 | Context Retriever | Error classification + code snippet | Top-k semantically similar snippets from ChromaDB |
| 4 | Code Fixer | Error analysis + RAG context | Candidate fix(es) with inline comments |
| 5 | Test Validator | Candidate fix | Linter + AST pass/fail report |
| 6 | Output Formatter | Validated fix + explanation | Structured markdown response sent to Streamlit |

### 6.3 LangServe API Endpoints

| Method | Endpoint | Request Body | Response |
|---|---|---|---|
| POST | `/debug-code` | `{ code, language, error_msg, session_id }` | `{ fix, explanation, confidence }` |
| POST | `/analyze-error` | `{ error_msg, language }` | `{ error_type, root_cause, severity }` |
| GET | `/fix-suggestions` | `?error_id=&session_id=` | `{ suggestions: [] }` |
| POST | `/validate-fix` | `{ original_code, fixed_code, language }` | `{ valid, lint_errors, ast_status }` |

---

## 7. Functional Requirements

### 7.1 Chat Interface (Streamlit)

- **FR-UI-01:** Multi-turn chat interface with code-block rendering and syntax highlighting for Python, JavaScript, TypeScript, and Java.
- **FR-UI-02:** Session selector sidebar listing all previous sessions by date/title, loaded from PostgreSQL.
- **FR-UI-03:** Code input area with language selector dropdown and optional error message text field.
- **FR-UI-04:** Thumbs up / thumbs down feedback widget per assistant response.
- **FR-UI-05:** Copy-to-clipboard button on all code blocks.
- **FR-UI-06:** Token usage and response latency displayed per turn (from LangSmith metadata).

### 7.2 Agent System

- **FR-AG-01:** Input Validator — Rejects non-code or empty inputs with a helpful error message.
- **FR-AG-02:** Error Classifier — Categorises errors into: SyntaxError, RuntimeError, LogicError, DependencyError, TypeMismatch, Other.
- **FR-AG-03:** Context Gatherer — Queries ChromaDB for the top-3 most semantically similar past errors.
- **FR-AG-04:** Fix Generator — Produces 1–3 ranked candidate fixes using GPT-4.
- **FR-AG-05:** Solution Ranker — Scores candidates on correctness, simplicity, and lint compliance.
- **FR-AG-06:** Explanation Builder — Generates a plain-English step-by-step explanation alongside the fix.
- **FR-AG-07:** Feedback Processor — Stores thumbs up/down against the fix in PostgreSQL for future fine-tuning.

### 7.3 Persistence Layer

#### 7.3.1 PostgreSQL Schema (Core Tables)

```sql
sessions(session_id PK, user_id, title, created_at, updated_at, language_preference)
messages(message_id PK, session_id FK, role ENUM[user|assistant], content TEXT, token_count, latency_ms, created_at)
feedback(feedback_id PK, message_id FK, rating SMALLINT, comment TEXT, created_at)
error_classifications(classification_id PK, message_id FK, error_type, root_cause, severity, created_at)
```

#### 7.3.2 ChromaDB Collections

| Collection | Embeds | Used For |
|---|---|---|
| `code_snippets` | Code blocks + language metadata | RAG context retrieval |
| `error_patterns` | Error messages + stack traces | Error similarity matching |
| `fix_history` | Validated fixes | Solution ranking reference |

### 7.4 Tools & Utilities Integration

- **FR-TL-01:** AST Parser — Python (`ast` module) and JavaScript (`acorn`) for structural code analysis.
- **FR-TL-02:** Syntax Validator — Pre-execution syntax check before presenting fixes.
- **FR-TL-03:** Linter Integration — Pylint for Python, ESLint for JavaScript; results included in fix validation.
- **FR-TL-04:** Code Formatter — Black for Python, Prettier for JavaScript; applied to all returned code blocks.
- **FR-TL-05:** Dependency Analyzer — Detects missing imports or version conflicts from error context.

---

## 8. Non-Functional Requirements

| Category | Requirement | Target | Notes |
|---|---|---|---|
| Performance | End-to-end response time (P95) | < 8 s | Excludes streaming tokens |
| Scalability | Concurrent Streamlit sessions | Up to 50 users | Horizontal pod scaling |
| Availability | Application uptime | > 99.5% monthly | Health-check endpoint |
| Security | API key management | Env vars / secrets manager | Never in source code |
| Security | PII in conversation logs | Redacted before storage | Regex + LLM guard |
| Observability | LangSmith tracing | 100% of LCEL runs | Error rate + latency |
| Data Retention | PostgreSQL conversation history | 90 days default | Configurable per user |
| Portability | Containerisation | Docker Compose setup | Streamlit + FastAPI + PG + Chroma |

---

## 9. Technology Stack

| Layer | Technology | Version | Purpose |
|---|---|---|---|
| UI | Streamlit | 1.33+ | Chat interface & session management |
| API Gateway | LangServe + FastAPI | 0.1+ | REST endpoints, request routing |
| Orchestration | LangChain LCEL | 0.3+ | Chain pipeline construction |
| LLM | OpenAI GPT-4 | gpt-4o | Code generation, error analysis |
| Vector DB | ChromaDB | 0.5+ | Semantic code/error retrieval (RAG) |
| Relational DB | PostgreSQL | 16+ | Chat history, session state, feedback |
| Observability | LangSmith | Latest | Tracing, metrics, latency tracking |
| Linting | Pylint + ESLint | Latest | Code quality validation in fixes |
| Formatting | Black + Prettier | Latest | Consistent code formatting |
| Containerisation | Docker + Compose | Latest | Local & cloud deployment |

---

## 10. Execution Flow & Data Flow

### 10.1 Primary Debug Request Flow

1. User submits code snippet + error message via Streamlit chat input.
2. Streamlit calls `POST /debug-code` on the LangServe FastAPI gateway with `{ code, error_msg, language, session_id }`.
3. LCEL Chain is invoked: Input Parser validates and structures the payload.
4. Error Analyzer classifies error type and generates root-cause hypothesis using GPT-4.
5. Context Retriever queries ChromaDB (`error_patterns` + `code_snippets` collections) for top-3 similar contexts.
6. Code Fixer sends combined [error analysis + RAG context + original code] to GPT-4 and receives candidate fixes.
7. Test Validator runs AST Parser + Linter on each candidate fix and returns a pass/fail score.
8. Output Formatter structures the winning fix with explanation into markdown.
9. PostgreSQL: The full conversation turn (user message + assistant response + metadata) is persisted.
10. ChromaDB: The validated fix is upserted into `fix_history` for future RAG retrieval.
11. Streamlit renders the response with syntax-highlighted code blocks and the feedback widget.

### 10.2 Session Resume Flow

1. User opens the app and selects a prior session from the sidebar.
2. Streamlit loads all messages for that `session_id` from PostgreSQL.
3. Chat history is hydrated as `LangChain ConversationBufferMemory` and passed into the LCEL chain context.
4. All subsequent turns in the session maintain full conversation context.

---

## 11. UI/UX Requirements

### 11.1 Layout

- **Left sidebar:** Session list, new session button, language filter.
- **Main panel:** Chat message stream with user (right-aligned) and assistant (left-aligned) bubbles.
- **Input bar (bottom):** Multi-line code input + error message field + Submit button.
- **Top-right:** LangSmith token/latency mini-widget.

### 11.2 Chat Message Display

- Code blocks rendered with `st.code()` with syntax highlighting.
- Error classifications shown as coloured badges (red = RuntimeError, yellow = SyntaxError, etc.).
- Explanation section collapsible using `st.expander()` to reduce visual clutter.
- Each assistant turn includes a thumbs up / thumbs down row for feedback capture.

---

## 12. Monitoring & Observability

- All LCEL chain runs automatically traced in LangSmith (project: `cda-production`).
- Custom LangSmith tags: `error_type`, `language`, `session_id`, `fix_validated`.
- PostgreSQL `error_classifications` table feeds a Streamlit admin dashboard showing error type distribution and success rate.
- Response latency tracked per chain stage; P50 / P95 / P99 reported in LangSmith.
- Feedback scores (thumbs up/down) aggregated weekly and surfaced in the admin dashboard.

---

## 13. Deployment Architecture

### 13.1 Docker Compose Services

| Service | Port | Purpose |
|---|---|---|
| `streamlit-app` | 8501 | Streamlit UI |
| `langserve-api` | 8100 | FastAPI / LangServe |
| `postgres` | 5432 | Relational DB (volume-mounted) |
| `chromadb` | 8080 | Vector DB server (volume-mounted) |

### 13.2 Environment Variables

```bash
OPENAI_API_KEY=           # OpenAI API key for GPT-4
LANGSMITH_API_KEY=        # LangSmith project key
LANGCHAIN_PROJECT=        # LangSmith project name (default: cda-production)
POSTGRES_URL=             # PostgreSQL connection string
CHROMA_HOST=              # ChromaDB server host
CHROMA_PORT=              # ChromaDB server port
```

---

## 14. Development Milestones

| # | Milestone | Deliverables | Target Week |
|---|---|---|---|
| M1 | Foundation | Project scaffold, Docker Compose, PostgreSQL schema, ChromaDB init | Week 1 |
| M2 | LCEL Chain v1 | Input Parser + Error Analyzer + Code Fixer pipeline with GPT-4 | Week 2 |
| M3 | RAG Integration | ChromaDB collections, Context Retriever stage, initial seed data | Week 3 |
| M4 | LangServe API | All 4 endpoints live, LangSmith tracing enabled | Week 4 |
| M5 | Streamlit UI | Full chat UI, session sidebar, code rendering, feedback widget | Week 5 |
| M6 | Tools Layer | AST Parser, Pylint/ESLint, Black/Prettier integration | Week 6 |
| M7 | Testing & QA | Unit tests, integration tests, LangSmith eval runs | Week 7 |
| M8 | v1.0 Release | Production Docker build, documentation, demo walkthrough | Week 8 |

---

## 15. Risks & Mitigations

| Risk | Likelihood | Mitigation |
|---|---|---|
| GPT-4 API rate limits impacting response time | Medium | Exponential backoff; GPT-3.5-turbo fallback for simple classifications |
| ChromaDB cold-start latency on first similarity query | Low | Warm-up query on app start; pre-populate seed dataset |
| PostgreSQL connection pool exhaustion under concurrent users | Medium | SQLAlchemy connection pooling (`pool_size=10`, `max_overflow=20`) |
| LangSmith tracing adds overhead to critical path | Low | Async tracing callbacks; tracing is non-blocking |
| LLM hallucinating incorrect fixes | Medium | AST + Linter validation stage rejects invalid fixes; user feedback loop |
| Sensitive code / credentials submitted by users | Medium | PII regex scan + LLM guard layer before persistence |

---

## 16. Future Roadmap — v2.0+

- **AWS Bedrock Claude integration** — Error Analysis and Code Reasoning via AWS Bedrock as an alternate LLM route.
- **Redis caching** — Cache frequent fixes and session data for sub-second repeat query responses.
- **IDE Plugin** — VS Code extension calling the LangServe API directly from the editor.
- **GitHub PR Integration** — Automatically scan PR diffs for potential bugs and suggest fixes.
- **Multi-user team workspaces** — Shared fix history and team-level ChromaDB collections.
- **Fine-tuning pipeline** — Use accumulated feedback data to fine-tune a custom debugging model.

---

## 17. Glossary

| Term | Definition |
|---|---|
| LCEL | LangChain Expression Language — a declarative way to compose LangChain chains using the pipe operator. |
| LangServe | LangChain's FastAPI-based server for deploying LCEL chains as production REST APIs. |
| RAG | Retrieval-Augmented Generation — augmenting LLM prompts with retrieved context from a vector store. |
| ChromaDB | An open-source vector database for storing and querying text embeddings. |
| AST | Abstract Syntax Tree — a tree representation of the syntactic structure of source code. |
| LangSmith | LangChain's observability platform for tracing, evaluating, and monitoring LLM applications. |
| LCEL Chain | An ordered sequence of LangChain Runnable components composed via `|` (pipe) operators. |
| Session | A single continuous debugging conversation stored in PostgreSQL and addressable by `session_id`. |

---

*Code Debugger Assistant — PRD v1.0 — March 2026*
