# Embedding Metrics Explained  
## Cosine Similarity, Euclidean Distance, and Dot Product (with Python Examples)

**Audience:** GenAI Developers, ML Engineers, Backend Engineers  
**Level:** Beginner → Intermediate  
**Use cases:** Semantic Search, RAG, Clustering, Recommendation Systems

---

## 1. Introduction

Embeddings convert text, images, or other data into **numerical vectors**.  
To compare embeddings, we use **distance or similarity metrics**.

The most commonly used embedding metrics are:
- **Cosine Similarity**
- **Euclidean Distance**
- **Dot Product**

Each metric answers a slightly different question.

---

## 2. Why Embedding Metrics Matter

Embedding metrics help answer:
- *How similar are two texts?*
- *Which document is closest to the query?*
- *Which vectors should be retrieved first?*

Choosing the wrong metric can:
- Reduce search accuracy
- Break ranking logic
- Mislead clustering algorithms

---

## 3. Sample Embeddings (for All Examples)

We will use small vectors for clarity.

```python
import numpy as np

vec_a = np.array([1, 2, 3])
vec_b = np.array([2, 4, 6])
vec_c = np.array([3, 0, 1])
````

---

## 4. Cosine Similarity

### 4.1 What is Cosine Similarity?

Cosine similarity measures the **angle** between two vectors, not their magnitude.

> It answers:
> **Are these vectors pointing in the same direction?**

---

### 4.2 Formula

$$
\text{cosine\_similarity}(A, B) =
\frac{A \cdot B}{||A|| \times ||B||}
$$

Where:

* `A · B` = dot product
* `||A||` = vector magnitude (length)

---

### 4.3 Python Implementation

```python
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

print(cosine_similarity(vec_a, vec_b))
print(cosine_similarity(vec_a, vec_c))
```

---

### 4.4 Output Interpretation

| Comparison     | Result | Meaning                |
| -------------- | ------ | ---------------------- |
| vec_a vs vec_b | ~1.0   | Very similar direction |
| vec_a vs vec_c | ~0.55  | Partially similar      |

**Range:**

* `1.0` → identical direction
* `0.0` → orthogonal (unrelated)
* `-1.0` → opposite meaning

---

### 4.5 When to Use Cosine Similarity

Best for:

* Text embeddings
* Semantic search
* RAG systems
* Normalized vectors

Not ideal when magnitude matters

---

## 5. Euclidean Distance

### 5.1 What is Euclidean Distance?

Euclidean distance measures **straight-line distance** between vectors.

> It answers:
> **How far apart are these vectors in space?**

---

### 5.2 Formula

$$
\text{distance}(A, B) =
\sqrt{\sum (A_i - B_i)^2}
$$

---

### 5.3 Python Implementation

```python
def euclidean_distance(a, b):
    return np.linalg.norm(a - b)

print(euclidean_distance(vec_a, vec_b))
print(euclidean_distance(vec_a, vec_c))
```

---

### 5.4 Output Interpretation

| Comparison     | Distance | Meaning                            |
| -------------- | -------- | ---------------------------------- |
| vec_a vs vec_b | High     | Far apart (even if direction same) |
| vec_a vs vec_c | Medium   | Somewhat close                     |

**Key Insight:**
Even if vectors point in the same direction, **larger magnitude increases distance**.

---

### 5.5 When to Use Euclidean Distance

Best for:

* Clustering (K-Means)
* Spatial similarity
* When magnitude matters

Less ideal for high-dimensional text embeddings

---

## 6. Dot Product

### 6.1 What is Dot Product?

Dot product measures **both direction and magnitude**.

> It answers:
> **Are these vectors aligned and how strong is that alignment?**

---

### 6.2 Formula

$$
A \cdot B = \sum A_i \times B_i
$$

---

### 6.3 Python Implementation

```python
def dot_product(a, b):
    return np.dot(a, b)

print(dot_product(vec_a, vec_b))
print(dot_product(vec_a, vec_c))
```

---

### 6.4 Output Interpretation

| Comparison     | Dot Value | Meaning          |
| -------------- | --------- | ---------------- |
| vec_a vs vec_b | High      | Strong alignment |
| vec_a vs vec_c | Low       | Weak alignment   |

**Note:** Dot product is **unbounded** (no fixed range).

---

### 6.5 Normalized Dot Product = Cosine Similarity

```python
vec_a_norm = vec_a / np.linalg.norm(vec_a)
vec_b_norm = vec_b / np.linalg.norm(vec_b)

print(np.dot(vec_a_norm, vec_b_norm))
```

This produces the **same result as cosine similarity**.

---

## 7. Metric Comparison Summary

| Metric      | Measures          | Range   | Sensitive to Magnitude |
| ----------- | ----------------- | ------- | ---------------------- |
| Cosine      | Direction         | -1 to 1 | No                     |
| Euclidean   | Distance          | 0 → ∞   | Yes                    |
| Dot Product | Alignment + scale | -∞ → ∞  | Yes                    |

---

## 8. Metric Choice in Real Systems

### 8.1 Semantic Search / RAG

```text
Use: Cosine Similarity
```

Reason:

* Embeddings are usually normalized
* Direction matters more than size

---

### 8.2 Clustering

```text
Use: Euclidean Distance
```

Reason:

* Clusters depend on spatial proximity

---

### 8.3 Recommendation / Ranking

```text
Use: Dot Product
```

Reason:

* Magnitude can represent importance or weight

---

## 9. Example: Ranking Documents

```python
query = np.array([1, 1, 0])
docs = [
    np.array([1, 1, 0]),
    np.array([0, 1, 1]),
    np.array([1, 0, 0])
]

scores = [(i, cosine_similarity(query, d)) for i, d in enumerate(docs)]
scores.sort(key=lambda x: x[1], reverse=True)

print(scores)
```

---

## 10. Key Takeaways

* **Cosine similarity** is the default for text embeddings
* **Euclidean distance** measures physical closeness
* **Dot product** combines direction and scale
* Normalization changes dot → cosine
* Metric choice directly affects retrieval quality

---

## 11. Next Topics You Can Learn

* Vector normalization
* Approximate Nearest Neighbors (ANN)
* FAISS / HNSW indexing
* Embedding drift & re-indexing
* Hybrid search (BM25 + embeddings)

---
