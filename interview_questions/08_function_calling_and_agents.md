# Function Calling & AI Agents — Interview Questions & Ideal Answers

---

## 1. Function Calling Basics

**Q: What is function calling (tool use) in LLMs and how does it work at the API level?**

**A:**
Function calling allows an LLM to decide when and how to invoke external tools (functions, APIs, databases) by returning a structured JSON object instead of free-form text.

**Flow:**
1. Developer describes available tools in the API request (name, description, JSON schema of parameters).
2. LLM analyses the user query and outputs a `tool_call` JSON if a tool is needed.
3. Developer executes the actual function and sends the result back.
4. LLM uses the result to compose a natural language response.

```python
import json
from openai import OpenAI

client = OpenAI()

tools = [{
    "type": "function",
    "function": {
        "name": "get_stock_price",
        "description": "Get the current stock price for a given ticker symbol",
        "parameters": {
            "type": "object",
            "properties": {
                "ticker": {"type": "string", "description": "Stock ticker, e.g. AAPL"},
                "currency": {"type": "string", "enum": ["USD", "EUR", "GBP"], "default": "USD"},
            },
            "required": ["ticker"],
        },
    },
}]

messages = [{"role": "user", "content": "What is Apple's stock price?"}]

response = client.chat.completions.create(
    model="gpt-4o-mini", messages=messages, tools=tools, tool_choice="auto"
)

tool_call = response.choices[0].message.tool_calls[0]
args = json.loads(tool_call.function.arguments)
# args = {"ticker": "AAPL", "currency": "USD"}

# Execute the actual function
price = get_stock_price(**args)   # your real implementation

# Send result back to the model
messages.append(response.choices[0].message)
messages.append({
    "role": "tool",
    "tool_call_id": tool_call.id,
    "content": json.dumps({"price": price, "currency": "USD"}),
})

final = client.chat.completions.create(model="gpt-4o-mini", messages=messages, tools=tools)
print(final.choices[0].message.content)
# "Apple's current stock price is $195.23 USD."
```

---

## 2. Tool Design

**Q: What makes a good tool description for an LLM? What happens if descriptions are poor?**

**A:**
The LLM selects tools based solely on the **description** — it cannot run the code. Poor descriptions cause:
- Wrong tool selected for the query.
- Incorrect parameter values.
- Tool called when it shouldn't be (or vice versa).

**Good tool description principles:**
1. **Be specific about what the tool returns**, not just what it does.
2. **Describe input constraints** (format, units, valid values).
3. **Give examples** in the description for ambiguous parameters.
4. **Name parameters intuitively** (`city_name` not `c`).

```python
# Bad
{"name": "weather", "description": "Weather function", "parameters": {"q": {"type": "string"}}}

# Good
{
    "name": "get_current_weather",
    "description": "Returns current weather conditions for a city. Use when the user asks about weather, temperature, or climate in a specific location. Returns temperature in Celsius, humidity percentage, and a condition description.",
    "parameters": {
        "type": "object",
        "properties": {
            "city_name": {
                "type": "string",
                "description": "City name with optional country code. Examples: 'London', 'Paris, FR', 'New York, US'"
            },
            "units": {
                "type": "string",
                "enum": ["celsius", "fahrenheit"],
                "description": "Temperature unit. Default: celsius"
            }
        },
        "required": ["city_name"]
    }
}
```

---

## 3. Multi-Tool Agents

**Q: Design an agent that can answer questions about a company's data by calling different tools.**

**A:**
```python
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

@tool
def query_sales_db(sql: str) -> str:
    """Execute a read-only SQL query against the sales database.
    Use for questions about revenue, orders, and customers.
    Only SELECT queries are allowed."""
    # In production: validate SQL, execute against DB
    return f"Query result for: {sql}"

@tool
def search_knowledge_base(query: str) -> str:
    """Search the internal knowledge base for product documentation,
    policies, and procedures. Use for how-to questions and policy lookups."""
    # In production: call your RAG retriever
    return f"KB results for: {query}"

@tool
def get_live_metrics(metric_name: str) -> str:
    """Fetch a live business metric by name.
    Available: daily_revenue, active_users, conversion_rate, nps_score."""
    metrics = {
        "daily_revenue": "$42,310",
        "active_users": "1,247",
        "conversion_rate": "3.2%",
        "nps_score": "72",
    }
    return metrics.get(metric_name, f"Unknown metric: {metric_name}")

llm = ChatOpenAI(model="gpt-4o", temperature=0)
tools = [query_sales_db, search_knowledge_base, get_live_metrics]

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a business intelligence assistant. Use tools to answer questions accurately."),
    MessagesPlaceholder("chat_history", optional=True),
    ("human", "{input}"),
    MessagesPlaceholder("agent_scratchpad"),
])

agent = create_tool_calling_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools, verbose=True, max_iterations=5)

executor.invoke({"input": "What is today's conversion rate and how does our refund policy work?"})
```

---

## 4. Parallel Tool Calling

**Q: What is parallel tool calling and when is it useful?**

**A:**
Modern LLMs (GPT-4o, Claude 3.5) can call multiple tools **simultaneously** in a single response when the calls are independent. This reduces latency from N sequential round-trips to 1.

```python
# The LLM returns multiple tool_calls in one response:
# tool_call 1: get_weather(city="London")
# tool_call 2: get_weather(city="Paris")
# tool_call 3: get_exchange_rate(from="GBP", to="EUR")

for tool_call in response.choices[0].message.tool_calls:
    result = dispatch_tool(tool_call)
    messages.append({
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": json.dumps(result),
    })
```

**Use case**: a travel planning assistant asked "Plan a trip from London to Paris next week" — weather for both cities and exchange rates can be fetched in parallel.

---

## 5. Agent Patterns

**Q: Compare ReAct, Plan-and-Execute, and Reflection agent patterns. When would you use each?**

**A:**

| Pattern | How it works | Best for |
|---|---|---|
| **ReAct** | Interleave thought → act → observe in a single LLM call loop | General tasks; straightforward tool use |
| **Plan-and-Execute** | First plan all steps, then execute sequentially | Complex multi-step tasks; when planning ahead matters |
| **Reflection / Critic** | A second LLM reviews the first one's output and suggests improvements | High-quality writing, code generation, reasoning |

```python
# Plan-and-Execute pattern
planner_prompt = "Break this task into numbered steps: {task}"
executor_prompt = "Execute step {step_num}: {step_description}. Prior results: {results}"

# Step 1: Generate plan
plan = planner_llm.invoke({"task": "Research and summarise the top 3 AI papers from 2024"})

# Step 2: Execute each step
results = []
for step in parse_plan(plan):
    result = executor_llm.invoke({"step_num": step.num, "step_description": step.text, "results": results})
    results.append(result)
```

---

## 6. Safety & Guardrails

**Q: What are the risks of giving an LLM agent access to tools and how do you mitigate them?**

**A:**

**Risks:**
1. **Prompt injection** — malicious text in retrieved content hijacks the agent's actions.
2. **Unintended side effects** — agent deletes data, sends emails, charges cards.
3. **Infinite loops** — agent gets stuck calling tools repeatedly.
4. **Data exfiltration** — sensitive data leaked via tool outputs.
5. **Scope creep** — agent takes actions beyond the user's intent.

**Mitigations:**
```python
# 1. Limit tool permissions — read-only by default
@tool
def query_database(sql: str) -> str:
    """Only SELECT statements allowed."""
    if not sql.strip().upper().startswith("SELECT"):
        raise ValueError("Only read queries are permitted")
    return execute_query(sql)

# 2. Human-in-the-loop for destructive actions
@tool
def send_email(to: str, subject: str, body: str) -> str:
    """Send an email. Requires human approval."""
    approval = get_human_approval(f"Send email to {to}?")
    if not approval:
        return "Email sending cancelled by user."
    return actually_send_email(to, subject, body)

# 3. Max iterations guard
executor = AgentExecutor(
    agent=agent,
    tools=tools,
    max_iterations=10,       # prevent infinite loops
    max_execution_time=30,   # timeout in seconds
)
```

---

## 7. Structured Output from Agents

**Q: How do you ensure an agent always returns a structured response (not free text)?**

**A:**
Use `with_structured_output()` on the LLM, or a final formatting step in the chain:

```python
from pydantic import BaseModel
from langchain_openai import ChatOpenAI

class ResearchReport(BaseModel):
    summary: str
    key_findings: list[str]
    confidence_score: float
    sources: list[str]

llm = ChatOpenAI(model="gpt-4o")
structured_llm = llm.with_structured_output(ResearchReport)

# The LLM is constrained to return a JSON matching ResearchReport
report: ResearchReport = structured_llm.invoke(
    "Summarise the key findings from the documents: ..."
)
print(report.confidence_score)  # 0.87
```
