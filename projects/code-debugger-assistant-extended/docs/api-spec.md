# Code Debugger Assistant — API Specification

## Base URL

```
http://localhost:8100
```

---

## Authentication

All endpoints require the LangServe API to be running. No user-level authentication is required in v1.0. API keys (OpenAI, LangSmith) are managed server-side via environment variables.

---

## Endpoints

### 1. POST /debug-code

Full debugging pipeline — submit code + error message, receive structured fix.

**Request Body:**

```json
{
  "code": "string",
  "language": "string (python | javascript | typescript | java)",
  "error_msg": "string",
  "session_id": "string (UUID, optional — auto-generated if omitted)"
}
```

**Response (200):**

```json
{
  "fix": "string (corrected code block)",
  "explanation": "string (step-by-step explanation of the fix)",
  "confidence": "float (0.0 – 1.0)",
  "error_classification": {
    "error_type": "string (SyntaxError | RuntimeError | LogicError | DependencyError | TypeMismatch | Other)",
    "root_cause": "string",
    "severity": "string (low | medium | high | critical)"
  },
  "rag_context": [
    {
      "snippet": "string",
      "similarity_score": "float",
      "source": "string (collection name)"
    }
  ],
  "metadata": {
    "session_id": "string (UUID)",
    "message_id": "string (UUID)",
    "token_count": "integer",
    "latency_ms": "integer",
    "model": "string",
    "chain_stages": ["input_parser", "error_analyzer", "context_retriever", "code_fixer", "test_validator", "output_formatter"]
  }
}
```

**Error Responses:**

| Status | Body | Condition |
|---|---|---|
| 400 | `{ "detail": "Code field is required" }` | Empty code input |
| 400 | `{ "detail": "Unsupported language: ..." }` | Unknown language value |
| 422 | Pydantic validation error | Malformed request body |
| 500 | `{ "detail": "LLM invocation failed" }` | OpenAI API error |
| 503 | `{ "detail": "Service unavailable" }` | Downstream dependency down |

---

### 2. POST /analyze-error

Lightweight error classification only — no fix generation.

**Request Body:**

```json
{
  "error_msg": "string",
  "language": "string (python | javascript | typescript | java)"
}
```

**Response (200):**

```json
{
  "error_type": "string (SyntaxError | RuntimeError | LogicError | DependencyError | TypeMismatch | Other)",
  "root_cause": "string",
  "severity": "string (low | medium | high | critical)",
  "suggested_action": "string",
  "metadata": {
    "token_count": "integer",
    "latency_ms": "integer",
    "model": "string"
  }
}
```

---

### 3. GET /fix-suggestions

Retrieve cached or ranked fix suggestions for a previously classified error.

**Query Parameters:**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `error_id` | string (UUID) | Yes | ID of the classified error (from `/analyze-error` or `/debug-code`) |
| `session_id` | string (UUID) | Yes | Session context |
| `limit` | integer | No | Max suggestions to return (default: 3) |

**Response (200):**

```json
{
  "suggestions": [
    {
      "rank": 1,
      "fix": "string (corrected code)",
      "confidence": "float",
      "source": "string (llm | rag_cache | fix_history)",
      "lint_status": "string (pass | fail)",
      "ast_valid": "boolean"
    }
  ],
  "total_candidates": "integer",
  "metadata": {
    "session_id": "string",
    "error_id": "string"
  }
}
```

---

### 4. POST /validate-fix

Run AST parsing and linter validation on a proposed code fix.

**Request Body:**

```json
{
  "original_code": "string",
  "fixed_code": "string",
  "language": "string (python | javascript | typescript | java)"
}
```

**Response (200):**

```json
{
  "valid": "boolean",
  "ast_status": {
    "parseable": "boolean",
    "error": "string | null"
  },
  "lint_errors": [
    {
      "line": "integer",
      "column": "integer",
      "rule": "string",
      "message": "string",
      "severity": "string (warning | error)"
    }
  ],
  "formatting_applied": "boolean",
  "formatted_code": "string (only if formatting_applied is true)"
}
```

---

### 5. POST /feedback

Submit user feedback on an assistant response.

**Request Body:**

```json
{
  "message_id": "string (UUID)",
  "rating": "integer (1 = thumbs down, 5 = thumbs up)",
  "comment": "string (optional)"
}
```

**Response (200):**

```json
{
  "feedback_id": "string (UUID)",
  "status": "recorded"
}
```

---

### 6. GET /sessions

List all sessions for the current user.

**Query Parameters:**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `user_id` | string | No | Filter by user (default: anonymous) |
| `limit` | integer | No | Max sessions to return (default: 20) |
| `offset` | integer | No | Pagination offset (default: 0) |

**Response (200):**

```json
{
  "sessions": [
    {
      "session_id": "string (UUID)",
      "title": "string",
      "language_preference": "string",
      "created_at": "string (ISO 8601)",
      "updated_at": "string (ISO 8601)",
      "message_count": "integer"
    }
  ],
  "total": "integer"
}
```

---

### 7. GET /sessions/{session_id}/messages

Retrieve all messages for a specific session (for session resume).

**Path Parameters:**

| Parameter | Type | Description |
|---|---|---|
| `session_id` | string (UUID) | Session identifier |

**Response (200):**

```json
{
  "session_id": "string",
  "messages": [
    {
      "message_id": "string (UUID)",
      "role": "string (user | assistant)",
      "content": "string",
      "token_count": "integer",
      "latency_ms": "integer | null",
      "created_at": "string (ISO 8601)",
      "feedback": {
        "rating": "integer | null",
        "comment": "string | null"
      }
    }
  ]
}
```

---

### 8. GET /health

Health check endpoint for monitoring.

**Response (200):**

```json
{
  "status": "healthy",
  "services": {
    "langserve": "up",
    "postgresql": "up | down",
    "chromadb": "up | down",
    "openai": "up | down"
  },
  "version": "1.0.0",
  "uptime_seconds": "integer"
}
```

---

## Common Headers

| Header | Value | Notes |
|---|---|---|
| `Content-Type` | `application/json` | All request/response bodies |
| `X-Request-ID` | UUID | Auto-generated per request for tracing |
| `X-Session-ID` | UUID | Echoed from request for client correlation |

---

## Rate Limiting (v1.0)

No rate limiting is enforced at the application level in v1.0. Rate limits are inherited from the OpenAI API tier. Exponential backoff with jitter is implemented in the LLM router for 429 responses.

---

*Code Debugger Assistant — API Specification v1.0*
