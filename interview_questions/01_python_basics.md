# Python Basics — Interview Questions & Ideal Answers

---

## 1. Data Types & Variables

**Q: What is the difference between a list, tuple, and set in Python? When would you use each?**

**A:**
- **List** (`[]`): Ordered, mutable, allows duplicates. Use when you need a sequence that changes over time — e.g., a queue of tasks.
- **Tuple** (`()`): Ordered, immutable, allows duplicates. Use for fixed collections (coordinates, RGB values) or as dictionary keys since they are hashable.
- **Set** (`{}`): Unordered, mutable, no duplicates. Use for membership testing, deduplication, or set operations (union, intersection).

```python
tasks = ["fetch", "process", "store"]      # list — order matters, grows
point = (40.7128, -74.0060)               # tuple — fixed coordinates
seen_ids = {101, 102, 103}                # set — fast `in` checks
```

---

## 2. Strings

**Q: How do f-strings differ from `.format()` and `%` formatting? Which should you prefer and why?**

**A:**
- `%` formatting is legacy C-style; hard to read with many arguments.
- `.format()` is more readable but verbose.
- **f-strings** (Python 3.6+) are the fastest at runtime, most readable, and support arbitrary expressions inline.

```python
name, score = "Alice", 98.5
# Legacy
print("Name: %s, Score: %.1f" % (name, score))
# .format()
print("Name: {}, Score: {:.1f}".format(name, score))
# f-string (preferred)
print(f"Name: {name}, Score: {score:.1f}")
print(f"Pass: {score >= 90}")  # inline expression
```

Prefer f-strings unless targeting Python < 3.6.

---

## 3. Functions & Scope

**Q: Explain `*args` and `**kwargs`. Give a real-world use case.**

**A:**
- `*args` collects positional arguments into a tuple.
- `**kwargs` collects keyword arguments into a dict.

Real-world use case — a logging utility that wraps any function call:

```python
def log_call(func, *args, **kwargs):
    print(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
    result = func(*args, **kwargs)
    print(f"Result: {result}")
    return result

log_call(max, 3, 7, 1)
log_call(sorted, [3, 1, 2], reverse=True)
```

---

## 4. List Comprehensions

**Q: Rewrite this loop as a list comprehension, then explain when NOT to use one.**

```python
result = []
for x in range(20):
    if x % 2 == 0:
        result.append(x ** 2)
```

**A:**
```python
result = [x ** 2 for x in range(20) if x % 2 == 0]
```

Avoid comprehensions when:
- The logic is complex enough that clarity suffers (nested 3+ levels deep).
- You only need the side effects (e.g., printing); use a regular loop.
- The collection is huge — prefer a **generator expression** `(x**2 for ...)` to avoid building the entire list in memory.

---

## 5. Exception Handling

**Q: What is the difference between `except Exception` and a bare `except:`? Why does it matter in production code?**

**A:**
- `except Exception` catches all exceptions that inherit from `Exception`, which covers most runtime errors.
- Bare `except:` also catches `BaseException` subclasses like `SystemExit`, `KeyboardInterrupt`, and `GeneratorExit` — signals that are meant to terminate the program.

In production, bare `except:` is dangerous because it can swallow a `KeyboardInterrupt` (Ctrl+C) or a `SystemExit` from `sys.exit()`, making the process unresponsive.

```python
# Bad — swallows Ctrl+C
try:
    run_pipeline()
except:
    pass

# Good — only catch what you expect
try:
    run_pipeline()
except (ValueError, IOError) as e:
    logger.error(f"Pipeline failed: {e}")
finally:
    cleanup()
```

---

## 6. OOP

**Q: Explain the difference between `@classmethod`, `@staticmethod`, and an instance method. When would you use each?**

**A:**
- **Instance method**: receives `self`; operates on instance state. Most methods are instance methods.
- **`@classmethod`**: receives `cls`; can access/modify class-level state. Commonly used as alternative constructors.
- **`@staticmethod`**: receives neither `self` nor `cls`; a plain utility function that lives in the class namespace for organisational clarity.

```python
class User:
    _count = 0

    def __init__(self, name):
        self.name = name
        User._count += 1

    def greet(self):                        # instance method
        return f"Hello, {self.name}"

    @classmethod
    def from_dict(cls, data: dict):         # alternative constructor
        return cls(data["name"])

    @staticmethod
    def validate_name(name: str) -> bool:  # pure utility
        return len(name) >= 2
```

---

## 7. Decorators

**Q: Write a decorator that measures and logs the execution time of any function.**

**A:**
```python
import time
import functools

def timer(func):
    @functools.wraps(func)   # preserves __name__, __doc__
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper

@timer
def fetch_data(url):
    time.sleep(0.5)
    return {"data": "..."}

fetch_data("https://api.example.com/items")
# fetch_data took 0.5002s
```

Key detail: `@functools.wraps(func)` is essential — without it, introspection tools and logging lose the original function name.

---

## 8. File Handling

**Q: What is the advantage of using a `with` statement when working with files? What happens if you don't?**

**A:**
The `with` statement uses the context manager protocol (`__enter__`/`__exit__`). It guarantees the file is closed even if an exception is raised inside the block.

Without `with`, if an exception occurs between `open()` and `file.close()`, the file descriptor leaks. Under high load, this exhausts the OS file-descriptor limit.

```python
# Risky
f = open("data.txt")
data = f.read()   # if this raises, f.close() never runs
f.close()

# Safe
with open("data.txt", encoding="utf-8") as f:
    data = f.read()
# file is guaranteed closed here
```

---

## 9. Collections Module

**Q: When would you use `collections.defaultdict` over a regular dict?**

**A:**
Use `defaultdict` when you need to group items and want to avoid explicit `if key not in d` checks.

```python
from collections import defaultdict

# Grouping words by first letter
words = ["apple", "avocado", "banana", "blueberry", "cherry"]
grouped = defaultdict(list)
for word in words:
    grouped[word[0]].append(word)

# {'a': ['apple', 'avocado'], 'b': ['banana', 'blueberry'], 'c': ['cherry']}
```

`Counter` is another powerful collection for frequency counting:

```python
from collections import Counter
text = "the quick brown fox jumps over the lazy dog"
freq = Counter(text.split())
print(freq.most_common(3))  # [('the', 2), ('quick', 1), ...]
```

---

## 10. Generators & Memory Efficiency

**Q: What is the difference between a generator and a list? Demonstrate with an example relevant to processing large files.**

**A:**
A list materialises all elements in memory. A generator yields one item at a time, using O(1) memory regardless of dataset size.

```python
# List — loads entire file into memory
def read_logs_list(path):
    with open(path) as f:
        return [line.strip() for line in f]

# Generator — streams one line at a time
def read_logs_gen(path):
    with open(path) as f:
        for line in f:
            yield line.strip()

# Safe to use on a 10GB log file
for log_line in read_logs_gen("server.log"):
    if "ERROR" in log_line:
        alert(log_line)
```

Generators are essential in GenAI pipelines where LLM output streams token by token.
