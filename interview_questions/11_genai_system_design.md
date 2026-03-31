# GenAI System Design — Interview Questions & Ideal Answers

---

## 1. Design a Study Assistant

**Q: Design a smart study assistant that can answer questions about uploaded course materials, quiz the student, and track progress.**

**A:**

**Requirements clarification:**
- Upload PDFs/notes → Q&A over them.
- Generate quizzes from the material.
- Track quiz performance over time.
- Multi-turn conversation with memory.

**Architecture:**

```
┌─────────────┐     upload      ┌──────────────────┐
│   Student   │ ────────────→  │  Indexing Service │
│  (Browser)  │                 │  - PyPDF loader   │
└─────┬───────┘                 │  - Text splitter  │
      │ questions               │  - Embeddings     │
      ▼                         │  - ChromaDB       │
┌─────────────┐                 └──────────────────┘
│  FastAPI    │ ←── RAG retriever ──────────────────┘
│  Backend    │
│  - /chat    │ ──→ ChatOpenAI  ──→ Answer + citations
│  - /quiz    │ ──→ QuizGen LLM ──→ MCQ/flashcards
│  - /results │ ──→ Postgres    ──→ Score history
└─────────────┘
```

**Key design decisions:**

```python
# 1. Session-aware RAG chain
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationSummaryBufferMemory

chain = ConversationalRetrievalChain.from_llm(
    llm=ChatOpenAI(model="gpt-4o-mini"),
    retriever=vectorstore.as_retriever(search_kwargs={"k": 5}),
    memory=ConversationSummaryBufferMemory(
        llm=ChatOpenAI(model="gpt-4o-mini"),
        max_token_limit=2000,
        return_messages=True,
    ),
    return_source_documents=True,
)

# 2. Quiz generation
class QuizQuestion(BaseModel):
    question: str
    options: list[str]         # 4 options
    correct_index: int
    explanation: str

quiz_chain = (
    ChatPromptTemplate.from_template(
        "Generate {n} multiple-choice questions from this material. "
        "Return JSON matching the QuizQuestion schema.\n\n{material}"
    )
    | ChatOpenAI(model="gpt-4o").with_structured_output(list[QuizQuestion])
)
```

---

## 2. Design a Code Debugging Assistant

**Q: Design an AI assistant that helps developers debug Python code. What are the key features and failure modes?**

**A:**

**Core features:**
1. Accept buggy code + error traceback.
2. Identify the bug with explanation.
3. Provide fixed code.
4. Explain the fix.
5. Suggest tests to prevent regression.

```python
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

class DebugResult(BaseModel):
    bug_description: str
    root_cause: str
    fixed_code: str
    explanation: str
    test_suggestions: list[str]

debug_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an expert Python debugger.
    Analyse the code and error, identify the root cause, provide a minimal fix.
    Do NOT rewrite unrelated code. Preserve the original structure."""),
    ("human", """Code:
```python
{code}
```

Error:
```
{error}
```

Analyse and fix this bug."""),
])

llm = ChatOpenAI(model="gpt-4o", temperature=0)
debug_chain = debug_prompt | llm.with_structured_output(DebugResult)

# Usage
result = debug_chain.invoke({
    "code": "def divide(a, b):\n    return a / b\n\nresult = divide(10, 0)",
    "error": "ZeroDivisionError: division by zero",
})
```

**Failure modes and mitigations:**
| Failure | Mitigation |
|---|---|
| LLM invents bugs that don't exist | Always include exact traceback |
| Fix introduces new bugs | Sandbox execution (subprocess/Docker) |
| Context window exceeded for large files | Send only the relevant function + traceback |
| Hallucinated library methods | Ask LLM to explain each API call used |
| Security: user submits malicious code for analysis | Never execute user code without sandboxing |

---

## 3. Design a FAQ RAG System

**Q: A company has 500 FAQ entries. Design a system to answer customer questions using those FAQs. How do you handle questions that aren't in the FAQs?**

**A:**

**Indexing:**
```python
from langchain_core.documents import Document

# Structure each FAQ as a Document with metadata
faqs = [
    Document(
        page_content=f"Q: {faq['question']}\nA: {faq['answer']}",
        metadata={"category": faq["category"], "id": faq["id"]},
    )
    for faq in load_faqs_from_db()
]

# Use small chunk_size — each FAQ is already a self-contained unit
vectorstore = Chroma.from_documents(
    faqs,
    OpenAIEmbeddings(model="text-embedding-3-small"),
)
```

**Query with fallback:**
```python
class FAQResponse(BaseModel):
    answer: str
    confidence: float    # 0.0 – 1.0
    source_faq_id: int | None
    escalate_to_human: bool

def answer_faq(question: str) -> FAQResponse:
    docs = vectorstore.similarity_search_with_score(question, k=3)

    # If best match score is too low, escalate
    best_score = docs[0][1] if docs else 0
    if best_score < 0.75:
        return FAQResponse(
            answer="I don't have a specific answer for this. Let me connect you with our support team.",
            confidence=best_score,
            source_faq_id=None,
            escalate_to_human=True,
        )

    context = "\n\n".join(d.page_content for d, _ in docs)
    result = rag_chain.invoke({"context": context, "question": question})
    return FAQResponse(
        answer=result,
        confidence=best_score,
        source_faq_id=docs[0][0].metadata["id"],
        escalate_to_human=False,
    )
```

**Handling out-of-scope questions:**
1. Low similarity score → route to human agent.
2. LLM instructed: "If the answer is not in the FAQs, say 'I don't have information on this.'"
3. Log all unanswered questions → review weekly → add to FAQ database.

---

## 4. LLM API Wrapper Design

**Q: How would you design a multi-provider LLM wrapper that handles failover, caching, and cost tracking?**

**A:**

```python
from dataclasses import dataclass, field
from typing import Iterator
import time

@dataclass
class CallStats:
    provider: str
    model: str
    prompt_tokens: int
    completion_tokens: int
    latency_ms: float
    cost_usd: float
    cache_hit: bool = False

class LLMGateway:
    def __init__(self, providers: list[LLMProvider], cache: LLMCache | None = None):
        self.providers = providers
        self.cache = cache
        self.stats: list[CallStats] = []

    def complete(self, prompt: str, temperature: float = 0.7) -> tuple[str, CallStats]:
        # Check cache for deterministic calls
        if temperature == 0 and self.cache:
            cached = self.cache.get(prompt)
            if cached:
                return cached, CallStats(..., cache_hit=True)

        # Try providers in order (failover)
        last_error = None
        for provider in self.providers:
            try:
                start = time.perf_counter()
                response = provider.complete(prompt, temperature=temperature)
                latency = (time.perf_counter() - start) * 1000

                stats = CallStats(
                    provider=type(provider).__name__,
                    model=provider.model,
                    prompt_tokens=count_tokens(prompt),
                    completion_tokens=count_tokens(response.content),
                    latency_ms=latency,
                    cost_usd=self._estimate_cost(provider.model, prompt, response.content),
                )
                self.stats.append(stats)

                if temperature == 0 and self.cache:
                    self.cache.set(prompt, response.content)

                return response.content, stats

            except Exception as e:
                last_error = e
                print(f"Provider {type(provider).__name__} failed: {e}, trying next...")
                continue

        raise RuntimeError(f"All providers failed. Last error: {last_error}")

# Usage
gateway = LLMGateway(
    providers=[OpenAIProvider("gpt-4o-mini"), AnthropicProvider("claude-haiku-3-5")],
    cache=RedisCache(),
)
answer, stats = gateway.complete("What is RAG?", temperature=0)
print(f"Cost: ${stats.cost_usd:.5f}, Latency: {stats.latency_ms:.0f}ms")
```

---

## 5. Scaling Considerations

**Q: Your GenAI application needs to handle 10,000 requests per day. What infrastructure decisions do you need to make?**

**A:**

**Compute:**
- FastAPI + uvicorn with multiple workers (`--workers 4`).
- Deploy on Kubernetes with horizontal pod autoscaling based on request queue depth.

**API rate limits:**
- OpenAI tier 3: ~500 RPM. At 10,000 req/day = ~7 RPM average → well within limits.
- Implement queue + worker pool for burst traffic.

**Caching:**
- Redis cache for repeat queries (expect 30–50% hit rate for FAQ systems).
- Saves ~$50–200/month at typical usage.

**Cost estimate:**
```
10,000 requests/day
× 500 tokens avg (prompt + completion)
= 5M tokens/day
× $0.00015/1K (gpt-4o-mini)
= $0.75/day = ~$23/month
```

**Observability stack:**
- Structured logging → CloudWatch/Datadog.
- Latency, token cost, error rate dashboards.
- Alerts: error rate > 1%, P95 latency > 5s.

**Data:**
- Store all Q&A pairs for fine-tuning dataset creation.
- Vector DB: Chroma (dev) → Pinecone or pgvector (production) for persistence and filtering.
