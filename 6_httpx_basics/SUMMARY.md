# HTTPX for Gen AI - Complete Tutorial Summary

## 📦 What You've Got

A comprehensive httpx tutorial specifically designed for Gen AI developers, with **6 Python files**, **3 documentation files**, and **1 setup script**.

---

## 📁 File Structure

```
httpx_basics/
├── 📘 Documentation
│   ├── README.md              # Complete guide & getting started
│   ├── CHEATSHEET.md          # Quick reference for common patterns
│   └── SUMMARY.md             # This file
│
├── 🐍 Python Examples
│   ├── 01_httpx-basics.py        # Fundamentals (GET, POST, headers, etc.)
│   ├── 04_httpx-async.py         # Async/await patterns
│   ├── 05_httpx-streaming.py     # Streaming responses (LLM APIs)
│   ├── 06_httpx-openai.py        # OpenAI API integration
│   └── 07_httpx-vs-requests.py   # Comparison with requests library
│
├── ⚙️ Configuration
│   ├── requirements.txt       # Python dependencies
│   └── setup.sh              # Automated setup script
│
└── 📦 Virtual Environment (create this)
    └── venv/                  # Run setup.sh to create
```

---

## 🚀 Quick Start (3 Steps)

### Step 1: Setup Environment
```bash
cd "/Users/vinod/Desktop/Desktop - Vinod's MacBook Air/Python for Gen AI/httpx_basics"

# Option A: Use the setup script (recommended)
chmod +x setup.sh
./setup.sh

# Option B: Manual setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 2: Run Examples
```bash
# Activate virtual environment (if not already active)
source venv/bin/activate

# Run the examples in order
python 01_httpx-basics.py        # Start here
python 04_httpx-async.py         # Learn async patterns
python 05_httpx-streaming.py     # Master streaming
python 07_httpx-vs-requests.py   # See the differences
```

### Step 3: Try OpenAI Integration
```bash
# Set your API key
export OPENAI_API_KEY='your-api-key-here'

# Run OpenAI examples
python 06_httpx-openai.py
```

---

## 📚 Learning Path

### Level 1: Basics (01_httpx-basics.py)
**Time: 15-20 minutes**

Learn:
- ✅ GET and POST requests
- ✅ Headers and authentication
- ✅ Query parameters
- ✅ Timeout handling
- ✅ Error handling
- ✅ Client configuration

**Key Takeaway:** httpx syntax is very similar to requests!

---

### Level 2: Async (04_httpx-async.py)
**Time: 20-25 minutes**

Learn:
- ✅ Basic async requests
- ✅ Concurrent API calls (huge performance boost!)
- ✅ Error handling in async
- ✅ Rate limiting with semaphores
- ✅ Multiple LLM calls simultaneously

**Key Takeaway:** Async makes Gen AI apps 5-10x faster!

---

### Level 3: Streaming (05_httpx-streaming.py)
**Time: 25-30 minutes**

Learn:
- ✅ Sync and async streaming
- ✅ Server-Sent Events (SSE) parsing
- ✅ OpenAI-style streaming patterns
- ✅ Streaming POST requests
- ✅ Custom streaming iterators

**Key Takeaway:** Streaming is essential for good UX in LLM apps!

---

### Level 4: Real-World (06_httpx-openai.py)
**Time: 30-40 minutes**

Learn:
- ✅ OpenAI chat completions
- ✅ Streaming chat responses
- ✅ Conversation history management
- ✅ Function calling
- ✅ Embeddings
- ✅ Retry logic with exponential backoff

**Key Takeaway:** Production-ready patterns for LLM APIs!

---

### Level 5: Comparison (07_httpx-vs-requests.py)
**Time: 15-20 minutes**

Learn:
- ✅ httpx vs requests differences
- ✅ Migration guide
- ✅ When to use which
- ✅ Performance comparisons

**Key Takeaway:** httpx is the modern choice for Gen AI!

---

## 🎯 Key Concepts

### 1. Why httpx for Gen AI?

```python
# ❌ requests - Sequential (slow)
for prompt in prompts:
    response = requests.post(api_url, json={"prompt": prompt})
    # Wait... wait... wait...

# ✅ httpx - Concurrent (fast!)
async with httpx.AsyncClient() as client:
    tasks = [client.post(api_url, json={"prompt": p}) for p in prompts]
    responses = await asyncio.gather(*tasks)
    # All run at the same time! 🚀
```

### 2. Streaming for Better UX

```python
# ❌ Without streaming - user waits
response = await client.post(url, json=payload)
print(response.json()['content'])  # Shows all at once

# ✅ With streaming - immediate feedback
async with client.stream('POST', url, json=payload) as response:
    async for chunk in response.aiter_lines():
        print(chunk, end='', flush=True)  # Shows word-by-word
```

### 3. Proper Error Handling

```python
try:
    response = await client.post(url, json=payload)
    response.raise_for_status()
    
except httpx.HTTPStatusError as e:
    if e.response.status_code == 429:  # Rate limit
        await asyncio.sleep(2)  # Wait and retry
    else:
        print(f"Error: {e.response.status_code}")
        
except httpx.TimeoutException:
    print("Request timed out")
```

---

## 💡 Best Practices

### ✅ DO:
1. **Use async for Gen AI apps** - Concurrent API calls are crucial
2. **Set appropriate timeouts** - LLM responses can take 30-60+ seconds
3. **Implement streaming** - Better user experience
4. **Handle rate limits** - Use exponential backoff
5. **Reuse clients** - Connection pooling improves performance
6. **Manage conversation history** - Track messages for context

### ❌ DON'T:
1. **Don't use sync for multiple API calls** - Too slow
2. **Don't forget timeouts** - Your app will hang
3. **Don't ignore errors** - Handle rate limits and failures
4. **Don't create new clients repeatedly** - Inefficient
5. **Don't hardcode API keys** - Use environment variables
6. **Don't skip streaming** - Users want immediate feedback

---

## 🔧 Common Patterns

### Pattern 1: Basic LLM Call
```python
async def call_llm(prompt: str) -> str:
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            'https://api.openai.com/v1/chat/completions',
            headers={'Authorization': f'Bearer {api_key}'},
            json={
                'model': 'gpt-4',
                'messages': [{'role': 'user', 'content': prompt}]
            }
        )
        return response.json()['choices'][0]['message']['content']
```

### Pattern 2: Streaming LLM Response
```python
async def stream_llm(prompt: str):
    async with httpx.AsyncClient(timeout=60.0) as client:
        async with client.stream('POST', url, json=payload) as response:
            async for line in response.aiter_lines():
                if line.startswith('data: '):
                    data = json.loads(line[6:])
                    if content := data['choices'][0]['delta'].get('content'):
                        yield content
```

### Pattern 3: Concurrent Processing
```python
async def process_batch(prompts: list[str]) -> list[str]:
    async with httpx.AsyncClient() as client:
        tasks = [call_llm(client, p) for p in prompts]
        return await asyncio.gather(*tasks)
```

### Pattern 4: Retry with Backoff
```python
async def call_with_retry(url, payload, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:
                await asyncio.sleep(2 ** attempt)
            else:
                raise
```

---

## 📊 Performance Comparison

### Sequential vs Concurrent (5 API calls)

| Method | Time | Speedup |
|--------|------|---------|
| requests (sequential) | ~15s | 1x |
| httpx (sequential) | ~15s | 1x |
| httpx (concurrent) | ~3s | **5x faster!** |

### Why Async Matters for Gen AI

```
Sequential (requests):
[====] [====] [====] [====] [====]  ← 15 seconds
 API1   API2   API3   API4   API5

Concurrent (httpx async):
[====]
[====]
[====]  ← 3 seconds (all run together!)
[====]
[====]
```

---

## 🎓 What You'll Learn

After completing this tutorial, you'll be able to:

✅ Make HTTP requests with httpx (sync and async)  
✅ Handle streaming responses from LLM APIs  
✅ Implement concurrent API calls for better performance  
✅ Manage conversation history in chatbots  
✅ Handle errors and rate limits gracefully  
✅ Use OpenAI, Anthropic, and other Gen AI APIs  
✅ Build production-ready Gen AI applications  

---

## 🔗 Resources

### Documentation
- [httpx Official Docs](https://www.python-httpx.org/)
- [OpenAI API Docs](https://platform.openai.com/docs/api-reference)
- [Python asyncio Docs](https://docs.python.org/3/library/asyncio.html)

### Quick References
- `README.md` - Complete guide
- `CHEATSHEET.md` - Quick reference
- `SUMMARY.md` - This file

---

## 🎯 Next Steps

1. ✅ Run `setup.sh` to create your environment
2. ✅ Work through the examples in order
3. ✅ Read the CHEATSHEET.md for quick reference
4. ✅ Try the OpenAI examples with your API key
5. 🚀 Build your own Gen AI application!

---

## 💬 Common Questions

### Q: Should I use httpx or requests?
**A:** For Gen AI apps, use httpx! The async support is crucial for performance.

### Q: Do I need to learn async/await?
**A:** Yes! It's essential for modern Gen AI development. The examples will teach you.

### Q: Can I use httpx with other LLM APIs?
**A:** Absolutely! The patterns work with OpenAI, Anthropic, Cohere, etc.

### Q: What about rate limits?
**A:** The examples show retry logic with exponential backoff - production ready!

### Q: Is streaming really necessary?
**A:** For good UX, yes! Users want to see responses as they're generated.

---

## 🎉 You're Ready!

You now have everything you need to build powerful Gen AI applications with httpx. Start with `01_httpx-basics.py` and work your way through the examples.

**Happy coding! 🚀**

---

*Last updated: January 2026*
