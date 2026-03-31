# LangChain — Interview Questions & Ideal Answers

---

## 1. Core Architecture

**Q: Explain the main components of LangChain and how they compose together.**

**A:**
LangChain is built around four composable primitives:

| Component | Purpose | Example |
|---|---|---|
| **Chat Models** | Wrap LLM providers (OpenAI, Anthropic) | `ChatOpenAI`, `ChatAnthropic` |
| **Prompts** | Structured templates for messages | `ChatPromptTemplate` |
| **Output Parsers** | Transform raw LLM text into typed data | `PydanticOutputParser`, `JsonOutputParser` |
| **Chains / LCEL** | Compose primitives into pipelines | `prompt | llm | parser` |

LCEL (LangChain Expression Language) uses the `|` pipe operator, similar to Unix shell pipelines:

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(model="gpt-4o-mini")
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a concise technical writer."),
    ("human", "Summarise this in 2 sentences: {text}"),
])

chain = prompt | llm | StrOutputParser()
result = chain.invoke({"text": "Long article about transformers..."})
```

---

## 2. Chat Models & Streaming

**Q: How do you stream a response from a LangChain chat model? Why is streaming important for user experience?**

**A:**
Streaming yields tokens as they are generated, giving users immediate feedback instead of a blank screen for 10+ seconds.

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o", streaming=True)

# Stream to console
for chunk in llm.stream("Explain vector databases in detail"):
    print(chunk.content, end="", flush=True)
```

In a FastAPI + WebSocket application:
```python
@app.websocket("/ws/chat")
async def chat_ws(websocket: WebSocket):
    await websocket.accept()
    query = await websocket.receive_text()
    async for chunk in llm.astream(query):
        await websocket.send_text(chunk.content)
    await websocket.close()
```

---

## 3. Prompt Templates

**Q: What is the difference between `PromptTemplate` and `ChatPromptTemplate`? When does it matter?**

**A:**
- `PromptTemplate` produces a **single string** — designed for completion-style (legacy) models.
- `ChatPromptTemplate` produces a **list of messages** with roles (`system`, `human`, `ai`) — required by chat models (GPT-4, Claude, Gemini).

```python
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Multi-turn conversation template
template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful {role}. Respond in {language}."),
    MessagesPlaceholder(variable_name="history"),  # inserts prior messages
    ("human", "{question}"),
])

messages = template.format_messages(
    role="data analyst",
    language="English",
    history=[],
    question="What is a p-value?",
)
```

`MessagesPlaceholder` is key for conversation memory — it injects the full chat history dynamically.

---

## 4. Output Parsers

**Q: How do you reliably extract structured data (e.g., a list of entities) from LLM output?**

**A:**
Use `PydanticOutputParser` to combine schema definition and parsing:

```python
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

class ExtractedEntities(BaseModel):
    people: list[str]
    organisations: list[str]
    locations: list[str]

parser = PydanticOutputParser(pydantic_object=ExtractedEntities)

prompt = ChatPromptTemplate.from_messages([
    ("system", "Extract entities. {format_instructions}"),
    ("human", "{text}"),
]).partial(format_instructions=parser.get_format_instructions())

llm = ChatOpenAI(model="gpt-4o-mini")
chain = prompt | llm | parser

result = chain.invoke({"text": "Elon Musk founded SpaceX in Hawthorne, California."})
print(result.people)        # ['Elon Musk']
print(result.organisations) # ['SpaceX']
print(result.locations)     # ['Hawthorne, California']
```

---

## 5. Document Loaders & Text Splitters

**Q: You have a 200-page PDF. Walk through the process of making it searchable with LangChain.**

**A:**
```python
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

# Step 1: Load
loader = PyPDFLoader("report.pdf")
pages = loader.load()  # list of Document objects, one per page

# Step 2: Split into overlapping chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,       # ~250 tokens at 4 chars/token
    chunk_overlap=200,     # preserve context at boundaries
    separators=["\n\n", "\n", ". ", " "],  # try paragraph → sentence → word
)
chunks = splitter.split_documents(pages)

# Step 3: Embed & store
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = Chroma.from_documents(chunks, embeddings, persist_directory="./chroma_db")
```

**Why overlap?** Without it, a sentence split across two chunks loses context at the boundary. Overlap ensures every idea is fully represented in at least one chunk.

---

## 6. Embeddings & Vector Stores

**Q: What are embeddings and why are they central to RAG systems?**

**A:**
An embedding is a fixed-size float vector (e.g., 1536 dimensions for `text-embedding-3-small`) that captures the **semantic meaning** of text. Similar meanings produce vectors that are geometrically close (high cosine similarity).

In a RAG system:
1. **Index time**: embed all document chunks → store in a vector DB.
2. **Query time**: embed the user's question → find the K nearest chunks → inject as context.

```python
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

docs = ["Paris is the capital of France.", "Python is a programming language."]
vectors = embeddings.embed_documents(docs)

query = "What is the capital city of France?"
query_vec = embeddings.embed_query(query)

# Cosine similarity of query_vec to vectors[0] ≈ 0.92 (relevant)
# Cosine similarity of query_vec to vectors[1] ≈ 0.31 (irrelevant)
```

---

## 7. Memory

**Q: How does LangChain handle conversation memory? What are the trade-offs of different memory types?**

**A:**

| Memory Type | How it works | Use when |
|---|---|---|
| `ConversationBufferMemory` | Store all messages | Short conversations |
| `ConversationBufferWindowMemory` | Keep last K turns | Medium conversations |
| `ConversationSummaryMemory` | Summarise old turns | Long sessions, cost matters |
| `ConversationTokenBufferMemory` | Trim by token count | Precise context window management |

```python
from langchain.memory import ConversationBufferWindowMemory
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain

memory = ConversationBufferWindowMemory(k=5)  # keep last 5 turns
llm = ChatOpenAI(model="gpt-4o-mini")
chain = ConversationChain(llm=llm, memory=memory, verbose=True)

chain.predict(input="My name is Alice.")
chain.predict(input="What is RAG?")
response = chain.predict(input="What is my name?")
# LLM correctly recalls "Alice" from buffer
```

---

## 8. Tools & Agents

**Q: Explain the ReAct agent pattern. When should you use an agent vs. a fixed chain?**

**A:**
**ReAct (Reasoning + Acting)** is a prompting strategy where the LLM:
1. **Reasons** — writes a thought about what to do.
2. **Acts** — calls a tool with specific arguments.
3. **Observes** — receives the tool output.
4. Repeats until it has a final answer.

```python
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.tools import tool

@tool
def calculator(expression: str) -> str:
    """Evaluate a mathematical expression. Input: Python expression string."""
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Error: {e}"

@tool
def current_date(_: str) -> str:
    """Return today's date."""
    from datetime import date
    return str(date.today())

llm = ChatOpenAI(model="gpt-4o", temperature=0)
tools = [calculator, current_date]
agent = create_react_agent(llm, tools, prompt=...)
executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

executor.invoke({"input": "How many days until 2025-12-31?"})
```

**Use an agent** when the number or order of steps is unknown at design time.
**Use a fixed chain** when the steps are deterministic — agents add latency and cost.

---

## 9. Callbacks

**Q: How do LangChain callbacks work? Give a practical monitoring use case.**

**A:**
Callbacks hook into LangChain lifecycle events: `on_llm_start`, `on_llm_end`, `on_chain_start`, `on_tool_start`, etc.

```python
from langchain_core.callbacks import BaseCallbackHandler
from langchain_openai import ChatOpenAI
import time

class LatencyLogger(BaseCallbackHandler):
    def __init__(self):
        self._start = None

    def on_llm_start(self, serialized, prompts, **kwargs):
        self._start = time.perf_counter()
        print(f"LLM called with {len(prompts[0])} chars")

    def on_llm_end(self, response, **kwargs):
        elapsed = time.perf_counter() - self._start
        tokens = response.llm_output.get("token_usage", {})
        print(f"Completed in {elapsed:.2f}s | tokens: {tokens}")

llm = ChatOpenAI(model="gpt-4o-mini", callbacks=[LatencyLogger()])
llm.invoke("What is LangChain?")
```

Real-world uses: push metrics to Datadog, log to LangSmith, rate-limit token usage per user.
