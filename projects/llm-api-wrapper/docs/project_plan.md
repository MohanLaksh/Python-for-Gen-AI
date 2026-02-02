# LLM API Wrapper - Project Plan

## Project Overview
**Project Name:** LLM API Wrapper
**Goal:** Create a unified Python class for interacting with multiple AI/LLM provider APIs (OpenAI, Anthropic, Gemini) through a single and consistent interface.

## Core Features
1.  **Multi-Provider Support:**
    *   OpenAI (e.g., GPT-4o, GPT-3.5-turbo)
    *   Anthropic (e.g., Claude 3.5 Sonnet)
    *   Google Gemini (e.g., Gemini 1.5 Pro/Flash)

2.  **Consistent Interface:**
    *   Unified input (prompt, system message, parameters like temperature/max_tokens).
    *   Unified output (standardized response object with content, usage stats).

3.  **Advanced Capabilities:**
    *   **Token Tracking:** Report input, output, and total tokens for every request.
    *   **Streaming:** Support for streaming responses across all providers.
    *   **Fault Tolerance:** Automatic retries on transient errors and fallback to alternative providers if the primary fails.

4.  **User Interfaces:**
    *   **CLI:** Command-line tool for quick testing.
    *   **Web App:** Streamlit-based UI for interactive chatting and configuration.

## Tech Stack
*   **Language:** Python 3.10+
*   **Core Libraries:**
    *   `pydantic`: For data validation and unified models.
    *   `httpx`: For asynchronous HTTP requests (or SDKs where preferable).
    *   `openai`: Official OpenAI SDK.
    *   `anthropic`: Official Anthropic SDK.
    *   `google-genai`: Official Google Gen AI SDK (v1.0+).
*   **UI/Web:** `streamlit`, `rich` (for CLI).
*   **Environment Management:** `python-dotenv`.

---

## Implementation Checklist

### Phase 1: Planning and Setup
- [ ] Create project structure and documentation.
- [ ] Initialize `docs/project_plan.md`.
- [ ] Set up virtual environment and `requirements.txt` / `pyproject.toml`.
- [ ] Create `.env` template for API keys.

### Phase 2: Core Architecture
- [ ] **Data Models:** Define `Pydantic` models for:
    -   `LLMRequest`: (prompt, messages, temperature, max_tokens, etc.)
    -   `LLMResponse`: (content, raw_response, provider, model_name)
    -   `TokenUsage`: (input_tokens, output_tokens, total_tokens)
- [ ] **Abstract Base Class:** Create `LLMProvider` ABC with methods:
    -   `generate(request: LLMRequest) -> LLMResponse`
    -   `stream(request: LLMRequest) -> Iterator[LLMResponseChunk]`
    -   `count_tokens(text: str) -> int`

### Phase 3: Provider Implementation
- [ ] **OpenAI Provider:** Implement `OpenAIProvider` class.
- [ ] **Anthropic Provider:** Implement `AnthropicProvider` class.
- [ ] **Gemini Provider:** Implement `GeminiProvider` class.
- [ ] **Unit Tests:** Basic tests for each provider (using mocks).

### Phase 4: Unified Wrapper & Application Logic
- [ ] **Unified Interface:** Create `UnifiedLLM` class.
- [ ] **Logic:** Implement provider selection and configuration.
- [ ] **Fault Tolerance:** Implement automatic retry logic and fallback mechanisms (e.g., if OpenAI fails, try Anthropic).

### Phase 5: UI Implementation
- [ ] **CLI:** Create `cli` module used to interact with the wrapper from terminal.
- [ ] **Streamlit App:** Build a web interface with:
    -   Sidebar for settings (provider selection, API keys).
    -   Chat interface.
    -   Display of token usage and costs (optional).

### Phase 6: Refinement
- [ ] Add logging.
- [ ] Finalize documentation (README.md).
- [ ] specific error handling improvement.
