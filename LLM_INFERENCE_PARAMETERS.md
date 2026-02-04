# LLM Inference Parameters – A Complete Practical Guide

**Audience:** Beginners → Intermediate GenAI Developers  
**Goal:** Understand how inference parameters control LLM behavior  
**Applies to:** OpenAI, Claude, Gemini, LLaMA, Mistral, local LLMs (LM Studio, Ollama)

---

## 1. What Are Inference Parameters?

Inference parameters control **how a Large Language Model generates text**.

Think of an LLM as:
- Having **knowledge** (trained data)
- But inference parameters decide **how it speaks, thinks, and behaves**

> Same prompt + different parameters = very different outputs

---

## 2. Temperature

### What it controls
- **Creativity vs predictability**
- Randomness in token selection

### Range
- `0.0` → Deterministic
- `1.0` → Balanced
- `>1.0` → Very creative (can be chaotic)

---

### Example Prompt
```

Explain recursion in simple terms.

```

### Temperature = 0.0
```

Recursion is a programming technique where a function calls itself to solve a problem.

```

✔ Very factual  
❌ Boring  
✔ Best for: **QA, legal, medical, summaries**

---

### Temperature = 0.7
```

Recursion is like looking into two mirrors facing each other.
A function solves a problem by calling a smaller version of itself.

```

✔ Balanced  
✔ Best for: **teaching, explanations**

---

### Temperature = 1.2
```

Imagine a snake eating its own tail—recursion is a function looping into itself
until the problem disappears!

```

✔ Creative  
❌ Risky for accuracy  
✔ Best for: **storytelling, brainstorming**

---

## 3. Top-P (Nucleus Sampling)

### What it controls
- Chooses tokens from the **top probability mass**
- Alternative to temperature

### Range
- `0.1` → Very safe
- `0.9` → Balanced
- `1.0` → Everything allowed

---

### Prompt
```

Give an analogy for APIs.

```

### Top-P = 0.2
```

An API is a messenger that delivers requests and responses between systems.

```

✔ Safe  
❌ Limited variety

---

### Top-P = 0.9
```

An API is like a waiter in a restaurant, taking your order to the kitchen
and bringing food back to your table.

```

✔ Natural  
✔ Common default

---

### Important Rule
> **Use either Temperature OR Top-P, not both aggressively**

---

## 4. Max Tokens

### What it controls
- Maximum length of output

### Prompt
```

Explain LLM inference.

```

### Max Tokens = 30
```

LLM inference is the process of generating responses from a trained language model.

```

❌ Incomplete

---

### Max Tokens = 300
```

LLM inference is the process where a trained language model predicts
the next token repeatedly to generate meaningful text...

```

✔ Detailed  
✔ Best for explanations

---

## 5. Stop Sequences

### What it controls
- Where the model **must stop generating**

### Example
```

Stop sequence: ["###"]

```

### Prompt
```

Explain REST APIs.

### END

```

### Output
```

REST APIs allow systems to communicate over HTTP using standard methods.

```

✔ Useful for:
- Structured outputs
- Preventing hallucinations
- Tool calling

---

## 6. Frequency Penalty

### What it controls
- Penalizes repeated tokens
- Reduces looping

### Range
- `0.0` → No penalty
- `1.0` → Strong penalty

---

### Prompt
```

Explain AI in one paragraph.

```

### Frequency Penalty = 0.0
```

AI is a field of computer science. AI systems use data.
AI helps automate tasks. AI improves efficiency.

```

❌ Repetitive

---

### Frequency Penalty = 0.8
```

Artificial Intelligence focuses on building systems that can learn,
reason, and assist humans in solving complex problems efficiently.

```

✔ Cleaner  
✔ Recommended for long answers

---

## 7. Presence Penalty

### What it controls
- Encourages **new topics**
- Avoids sticking to the same idea

### Range
- `0.0` → Stay focused
- `1.0` → Explore new ideas

---

### Prompt
```

Talk about Python.

```

### Presence Penalty = 0.0
```

Python is a programming language. Python is easy to learn.
Python is widely used.

```

---

### Presence Penalty = 1.0
```

Python is popular in web development, data science, automation,
AI research, DevOps, and education.

```

✔ Broader coverage

---

## 8. Top-K (Mostly for Open-Source Models)

### What it controls
- Limits token selection to top **K most probable tokens**

### Example
- `Top-K = 10` → Very safe
- `Top-K = 50` → Creative

---

### Prompt
```

Describe the future of AI.

```

### Top-K = 10
```

AI will continue improving efficiency and automation across industries.

```

---

### Top-K = 50
```

AI may redefine creativity, reshape jobs, influence ethics,
and blur the line between human and machine intelligence.

```

---

## 9. Repetition Penalty (Local Models)

### What it controls
- Prevents repeating phrases exactly

### Common in:
- LLaMA
- Mistral
- Ollama
- LM Studio

---

### Recommended Values
- `1.0` → Default
- `1.1 – 1.2` → Safer for long text

---

## 10. Seed (Deterministic Output)

### What it controls
- Reproducibility

### Same Prompt + Same Seed = Same Output

✔ Useful for:
- Testing
- Debugging
- Demos

---

## 11. Typical Parameter Presets

### 🔹 Chatbot (Balanced)
```

temperature: 0.7
top_p: 0.9
max_tokens: 300
frequency_penalty: 0.5
presence_penalty: 0.3

```

---

### 🔹 QA / Legal / Medical
```

temperature: 0.0
top_p: 0.1
max_tokens: 200
frequency_penalty: 0.0
presence_penalty: 0.0

```

---

### 🔹 Creative Writing
```

temperature: 1.0
top_p: 0.95
max_tokens: 500
frequency_penalty: 0.7
presence_penalty: 0.8

```

---

## 12. Key Mental Model

> **Prompt defines WHAT to say**  
> **Inference parameters define HOW to say it**

---

## 13. Common Mistakes

❌ Using high temperature for factual tasks  
❌ Very low max_tokens for explanations  
❌ No stop sequences for structured output  
❌ Expecting parameters to fix bad prompts  

---

## 14. Final Tip for Engineers

> Start with **good prompts**, then fine-tune **parameters last**

Parameters **polish behavior**, they do not replace **prompt quality**.

---

## 15. Next Steps

- Try same prompt with different parameters
- Build a small playground UI
- Log outputs for comparison

---