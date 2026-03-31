# RAG (Retrieval-Augmented Generation) — Interview Questions & Ideal Answers

---

## 1. RAG Fundamentals

**Q: What is RAG and why is it preferred over fine-tuning for many enterprise use cases?**

**A:**
RAG (Retrieval-Augmented Generation) enhances LLM responses by fetching relevant documents from an external knowledge base at query time and injecting them into the prompt as context.

**RAG vs. Fine-tuning comparison:**

| Dimension | RAG | Fine-tuning |
|---|---|---|
| Knowledge updates | Real-time — update the vector DB | Requires re-training |
| Cost | Low (vector DB + API calls) | High (GPU compute) |
| Transparency | Citable sources | Opaque |
| Hallucinations | Reduced (grounded in docs) | Still possible |
| Best for | Dynamic, large, proprietary knowledge bases | Changing model style/tone/format |

Use RAG when: the knowledge changes frequently (product docs, legal updates, internal wikis).
Use fine-tuning when: you need a specific output format or domain-specific reasoning style.

---

## 2. RAG Architecture

**Q: Draw the architecture of a production RAG pipeline. What happens at indexing time vs. query time?**

**A:**

**Indexing pipeline (offline / periodic):**
```
Raw Documents
    → Document Loader (PDF, URL, DB)
    → Text Splitter (chunk with overlap)
    → Embedding Model (text → float vector)
    → Vector Store (Chroma, Pinecone, pgvector)
```

**Query pipeline (online / per request):**
```
User Question
    → Embedding Model (question → vector)
    → Vector Store similarity search (top-K chunks)
    → Context assembly (question + retrieved chunks)
    → LLM (generate grounded answer)
    → Response (+ source citations)
```

```python
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Retriever
vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=OpenAIEmbeddings())
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

# RAG chain
rag_prompt = ChatPromptTemplate.from_template("""
Answer the question using ONLY the context below. If unsure, say "I don't know."

Context:
{context}

Question: {question}
""")

def format_docs(docs):
    return "\n\n---\n\n".join(d.page_content for d in docs)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | rag_prompt
    | ChatOpenAI(model="gpt-4o-mini")
    | StrOutputParser()
)

answer = rag_chain.invoke("What is our refund policy?")
```

---

## 3. Chunking Strategy

**Q: What chunking strategy would you use for a legal document vs. a code repository? Why does chunk size matter?**

**A:**

**Chunk size trade-offs:**
- **Too small**: individual chunks lack context; retrieval may return fragments.
- **Too large**: chunks exceed context window; irrelevant text dilutes the answer; more expensive.

**Strategy by document type:**

| Document Type | Strategy | Chunk size | Overlap |
|---|---|---|---|
| Legal / contracts | `RecursiveCharacterTextSplitter` by paragraph | 800–1200 chars | 200 chars |
| Code | `LanguageTextSplitter` by function/class | Per function | None |
| PDFs with tables | `PDFPlumberLoader` + structured extraction | Per table + context | N/A |
| FAQs | Split by Q&A pair | Per Q&A | None |

```python
from langchain_text_splitters import Language, RecursiveCharacterTextSplitter

# Code-aware splitting
code_splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.PYTHON,
    chunk_size=2000,
    chunk_overlap=0,  # functions don't need overlap
)
```

---

## 4. Retrieval Quality

**Q: What techniques can you use to improve retrieval accuracy in a RAG system?**

**A:**

**1. Hybrid search** — combine dense (embeddings) + sparse (BM25 keyword) retrieval:
```python
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever

bm25 = BM25Retriever.from_documents(docs)
dense = vectorstore.as_retriever()
hybrid = EnsembleRetriever(retrievers=[bm25, dense], weights=[0.4, 0.6])
```

**2. Re-ranking** — use a cross-encoder to re-score retrieved chunks:
```python
from langchain.retrievers.document_compressors import CrossEncoderReranker
from langchain.retrievers import ContextualCompressionRetriever

reranker = CrossEncoderReranker(model_name="cross-encoder/ms-marco-MiniLM-L-6-v2", top_n=3)
compressed = ContextualCompressionRetriever(base_compressor=reranker, base_retriever=retriever)
```

**3. Query expansion / HyDE** — generate a hypothetical answer first, then embed it for retrieval.

**4. Metadata filtering** — filter by date, document type, or user permissions before semantic search.

---

## 5. Hallucination Prevention

**Q: How do you reduce hallucinations in a RAG system?**

**A:**

1. **Ground the prompt** — instruct the model to only use provided context:
   ```
   Answer ONLY using the context below. Say "I don't know" if the answer is not in the context.
   ```

2. **Return source citations** — ask the model to cite the source chunk:
   ```python
   class AnswerWithSources(BaseModel):
       answer: str
       sources: list[str]  # document IDs or titles
   ```

3. **Faithfulness scoring** — use an LLM-as-judge to check if the answer is supported by the retrieved context (RAGAS framework).

4. **Increase retrieval K** — more context reduces gaps, but watch the context window limit.

5. **Confidence thresholding** — if similarity scores are all below a threshold, return "I don't have information on this topic."

---

## 6. Evaluation

**Q: How do you evaluate a RAG system? What metrics matter?**

**A:**
Use the **RAGAS** framework which measures three dimensions:

| Metric | Measures | Method |
|---|---|---|
| **Faithfulness** | Is the answer grounded in retrieved context? | LLM-as-judge |
| **Answer Relevancy** | Does the answer address the question? | Embedding similarity |
| **Context Recall** | Did retrieval find the needed documents? | Compare to ground truth |
| **Context Precision** | Are retrieved docs relevant? | LLM-as-judge |

```python
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_recall
from datasets import Dataset

data = Dataset.from_dict({
    "question": ["What is our return policy?"],
    "answer": ["Returns accepted within 30 days."],
    "contexts": [["Our policy allows returns within 30 days of purchase."]],
    "ground_truth": ["Items can be returned within 30 days."],
})

result = evaluate(data, metrics=[faithfulness, answer_relevancy, context_recall])
print(result)
```

---

## 7. Production Considerations

**Q: What would you add to a basic RAG prototype to make it production-ready?**

**A:**

1. **Caching** — cache embeddings and responses (Redis) to avoid redundant API calls.
2. **Incremental indexing** — re-index only changed documents, not the entire corpus.
3. **Access control** — filter retrieved chunks by user permissions (tenant isolation in multi-tenant apps).
4. **Observability** — log query, retrieved chunks, LLM input/output, latency, and token cost per request (LangSmith, Arize).
5. **Guardrails** — detect prompt injection, PII in retrieved context, and off-topic queries.
6. **Async indexing pipeline** — use a message queue (Celery, AWS SQS) so document uploads don't block the API.
7. **Chunking versioning** — if you change chunk size, re-index to avoid mismatches.
8. **Fallback** — if retrieval returns nothing relevant, fall back to a general answer or escalate to a human.
