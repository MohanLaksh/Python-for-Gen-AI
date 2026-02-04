# Streamlit – Complete Practical Guide

> Build data apps, dashboards, and AI tools using **pure Python** with minimal effort.

---

## Table of Contents

1. What is Streamlit?
2. When & Why Use Streamlit
3. Installation & Setup
4. Streamlit App Structure
5. Running a Streamlit App
6. Core Concepts

   * Script Rerun Model
   * State & Reactivity
7. Layout & Page Structure
8. Display Elements
9. Input Widgets
10. Data Display Components
11. Charts & Visualization
12. Forms
13. Session State
14. Caching & Performance
15. File Uploads & Downloads
16. Sidebar & Multipage Apps
17. Configuration & Theming
18. Deployment Options
19. Streamlit for AI / LLM Apps
20. Best Practices
21. Common Pitfalls
22. Mini Project Ideas

---

## 1️⃣ What is Streamlit?

**Streamlit** is an open-source Python framework used to build **interactive web applications** for:

* Data analysis
* Dashboards
* Machine learning demos
* AI / LLM-powered tools
* Internal tools & prototypes

### Key Idea

> **Write Python → Get a Web App**

No frontend frameworks. No HTML/CSS/JS required.

---

## 2️⃣ When & Why Use Streamlit

### ✅ Use Streamlit when:

* You want to quickly build a UI for Python logic
* You are building AI tools (chatbots, summarizers, RAG apps)
* You need internal dashboards
* You want fast iteration

### ❌ Not ideal when:

* You need heavy custom UI
* You are building large consumer apps
* SEO or fine-grained frontend control is critical

---

## 3️⃣ Installation & Setup

```bash
pip install streamlit
```

Check installation:

```bash
streamlit version
```

---

## 4️⃣ Streamlit App Structure

Minimal app:

```python
import streamlit as st

st.title("Hello Streamlit")
st.write("My first Streamlit app")
```

📁 Typical structure:

```
app.py
requirements.txt
pages/
  1_Dashboard.py
  2_Settings.py
```

---

## 5️⃣ Running a Streamlit App

```bash
streamlit run app.py
```

* App runs on: `http://localhost:8501`
* Auto reloads on file save

---

## 6️⃣ Core Concepts (VERY IMPORTANT)

---

### 🔁 Script Rerun Model

👉 **Streamlit re-runs the entire script from top to bottom on every user interaction**

Example:

```python
count = 0
if st.button("Click"):
    count += 1
st.write(count)
```

❌ This will always show `1`

Why?
Because the script restarts.

---

### ⚡ Reactivity

Widgets automatically trigger reruns.

```python
name = st.text_input("Enter name")
st.write("Hello", name)
```

No event handlers required.

---

## 7️⃣ Layout & Page Structure

---

### Titles & Text

```python
st.title("Main Title")
st.header("Header")
st.subheader("Subheader")
st.text("Plain text")
st.markdown("**Markdown supported**")
```

---

### Columns

```python
col1, col2 = st.columns(2)

with col1:
    st.write("Left")

with col2:
    st.write("Right")
```

---

### Containers

```python
with st.container():
    st.write("Grouped content")
```

---

## 8️⃣ Display Elements

---

### Metrics

```python
st.metric("Revenue", "₹1,20,000", "+8%")
```

---

### Status Messages

```python
st.success("Success")
st.error("Error")
st.warning("Warning")
st.info("Info")
```

---

### Progress Bar

```python
import time

progress = st.progress(0)
for i in range(100):
    time.sleep(0.05)
    progress.progress(i + 1)
```

---

## 9️⃣ Input Widgets

---

### Text Inputs

```python
st.text_input("Name")
st.text_area("Description")
```

---

### Numbers

```python
st.number_input("Age", min_value=0)
st.slider("Rating", 0, 10)
```

---

### Selection Widgets

```python
st.selectbox("Country", ["India", "USA"])
st.multiselect("Skills", ["Python", "JS", "AI"])
st.radio("Gender", ["Male", "Female"])
```

---

### Buttons

```python
if st.button("Submit"):
    st.write("Clicked!")
```

---

## 🔟 Data Display Components

---

### Tables & DataFrames

```python
import pandas as pd

df = pd.DataFrame({
    "Name": ["A", "B"],
    "Score": [80, 90]
})

st.dataframe(df)
st.table(df)
```

---

### JSON

```python
st.json({"name": "Vinod", "role": "Engineer"})
```

---

## 1️⃣1️⃣ Charts & Visualization

---

### Line Chart

```python
st.line_chart(df)
```

---

### Bar Chart

```python
st.bar_chart(df)
```

---

### Matplotlib

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.plot([1, 2, 3], [4, 5, 6])
st.pyplot(fig)
```

---

### Plotly

```python
import plotly.express as px

fig = px.line(df, x="Name", y="Score")
st.plotly_chart(fig)
```

---

## 1️⃣2️⃣ Forms (Prevent Multiple Reruns)

```python
with st.form("login"):
    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")
    submitted = st.form_submit_button("Login")

if submitted:
    st.write("Logged in:", user)
```

---

## 1️⃣3️⃣ Session State (CRITICAL)

Used to **persist data across reruns**.

---

### Initialize

```python
if "count" not in st.session_state:
    st.session_state.count = 0
```

---

### Update

```python
if st.button("Increment"):
    st.session_state.count += 1

st.write(st.session_state.count)
```

---

## 1️⃣4️⃣ Caching & Performance

---

### `st.cache_data`

Used for **data loading**

```python
@st.cache_data
def load_data():
    return pd.read_csv("data.csv")
```

---

### `st.cache_resource`

Used for **models, DB connections**

```python
@st.cache_resource
def load_model():
    return model
```

---

## 1️⃣5️⃣ File Uploads & Downloads

---

### Upload

```python
file = st.file_uploader("Upload CSV")
if file:
    df = pd.read_csv(file)
    st.dataframe(df)
```

---

### Download

```python
st.download_button(
    "Download",
    data="Hello",
    file_name="hello.txt"
)
```

---

## 1️⃣6️⃣ Sidebar & Multipage Apps

---

### Sidebar

```python
st.sidebar.title("Menu")
option = st.sidebar.selectbox("Choose", ["Home", "Settings"])
```

---

### Multipage Apps

📁 Structure:

```
app.py
pages/
  1_Home.py
  2_Settings.py
```

Streamlit auto-detects pages.

---

## 1️⃣7️⃣ Configuration & Theming

---

### `.streamlit/config.toml`

```toml
[theme]
primaryColor="#4CAF50"
backgroundColor="#FFFFFF"
textColor="#000000"
```

---

## 1️⃣8️⃣ Deployment Options

* Streamlit Community Cloud
* AWS EC2
* Docker
* HuggingFace Spaces
* Render / Railway

---

## 1️⃣9️⃣ Streamlit for AI / LLM Apps

Typical flow:

1. User input
2. Call LLM API
3. Show response

```python
prompt = st.text_area("Ask")
if st.button("Generate"):
    response = call_llm(prompt)
    st.write(response)
```

Perfect for:

* Chatbots
* Summarizers
* RAG systems
* AI tutors

---

## 2️⃣0️⃣ Best Practices

✅ Use `st.session_state`
✅ Use forms for inputs
✅ Cache heavy operations
✅ Modularize logic
✅ Keep UI simple

---

## 2️⃣1️⃣ Common Pitfalls

❌ Forgetting rerun behavior
❌ Heavy computation without caching
❌ Global variables
❌ Blocking API calls

---

## 2️⃣2️⃣ Mini Project Ideas

* AI Chatbot UI
* Resume Analyzer
* Text Summarizer
* CSV Dashboard
* LLM Playground
* Admin Panel for ML Models

---

## 🧠 Final Thought

> **Streamlit turns Python into a UI superpower.**

If you know Python, you already know Streamlit.

---
