# 📚 HTTPX Tutorial for Gen AI Developers - File Index

## 🎯 Start Here!

**New to httpx?** → Read `SUMMARY.md` first for an overview  
**Want quick reference?** → Check `CHEATSHEET.md`  
**Ready to code?** → Run `setup.sh` then start with `01_httpx-basics.py`

---

## 📖 Documentation Files

### 1. **SUMMARY.md** ⭐ START HERE
- **What it is:** Complete overview of the entire tutorial
- **Read this if:** You're new and want to understand what you'll learn
- **Time:** 10 minutes
- **Contains:** Learning path, key concepts, quick start guide

### 2. **README.md**
- **What it is:** Comprehensive guide with installation and best practices
- **Read this if:** You want detailed explanations and setup instructions
- **Time:** 20 minutes
- **Contains:** Installation, concepts, best practices, troubleshooting

### 3. **CHEATSHEET.md** ⭐ BOOKMARK THIS
- **What it is:** Quick reference for common patterns
- **Read this if:** You need to quickly look up syntax
- **Time:** 5 minutes (reference)
- **Contains:** Code snippets, common patterns, quick tips

### 4. **INDEX.md** (this file)
- **What it is:** Navigation guide for all files
- **Read this if:** You're not sure which file to use

---

## 🐍 Python Tutorial Files

### Level 1: Fundamentals

#### **01_httpx-basics.py** ⭐ START HERE FOR CODE
- **Difficulty:** Beginner
- **Time:** 15-20 minutes
- **Prerequisites:** Basic Python knowledge
- **What you'll learn:**
  - GET and POST requests
  - Headers and authentication
  - Query parameters
  - Timeout handling
  - Error handling
  - Client configuration
  - Response methods
- **Run it:** `python 01_httpx-basics.py`
- **Key takeaway:** httpx syntax is similar to requests!

---

### Level 2: Async Programming

#### **04_httpx-async.py**
- **Difficulty:** Intermediate
- **Time:** 20-25 minutes
- **Prerequisites:** Complete 01_httpx-basics.py
- **What you'll learn:**
  - Basic async requests
  - Concurrent API calls (5-10x faster!)
  - Error handling in async
  - Rate limiting with semaphores
  - Multiple LLM calls simultaneously
  - Async client configuration
- **Run it:** `python 04_httpx-async.py`
- **Key takeaway:** Async makes Gen AI apps much faster!

---

### Level 3: Streaming

#### **05_httpx-streaming.py**
- **Difficulty:** Intermediate
- **Time:** 25-30 minutes
- **Prerequisites:** Complete 04_httpx-async.py
- **What you'll learn:**
  - Sync and async streaming
  - Server-Sent Events (SSE) parsing
  - OpenAI-style streaming patterns
  - Streaming POST requests
  - Custom streaming iterators
  - Error handling in streams
- **Run it:** `python 05_httpx-streaming.py`
- **Key takeaway:** Streaming is essential for good UX in LLM apps!

---

### Level 4: Real-World Integration

#### **06_httpx-openai.py**
- **Difficulty:** Intermediate-Advanced
- **Time:** 30-40 minutes
- **Prerequisites:** Complete previous tutorials, have OpenAI API key
- **What you'll learn:**
  - OpenAI chat completions
  - Streaming chat responses
  - Conversation history management
  - Function calling
  - Embeddings
  - Retry logic with exponential backoff
- **Setup:** `export OPENAI_API_KEY='your-key'`
- **Run it:** `python 06_httpx-openai.py`
- **Key takeaway:** Production-ready patterns for LLM APIs!

---

### Level 5: Comparison

#### **07_httpx-vs-requests.py**
- **Difficulty:** Beginner-Intermediate
- **Time:** 15-20 minutes
- **Prerequisites:** Familiarity with requests library (optional)
- **What you'll learn:**
  - httpx vs requests differences
  - Migration guide
  - When to use which
  - Performance comparisons
  - Side-by-side examples
- **Run it:** `python 07_httpx-vs-requests.py`
- **Key takeaway:** httpx is the modern choice for Gen AI!

---

### Level 6: Production Template

#### **08_complete-example.py** ⭐ PRODUCTION TEMPLATE
- **Difficulty:** Advanced
- **Time:** 40-60 minutes
- **Prerequisites:** Complete all previous tutorials
- **What you'll learn:**
  - Production-ready LLM client
  - Multi-provider support (OpenAI, Anthropic)
  - Chat session management
  - Batch processing
  - Complete error handling
  - Rate limiting
  - Retry logic
- **Run it:** `python 08_complete-example.py`
- **Key takeaway:** Use this as a template for your own projects!

---

## ⚙️ Configuration Files

### **requirements.txt**
- **What it is:** Python dependencies
- **Use it for:** `pip install -r requirements.txt`
- **Contains:** httpx, python-dotenv

### **setup.sh** ⭐ RUN THIS FIRST
- **What it is:** Automated setup script
- **Use it for:** Creating venv and installing dependencies
- **Run it:** `chmod +x setup.sh && ./setup.sh`
- **What it does:**
  1. Creates virtual environment
  2. Activates venv
  3. Installs dependencies
  4. Shows next steps

---

## 🗺️ Recommended Learning Paths

### Path 1: Complete Beginner (Total: 2-3 hours)
```
1. Read SUMMARY.md (10 min)
2. Run setup.sh (5 min)
3. Work through 01_httpx-basics.py (20 min)
4. Work through 04_httpx-async.py (25 min)
5. Work through 05_httpx-streaming.py (30 min)
6. Read CHEATSHEET.md (10 min)
7. Try 06_httpx-openai.py with your API key (40 min)
```

### Path 2: Experienced Developer (Total: 1-2 hours)
```
1. Skim SUMMARY.md (5 min)
2. Run setup.sh (5 min)
3. Skim 01_httpx-basics.py (10 min)
4. Focus on 04_httpx-async.py (15 min)
5. Focus on 05_httpx-streaming.py (20 min)
6. Study 08_complete-example.py (30 min)
7. Bookmark CHEATSHEET.md for reference
```

### Path 3: Quick Reference (Total: 15 min)
```
1. Run setup.sh (5 min)
2. Read CHEATSHEET.md (5 min)
3. Copy patterns from 08_complete-example.py (5 min)
```

### Path 4: Migrating from requests (Total: 1 hour)
```
1. Read 07_httpx-vs-requests.py (20 min)
2. Focus on 04_httpx-async.py (20 min)
3. Study 08_complete-example.py (20 min)
4. Use CHEATSHEET.md for reference
```

---

## 🎯 Quick Reference by Use Case

### "I need to make a simple API call"
→ See `01_httpx-basics.py` (examples 1-2)  
→ Or `CHEATSHEET.md` (Basic Requests section)

### "I need to call multiple LLM APIs concurrently"
→ See `04_httpx-async.py` (example 2)  
→ Or `08_complete-example.py` (BatchProcessor class)

### "I need to stream LLM responses"
→ See `05_httpx-streaming.py` (examples 3, 5)  
→ Or `06_httpx-openai.py` (example 2)  
→ Or `08_complete-example.py` (stream_complete method)

### "I need to manage conversation history"
→ See `06_httpx-openai.py` (example 4)  
→ Or `08_complete-example.py` (ChatSession class)

### "I need production-ready code"
→ Use `08_complete-example.py` as your template

### "I'm getting rate limited"
→ See `04_httpx-async.py` (example 6)  
→ Or `06_httpx-openai.py` (example 7)  
→ Or `08_complete-example.py` (retry logic in LLMClient)

### "I need to compare httpx vs requests"
→ See `07_httpx-vs-requests.py`

---

## 📊 File Complexity Matrix

| File | Difficulty | Time | Prerequisites | Best For |
|------|-----------|------|---------------|----------|
| SUMMARY.md | Easy | 10m | None | Overview |
| README.md | Easy | 20m | None | Setup guide |
| CHEATSHEET.md | Easy | 5m | None | Quick reference |
| 01_httpx-basics.py | Beginner | 20m | Basic Python | Learning fundamentals |
| 04_httpx-async.py | Intermediate | 25m | 01_httpx-basics.py | Learning async |
| 05_httpx-streaming.py | Intermediate | 30m | 04_httpx-async.py | Learning streaming |
| 06_httpx-openai.py | Intermediate | 40m | Previous files + API key | Real integration |
| 07_httpx-vs-requests.py | Beginner | 20m | Optional: requests knowledge | Comparison |
| 08_complete-example.py | Advanced | 60m | All previous files | Production template |

---

## 🚀 Quick Start Commands

```bash
# 1. Setup (first time only)
cd "/Users/vinod/Desktop/Desktop - Vinod's MacBook Air/Python for Gen AI/httpx_basics"
chmod +x setup.sh
./setup.sh

# 2. Activate environment (every time)
source venv/bin/activate

# 3. Run examples (in order)
python 01_httpx-basics.py
python 04_httpx-async.py
python 05_httpx-streaming.py

# 4. For OpenAI examples
export OPENAI_API_KEY='your-api-key-here'
python 06_httpx-openai.py

# 5. Production template
python 08_complete-example.py
```

---

## 💡 Tips for Success

1. **Follow the order:** Start with basics, move to async, then streaming
2. **Run the code:** Don't just read - execute and experiment
3. **Bookmark CHEATSHEET.md:** You'll reference it often
4. **Use 08_complete-example.py:** It's a production-ready template
5. **Practice async:** It's the most important concept for Gen AI

---

## 🆘 Troubleshooting

### "I can't run the setup script"
```bash
chmod +x setup.sh
./setup.sh
```

### "Import error: No module named 'httpx'"
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### "OpenAI examples fail"
```bash
export OPENAI_API_KEY='your-actual-api-key'
```

### "I'm confused about async"
→ Start with `01_httpx-basics.py` first  
→ Then carefully work through `04_httpx-async.py`  
→ The examples build on each other

---

## 📞 Next Steps

After completing this tutorial:

1. ✅ Build your own Gen AI application using `08_complete-example.py` as a template
2. ✅ Explore other LLM providers (Anthropic, Cohere, etc.)
3. ✅ Implement advanced features (caching, fallbacks, monitoring)
4. ✅ Share your learnings with others!

---

**Happy coding! 🎉**

*Last updated: January 2026*
