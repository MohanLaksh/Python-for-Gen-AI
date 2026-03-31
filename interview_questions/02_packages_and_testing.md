# Python Packages & Testing — Interview Questions & Ideal Answers

---

## 1. Package Structure

**Q: What is the purpose of `__init__.py`? What is the difference between an implicit namespace package and a regular package?**

**A:**
`__init__.py` marks a directory as a Python **regular package**. It runs when the package is first imported and is used to:
- Control what `from package import *` exports (via `__all__`).
- Provide a convenient public API by re-exporting symbols from sub-modules.
- Run package-level initialisation (e.g., configure logging).

```python
# calc/__init__.py
from .add import add
from .multiply import multiply
from .divide import divide
from .subtract import subtract

__all__ = ["add", "multiply", "divide", "subtract"]
```

An **implicit namespace package** (PEP 420, Python 3.3+) is a directory *without* `__init__.py`. Python still finds it, but it has no initialisation code and is used mainly for splitting large packages across multiple directories (namespace packages).

---

## 2. Unit Testing with pytest

**Q: What makes a good unit test? Write a test for a `divide(a, b)` function that covers edge cases.**

**A:**
A good unit test is:
- **Fast** — no I/O, no network.
- **Isolated** — tests one behaviour at a time.
- **Repeatable** — same result every run.
- **Clear** — the test name describes the scenario and expectation.

```python
# calc/divide.py
def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


# tests/test_divide.py
import pytest
from calc.divide import divide

def test_divide_positive_numbers():
    assert divide(10, 2) == 5.0

def test_divide_with_float():
    assert divide(7, 2) == pytest.approx(3.5)

def test_divide_by_zero_raises():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(10, 0)

def test_divide_negative_numerator():
    assert divide(-9, 3) == -3.0

def test_divide_both_negative():
    assert divide(-6, -2) == 3.0
```

---

## 3. Test Organisation

**Q: How do you organise tests in a larger project? What is the difference between `tests/` at the root vs. tests inside each package?**

**A:**
**Root-level `tests/`** (most common):
```
my_project/
├── calc/
│   ├── __init__.py
│   └── add.py
├── tests/
│   ├── __init__.py
│   └── test_add.py
└── pyproject.toml
```
- Clean separation between source and test code.
- pytest discovers tests automatically.
- Mirrors the source structure — easy navigation.

**Tests inside the package** (library-style):
```
calc/
├── __init__.py
├── add.py
└── tests/
    └── test_add.py
```
- Useful when tests are shipped with the package itself.

For most applications, use root-level `tests/` and mirror the package structure inside it.

---

## 4. pytest Fixtures

**Q: What is a pytest fixture and why is it better than `setUp/tearDown` from `unittest`?**

**A:**
A fixture is a reusable piece of test infrastructure declared with `@pytest.fixture`. It is injected by name into test functions.

Advantages over `setUp/tearDown`:
- **Composable** — fixtures can use other fixtures.
- **Scoped** — `function`, `class`, `module`, or `session` lifetime.
- **Explicit** — you see exactly which test uses which fixture.

```python
import pytest
from calc import add, divide

@pytest.fixture
def sample_numbers():
    return {"a": 10, "b": 5}

def test_add(sample_numbers):
    assert add(sample_numbers["a"], sample_numbers["b"]) == 15

def test_divide(sample_numbers):
    assert divide(sample_numbers["a"], sample_numbers["b"]) == 2.0
```

A session-scoped fixture (e.g., a database connection) is created once for the entire test run, saving setup time.

---

## 5. Mocking

**Q: When and how would you mock an external API call in a unit test?**

**A:**
Mock external calls when:
- They are slow (network latency).
- They have side effects (sending emails, charging cards).
- They are non-deterministic (changing live data).

```python
from unittest.mock import patch, MagicMock
from my_app.weather import get_temperature

def test_get_temperature_returns_celsius():
    mock_response = MagicMock()
    mock_response.json.return_value = {"main": {"temp": 295.15}}
    mock_response.status_code = 200

    with patch("my_app.weather.requests.get", return_value=mock_response):
        temp = get_temperature("London")

    assert temp == pytest.approx(22.0, abs=0.1)  # 295.15 K → 22°C
```

---

## 6. Code Coverage

**Q: What does code coverage measure? Is 100% coverage a good goal?**

**A:**
Code coverage measures what **percentage of lines/branches** are executed during tests. Run with:

```bash
pytest --cov=calc --cov-report=term-missing
```

**100% coverage is not a good goal in isolation** because:
- It proves code was *executed*, not that it works correctly.
- Chasing 100% leads to trivial tests that inflate the number.
- Integration and edge-case bugs can exist in 100%-covered code.

A pragmatic target is **80–90%** for business logic, with coverage reports used to spot *untested critical paths*, not as a KPI.

---

## 7. Package Distribution

**Q: What is `pyproject.toml` and why has it replaced `setup.py`?**

**A:**
`pyproject.toml` (PEP 517/518) is the modern, standardised way to declare a Python project's build system and metadata. It replaces `setup.py` + `setup.cfg` with a single declarative file.

```toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.backends.legacy:build"

[project]
name = "my-calc"
version = "1.0.0"
description = "A simple calculator package"
requires-python = ">=3.10"
dependencies = ["pydantic>=2.0"]

[project.optional-dependencies]
dev = ["pytest", "pytest-cov"]
```

Benefits:
- Tool-agnostic (works with setuptools, poetry, hatch).
- No executable code during install (security improvement).
- Single source of truth for build config, dependencies, and tool settings.
