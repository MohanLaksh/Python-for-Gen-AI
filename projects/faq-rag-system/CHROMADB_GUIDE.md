# ChromaDB Complete Guide
## CRUD Operations and Advanced Techniques for Gen AI Developers

---

## Table of Contents

1. [Introduction to ChromaDB](#introduction-to-chromadb)
2. [Installation and Setup](#installation-and-setup)
3. [Core Concepts](#core-concepts)
4. [CRUD Operations](#crud-operations)
5. [Embedding Functions](#embedding-functions)
6. [Querying and Search](#querying-and-search)
7. [Metadata Filtering](#metadata-filtering)
8. [Advanced Features](#advanced-features)
9. [Best Practices](#best-practices)
10. [Production Deployment](#production-deployment)
11. [Performance Optimization](#performance-optimization)
12. [Common Use Cases](#common-use-cases)
13. [Troubleshooting](#troubleshooting)

---

## Introduction to ChromaDB

ChromaDB is an open-source embedding database designed for AI applications. It provides a simple, fast, and scalable way to store and retrieve embeddings with metadata, making it ideal for building RAG (Retrieval-Augmented Generation) systems, semantic search, and other AI-powered applications.

### Why ChromaDB?

**Key Features:**
- **Simple API**: Easy to use with minimal setup
- **Built for AI**: Native support for embeddings and vector similarity search
- **Flexible**: Works with any embedding model (OpenAI, Sentence Transformers, etc.)
- **Metadata Support**: Rich filtering capabilities on metadata
- **Multiple Storage Options**: In-memory, persistent, or client-server
- **Production Ready**: Supports Docker deployment and horizontal scaling

**Common Use Cases:**
- Retrieval-Augmented Generation (RAG) systems
- Semantic search engines
- Document Q&A systems
- Chatbots with long-term memory
- Recommendation systems
- Content deduplication

---

## Installation and Setup

### Basic Installation

```bash
# Install ChromaDB
pip install chromadb

# Optional: Install with specific embedding models
pip install chromadb[openai]  # For OpenAI embeddings
pip install chromadb[cohere]  # For Cohere embeddings
```

### Quick Start

```python
import chromadb

# Create a client (in-memory by default)
client = chromadb.Client()

# Create a collection
collection = client.create_collection(name="my_collection")

# Add some documents
collection.add(
    documents=["This is document 1", "This is document 2"],
    ids=["id1", "id2"]
)

# Query the collection
results = collection.query(
    query_texts=["Find similar documents"],
    n_results=2
)

print(results)
```

### Storage Modes

#### 1. In-Memory (Default)
```python
import chromadb

# Data is lost when program exits
client = chromadb.Client()
```

#### 2. Persistent Storage
```python
import chromadb

# Data persists to disk
client = chromadb.PersistentClient(path="/path/to/data")

# Or use settings
from chromadb.config import Settings

client = chromadb.Client(Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory="/path/to/data"
))
```

#### 3. Client-Server Mode
```python
import chromadb

# Connect to a ChromaDB server
client = chromadb.HttpClient(
    host="localhost",
    port=8000
)
```

**Starting ChromaDB Server:**
```bash
# Install server dependencies
pip install chromadb[server]

# Run the server
chroma run --path /path/to/data --port 8000

# Or use Docker
docker run -p 8000:8000 chromadb/chroma
```

---

## Core Concepts

### Collections

Collections are groups of embeddings with associated metadata. Think of them as tables in a traditional database.

```python
# Create a collection
collection = client.create_collection(
    name="documents",
    metadata={"description": "A collection of documents"}
)

# Get an existing collection
collection = client.get_collection(name="documents")

# Get or create (useful for idempotent operations)
collection = client.get_or_create_collection(name="documents")

# List all collections
collections = client.list_collections()
print([col.name for col in collections])

# Delete a collection
client.delete_collection(name="documents")
```

### Documents, Embeddings, and Metadata

**Document**: The actual text content  
**Embedding**: Vector representation of the document  
**Metadata**: Additional information about the document (tags, timestamps, etc.)  
**ID**: Unique identifier for each document

```python
collection.add(
    documents=["Paris is the capital of France"],  # The text
    embeddings=[[0.1, 0.2, 0.3, ...]],           # Optional: provide your own
    metadatas=[{"source": "wikipedia", "date": "2024-01-01"}],  # Optional metadata
    ids=["doc1"]  # Required: unique ID
)
```

### Distance Metrics

ChromaDB supports different distance metrics for similarity search:

```python
# L2 (Euclidean distance) - default
collection = client.create_collection(
    name="l2_collection",
    metadata={"hnsw:space": "l2"}
)

# Cosine similarity (most common for text)
collection = client.create_collection(
    name="cosine_collection",
    metadata={"hnsw:space": "cosine"}
)

# Inner product
collection = client.create_collection(
    name="ip_collection",
    metadata={"hnsw:space": "ip"}
)
```

---

## CRUD Operations

### Create (Add Documents)

#### Basic Add
```python
import chromadb

client = chromadb.Client()
collection = client.get_or_create_collection(name="documents")

# Add a single document
collection.add(
    documents=["The quick brown fox jumps over the lazy dog"],
    ids=["doc1"]
)

# Add multiple documents
collection.add(
    documents=[
        "Machine learning is a subset of AI",
        "Deep learning uses neural networks",
        "Natural language processing handles text"
    ],
    ids=["doc2", "doc3", "doc4"]
)
```

#### Add with Metadata
```python
collection.add(
    documents=[
        "Python is a programming language",
        "JavaScript is used for web development",
        "Java is used for enterprise applications"
    ],
    metadatas=[
        {"category": "programming", "difficulty": "beginner", "year": 1991},
        {"category": "programming", "difficulty": "intermediate", "year": 1995},
        {"category": "programming", "difficulty": "intermediate", "year": 1995}
    ],
    ids=["lang1", "lang2", "lang3"]
)
```

#### Add with Custom Embeddings
```python
# If you want to provide your own embeddings
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
documents = ["First document", "Second document"]
embeddings = model.encode(documents).tolist()

collection.add(
    documents=documents,
    embeddings=embeddings,
    ids=["custom1", "custom2"]
)
```

#### Batch Adding (Large Datasets)
```python
def batch_add(collection, documents, batch_size=100):
    """Add documents in batches for better performance."""
    for i in range(0, len(documents), batch_size):
        batch = documents[i:i + batch_size]
        collection.add(
            documents=batch,
            ids=[f"doc_{j}" for j in range(i, i + len(batch))]
        )
        print(f"Added batch {i//batch_size + 1}")

# Usage
large_document_list = ["Document " + str(i) for i in range(10000)]
batch_add(collection, large_document_list)
```

### Read (Retrieve Documents)

#### Get by ID
```python
# Get specific documents by ID
results = collection.get(
    ids=["doc1", "doc2"]
)

print(results)
# {
#     'ids': ['doc1', 'doc2'],
#     'documents': ['...', '...'],
#     'metadatas': [{...}, {...}],
#     'embeddings': None  # Not returned by default
# }

# Include embeddings in results
results = collection.get(
    ids=["doc1"],
    include=["documents", "metadatas", "embeddings"]
)
```

#### Get All Documents
```python
# Get all documents in collection
results = collection.get()

print(f"Total documents: {len(results['ids'])}")
```

#### Get with Metadata Filter
```python
# Get documents matching metadata criteria
results = collection.get(
    where={"category": "programming"},
    limit=10
)

# Complex metadata queries
results = collection.get(
    where={
        "$and": [
            {"category": "programming"},
            {"difficulty": "beginner"}
        ]
    }
)
```

#### Peek (Quick Look)
```python
# Get first N documents (useful for debugging)
results = collection.peek(limit=5)
```

### Update (Modify Documents)

#### Update Documents
```python
# Update document content
collection.update(
    ids=["doc1"],
    documents=["Updated content for document 1"]
)

# Update metadata only
collection.update(
    ids=["doc2"],
    metadatas=[{"category": "updated", "status": "reviewed"}]
)

# Update both document and metadata
collection.update(
    ids=["doc3"],
    documents=["New content"],
    metadatas=[{"updated_at": "2024-02-05"}]
)
```

#### Update with Custom Embeddings
```python
# Provide new embeddings
collection.update(
    ids=["doc1"],
    embeddings=[[0.5, 0.6, 0.7, ...]],
    documents=["New document content"]
)
```

#### Upsert (Update or Insert)
```python
# Upsert: update if exists, insert if not
collection.upsert(
    ids=["doc1", "new_doc"],
    documents=["Updated doc1", "Brand new document"],
    metadatas=[{"status": "updated"}, {"status": "new"}]
)
```

### Delete (Remove Documents)

#### Delete by ID
```python
# Delete specific documents
collection.delete(ids=["doc1", "doc2"])

# Delete a single document
collection.delete(ids=["doc3"])
```

#### Delete with Metadata Filter
```python
# Delete all documents matching criteria
collection.delete(
    where={"category": "temporary"}
)

# Delete old documents
collection.delete(
    where={"year": {"$lt": 2020}}
)
```

#### Delete All Documents
```python
# Clear entire collection
collection.delete(where={})

# Or get all IDs and delete
all_ids = collection.get()['ids']
if all_ids:
    collection.delete(ids=all_ids)
```

---

## Embedding Functions

ChromaDB can automatically generate embeddings for your documents using various embedding models.

### Default Embedding Function

```python
# ChromaDB uses a default embedding function
collection = client.create_collection(name="default_embeddings")

# It will automatically embed documents when you add them
collection.add(
    documents=["Text to embed"],
    ids=["id1"]
)
```

### Sentence Transformers

```python
from chromadb.utils import embedding_functions

# Use Sentence Transformers
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

collection = client.create_collection(
    name="sentence_transformers",
    embedding_function=sentence_transformer_ef
)

# Documents are automatically embedded
collection.add(
    documents=["Document to embed"],
    ids=["id1"]
)
```

**Popular Sentence Transformer Models:**
- `all-MiniLM-L6-v2`: Fast and efficient (384 dimensions)
- `all-mpnet-base-v2`: High quality (768 dimensions)
- `multi-qa-mpnet-base-dot-v1`: Optimized for Q&A
- `paraphrase-multilingual-MiniLM-L12-v2`: Multilingual support

### OpenAI Embeddings

```python
from chromadb.utils import embedding_functions

# OpenAI embedding function
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key="your-api-key",
    model_name="text-embedding-3-small"
)

collection = client.create_collection(
    name="openai_embeddings",
    embedding_function=openai_ef
)
```

**OpenAI Models:**
- `text-embedding-3-small`: Cost-effective, 1536 dimensions
- `text-embedding-3-large`: Highest quality, 3072 dimensions
- `text-embedding-ada-002`: Legacy model, 1536 dimensions

### Cohere Embeddings

```python
from chromadb.utils import embedding_functions

cohere_ef = embedding_functions.CohereEmbeddingFunction(
    api_key="your-api-key",
    model_name="embed-english-v3.0"
)

collection = client.create_collection(
    name="cohere_embeddings",
    embedding_function=cohere_ef
)
```

### HuggingFace Embeddings

```python
from chromadb.utils import embedding_functions

huggingface_ef = embedding_functions.HuggingFaceEmbeddingFunction(
    api_key="your-api-key",
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

collection = client.create_collection(
    name="huggingface_embeddings",
    embedding_function=huggingface_ef
)
```

### Custom Embedding Function

```python
from chromadb import Documents, EmbeddingFunction, Embeddings

class MyEmbeddingFunction(EmbeddingFunction):
    def __call__(self, input: Documents) -> Embeddings:
        # Your custom embedding logic
        # Return a list of embeddings (list of lists of floats)
        embeddings = []
        for doc in input:
            # Example: simple word count embedding (don't use in production!)
            embedding = [len(doc), len(doc.split()), doc.count(' ')]
            embeddings.append(embedding)
        return embeddings

custom_ef = MyEmbeddingFunction()
collection = client.create_collection(
    name="custom_embeddings",
    embedding_function=custom_ef
)
```

### Using Multiple Embedding Functions

```python
# Different collections can use different embedding functions
st_collection = client.create_collection(
    name="sentence_transformer_docs",
    embedding_function=sentence_transformer_ef
)

openai_collection = client.create_collection(
    name="openai_docs",
    embedding_function=openai_ef
)
```

---

## Querying and Search

### Basic Query

```python
# Query with text
results = collection.query(
    query_texts=["What is machine learning?"],
    n_results=5
)

print(results)
# {
#     'ids': [['doc2', 'doc3', ...]],
#     'distances': [[0.1, 0.3, ...]],
#     'documents': [['Machine learning is...', ...]],
#     'metadatas': [[{...}, {...}]]
# }
```

### Multiple Queries

```python
# Query with multiple texts (batch query)
results = collection.query(
    query_texts=[
        "What is Python?",
        "Tell me about JavaScript"
    ],
    n_results=3
)

# Results are grouped by query
for i, query in enumerate(["What is Python?", "Tell me about JavaScript"]):
    print(f"\nResults for: {query}")
    print(f"IDs: {results['ids'][i]}")
    print(f"Documents: {results['documents'][i]}")
```

### Query with Embeddings

```python
# Query using pre-computed embeddings
query_embedding = [[0.1, 0.2, 0.3, ...]]

results = collection.query(
    query_embeddings=query_embedding,
    n_results=5
)
```

### Query with Metadata Filters

```python
# Filter results by metadata
results = collection.query(
    query_texts=["programming languages"],
    n_results=10,
    where={"difficulty": "beginner"}
)

# Complex filters
results = collection.query(
    query_texts=["AI topics"],
    n_results=5,
    where={
        "$and": [
            {"category": "programming"},
            {"year": {"$gte": 2000}}
        ]
    }
)
```

### Query with Document Filters

```python
# Filter based on document content
results = collection.query(
    query_texts=["machine learning"],
    n_results=5,
    where_document={"$contains": "neural"}
)
```

### Control Result Contents

```python
# Specify what to include in results
results = collection.query(
    query_texts=["search query"],
    n_results=5,
    include=["documents", "metadatas", "distances"]  # Exclude embeddings
)

# Include only specific fields
results = collection.query(
    query_texts=["search query"],
    n_results=5,
    include=["metadatas"]  # Only metadata
)
```

---

## Metadata Filtering

ChromaDB supports powerful metadata filtering using a MongoDB-like query syntax.

### Basic Operators

#### Equality
```python
# Exact match
collection.query(
    query_texts=["query"],
    where={"category": "science"}
)
```

#### Inequality
```python
# Not equal
collection.query(
    query_texts=["query"],
    where={"status": {"$ne": "draft"}}
)
```

#### Comparison Operators
```python
# Greater than
collection.query(
    query_texts=["query"],
    where={"year": {"$gt": 2020}}
)

# Greater than or equal
collection.query(
    query_texts=["query"],
    where={"score": {"$gte": 0.8}}
)

# Less than
collection.query(
    query_texts=["query"],
    where={"price": {"$lt": 100}}
)

# Less than or equal
collection.query(
    query_texts=["query"],
    where={"rating": {"$lte": 3}}
)
```

### Logical Operators

#### AND
```python
# Multiple conditions (all must be true)
collection.query(
    query_texts=["query"],
    where={
        "$and": [
            {"category": "tech"},
            {"status": "published"},
            {"year": {"$gte": 2020}}
        ]
    }
)
```

#### OR
```python
# Any condition can be true
collection.query(
    query_texts=["query"],
    where={
        "$or": [
            {"category": "tech"},
            {"category": "science"}
        ]
    }
)
```

#### Combined Logic
```python
# Complex nested logic
collection.query(
    query_texts=["query"],
    where={
        "$and": [
            {
                "$or": [
                    {"category": "tech"},
                    {"category": "science"}
                ]
            },
            {"year": {"$gte": 2020}},
            {"status": "published"}
        ]
    }
)
```

### Membership Operators

#### IN
```python
# Value must be in list
collection.query(
    query_texts=["query"],
    where={"category": {"$in": ["tech", "science", "engineering"]}}
)
```

#### NIN (Not In)
```python
# Value must not be in list
collection.query(
    query_texts=["query"],
    where={"status": {"$nin": ["draft", "archived"]}}
)
```

### Document Content Filters

```python
# Contains substring
collection.query(
    query_texts=["query"],
    where_document={"$contains": "machine learning"}
)

# Does not contain
collection.query(
    query_texts=["query"],
    where_document={"$not_contains": "deprecated"}
)
```

### Practical Examples

#### Filter by Date Range
```python
# Documents from specific date range
collection.query(
    query_texts=["recent AI developments"],
    where={
        "$and": [
            {"date": {"$gte": "2024-01-01"}},
            {"date": {"$lte": "2024-12-31"}}
        ]
    }
)
```

#### Multi-Tag Filtering
```python
# Documents with specific tags
collection.query(
    query_texts=["search query"],
    where={
        "tags": {"$in": ["python", "tutorial"]}
    }
)
```

#### Exclude Certain Types
```python
# Exclude specific document types
collection.query(
    query_texts=["search query"],
    where={
        "type": {"$nin": ["advertisement", "spam"]}
    }
)
```

#### Complex Business Logic
```python
# Premium published content from last year
collection.query(
    query_texts=["latest content"],
    where={
        "$and": [
            {"tier": "premium"},
            {"status": "published"},
            {"year": 2024},
            {"rating": {"$gte": 4.0}},
            {"views": {"$gt": 1000}}
        ]
    },
    n_results=20
)
```

---

## Advanced Features

### Collection Management

#### Collection Metadata
```python
# Create collection with metadata
collection = client.create_collection(
    name="articles",
    metadata={
        "description": "News articles collection",
        "created_by": "data_team",
        "version": "1.0"
    }
)

# Get collection metadata
metadata = collection.metadata
print(metadata)

# Modify collection metadata
collection.modify(metadata={"version": "1.1", "updated": "2024-02-05"})
```

#### Collection Count
```python
# Get number of documents in collection
count = collection.count()
print(f"Collection contains {count} documents")
```

### Multi-Modal Collections

```python
# Store different types of content with metadata
collection.add(
    documents=[
        "This is a text document",
        "Image description: A cat sitting on a mat",
        "Video transcript: Welcome to our tutorial"
    ],
    metadatas=[
        {"type": "text", "format": "markdown"},
        {"type": "image", "format": "jpg", "width": 800, "height": 600},
        {"type": "video", "format": "mp4", "duration": 120}
    ],
    ids=["text1", "img1", "vid1"]
)

# Query by modality
text_results = collection.query(
    query_texts=["find documents"],
    where={"type": "text"},
    n_results=5
)
```

### Hybrid Search (Combining Filters and Similarity)

```python
# Semantic search + metadata filtering
results = collection.query(
    query_texts=["machine learning algorithms"],
    where={
        "$and": [
            {"category": "AI"},
            {"difficulty": {"$in": ["beginner", "intermediate"]}},
            {"year": {"$gte": 2022}}
        ]
    },
    n_results=10
)
```

### Re-ranking Results

```python
# Get more results than needed, then re-rank
initial_results = collection.query(
    query_texts=["search query"],
    n_results=50  # Get 50 candidates
)

# Custom re-ranking logic
def custom_rerank(results, criteria):
    """Re-rank based on custom criteria."""
    ranked = []
    for i, doc_id in enumerate(results['ids'][0]):
        metadata = results['metadatas'][0][i]
        distance = results['distances'][0][i]
        
        # Custom scoring (example: boost recent documents)
        recency_score = metadata.get('year', 2000) / 2024
        quality_score = metadata.get('rating', 0) / 5
        relevance_score = 1 - distance  # Lower distance = higher relevance
        
        combined_score = (relevance_score * 0.5 + 
                         recency_score * 0.3 + 
                         quality_score * 0.2)
        
        ranked.append({
            'id': doc_id,
            'score': combined_score,
            'document': results['documents'][0][i],
            'metadata': metadata
        })
    
    # Sort by combined score
    ranked.sort(key=lambda x: x['score'], reverse=True)
    return ranked[:10]  # Return top 10

# Apply custom ranking
final_results = custom_rerank(initial_results, criteria={})
```

### Document Deduplication

```python
def find_duplicates(collection, threshold=0.95):
    """Find near-duplicate documents."""
    all_docs = collection.get()
    duplicates = []
    
    for i, doc_id in enumerate(all_docs['ids']):
        # Query with this document's embedding
        results = collection.query(
            query_texts=[all_docs['documents'][i]],
            n_results=5
        )
        
        # Check for very similar documents (excluding itself)
        for j, similar_id in enumerate(results['ids'][0][1:], 1):
            distance = results['distances'][0][j]
            similarity = 1 - distance
            
            if similarity > threshold:
                duplicates.append({
                    'doc1': doc_id,
                    'doc2': similar_id,
                    'similarity': similarity
                })
    
    return duplicates

# Usage
duplicates = find_duplicates(collection, threshold=0.95)
print(f"Found {len(duplicates)} potential duplicates")
```

### Incremental Updates

```python
class IncrementalUpdater:
    """Handle incremental updates to a collection."""
    
    def __init__(self, collection):
        self.collection = collection
    
    def sync_documents(self, new_documents):
        """Add new documents and update existing ones."""
        existing_ids = set(self.collection.get()['ids'])
        
        to_add = []
        to_add_ids = []
        to_update = []
        to_update_ids = []
        
        for doc in new_documents:
            if doc['id'] in existing_ids:
                to_update.append(doc['text'])
                to_update_ids.append(doc['id'])
            else:
                to_add.append(doc['text'])
                to_add_ids.append(doc['id'])
        
        # Add new documents
        if to_add:
            self.collection.add(
                documents=to_add,
                ids=to_add_ids,
                metadatas=[doc.get('metadata', {}) for doc in new_documents 
                          if doc['id'] in to_add_ids]
            )
            print(f"Added {len(to_add)} new documents")
        
        # Update existing documents
        if to_update:
            self.collection.update(
                documents=to_update,
                ids=to_update_ids,
                metadatas=[doc.get('metadata', {}) for doc in new_documents 
                          if doc['id'] in to_update_ids]
            )
            print(f"Updated {len(to_update)} documents")

# Usage
updater = IncrementalUpdater(collection)
new_docs = [
    {'id': 'doc1', 'text': 'Updated content', 'metadata': {'status': 'updated'}},
    {'id': 'new_doc', 'text': 'New content', 'metadata': {'status': 'new'}}
]
updater.sync_documents(new_docs)
```

---

## Best Practices

### 1. Collection Design

#### Choose Appropriate Names
```python
# ✅ Good: Descriptive, namespaced
collection = client.create_collection("prod_customer_support_docs_v1")

# ❌ Bad: Vague, no versioning
collection = client.create_collection("docs")
```

#### Use Metadata for Organization
```python
# Store rich metadata
collection.add(
    documents=["Document content"],
    metadatas=[{
        "source": "api",
        "created_at": "2024-02-05T10:00:00Z",
        "author": "system",
        "version": 1,
        "tags": ["important", "reviewed"],
        "doc_type": "technical"
    }],
    ids=["doc1"]
)
```

#### Plan Your Schema
```python
# Define metadata schema
METADATA_SCHEMA = {
    "source": str,        # Required: where doc came from
    "created_at": str,    # Required: ISO timestamp
    "category": str,      # Required: document category
    "tags": list,         # Optional: list of tags
    "priority": int,      # Optional: 1-5
    "version": int,       # Required: document version
    "author": str,        # Optional: creator
}

def validate_metadata(metadata):
    """Validate metadata against schema."""
    for key, expected_type in METADATA_SCHEMA.items():
        if key in metadata:
            if not isinstance(metadata[key], expected_type):
                raise ValueError(f"{key} must be {expected_type}")
    return True
```

### 2. ID Management

#### Use Meaningful IDs
```python
# ✅ Good: Structured, meaningful
id_format = f"{source}_{category}_{timestamp}_{hash}"
collection.add(
    documents=["content"],
    ids=["wiki_science_20240205_abc123"]
)

# ❌ Bad: Sequential numbers (hard to debug)
collection.add(documents=["content"], ids=["1"])
```

#### Generate Consistent IDs
```python
import hashlib
from datetime import datetime

def generate_doc_id(content, source):
    """Generate consistent ID for document."""
    # Create hash of content
    content_hash = hashlib.md5(content.encode()).hexdigest()[:8]
    timestamp = datetime.now().strftime("%Y%m%d")
    return f"{source}_{timestamp}_{content_hash}"

# Usage
doc_id = generate_doc_id("Document content", "api")
collection.add(documents=["Document content"], ids=[doc_id])
```

### 3. Batch Operations

```python
# ✅ Good: Batch operations
def add_documents_efficiently(collection, documents, batch_size=100):
    """Add documents in batches."""
    for i in range(0, len(documents), batch_size):
        batch = documents[i:i + batch_size]
        collection.add(
            documents=[d['text'] for d in batch],
            metadatas=[d['metadata'] for d in batch],
            ids=[d['id'] for d in batch]
        )
        print(f"Processed {min(i + batch_size, len(documents))}/{len(documents)}")

# ❌ Bad: One at a time
for doc in documents:
    collection.add(documents=[doc['text']], ids=[doc['id']])  # Slow!
```

### 4. Error Handling

```python
from chromadb.errors import ChromaError, IDAlreadyExistsError

def safe_add(collection, documents, ids, metadatas):
    """Add documents with error handling."""
    try:
        collection.add(
            documents=documents,
            ids=ids,
            metadatas=metadatas
        )
        return True, "Success"
    
    except IDAlreadyExistsError:
        # Try upsert instead
        try:
            collection.upsert(
                documents=documents,
                ids=ids,
                metadatas=metadatas
            )
            return True, "Updated existing documents"
        except Exception as e:
            return False, f"Upsert failed: {e}"
    
    except ChromaError as e:
        return False, f"ChromaDB error: {e}"
    
    except Exception as e:
        return False, f"Unexpected error: {e}"

# Usage
success, message = safe_add(
    collection,
    documents=["doc"],
    ids=["id1"],
    metadatas=[{"key": "value"}]
)
```

### 5. Query Optimization

```python
# ✅ Good: Request only needed fields
results = collection.query(
    query_texts=["query"],
    n_results=10,
    include=["documents", "metadatas"]  # Exclude embeddings
)

# ❌ Bad: Request everything (slower)
results = collection.query(
    query_texts=["query"],
    n_results=10,
    include=["documents", "metadatas", "embeddings", "distances"]
)

# ✅ Good: Use metadata filters to narrow search
results = collection.query(
    query_texts=["query"],
    where={"category": "relevant"},  # Pre-filter
    n_results=10
)

# ❌ Bad: Filter in Python after retrieval
all_results = collection.query(query_texts=["query"], n_results=1000)
filtered = [r for r in all_results if r['metadata']['category'] == 'relevant']
```

### 6. Memory Management

```python
# For large collections, use persistent storage
client = chromadb.PersistentClient(path="./chroma_data")

# Clean up when done
def cleanup_old_collections(client, days_old=30):
    """Remove collections older than specified days."""
    from datetime import datetime, timedelta
    
    cutoff_date = datetime.now() - timedelta(days=days_old)
    
    for collection in client.list_collections():
        metadata = collection.metadata
        if 'created_at' in metadata:
            created = datetime.fromisoformat(metadata['created_at'])
            if created < cutoff_date:
                print(f"Deleting old collection: {collection.name}")
                client.delete_collection(collection.name)
```

### 7. Testing

```python
import pytest
import chromadb

@pytest.fixture
def test_collection():
    """Create a test collection."""
    client = chromadb.Client()  # In-memory
    collection = client.create_collection("test")
    yield collection
    # Cleanup happens automatically with in-memory client

def test_add_and_query(test_collection):
    """Test basic add and query operations."""
    # Add documents
    test_collection.add(
        documents=["test document"],
        ids=["test1"],
        metadatas=[{"type": "test"}]
    )
    
    # Query
    results = test_collection.query(
        query_texts=["test"],
        n_results=1
    )
    
    assert len(results['ids'][0]) == 1
    assert results['ids'][0][0] == "test1"

def test_metadata_filtering(test_collection):
    """Test metadata filtering."""
    test_collection.add(
        documents=["doc1", "doc2"],
        ids=["id1", "id2"],
        metadatas=[{"category": "A"}, {"category": "B"}]
    )
    
    results = test_collection.get(where={"category": "A"})
    assert len(results['ids']) == 1
    assert results['ids'][0] == "id1"
```

---

## Production Deployment

### Docker Deployment

#### Docker Compose Setup
```yaml
# docker-compose.yml
version: '3.8'

services:
  chromadb:
    image: chromadb/chroma:latest
    ports:
      - "8000:8000"
    volumes:
      - ./chroma_data:/chroma/chroma
      - ./chroma_config:/chroma/config
    environment:
      - ALLOW_RESET=True  # Set to False in production
      - ANONYMIZED_TELEMETRY=False
    command: uvicorn chromadb.app:app --reload --workers 1 --host 0.0.0.0 --port 8000 --log-config /chroma/config/log_config.yml
```

**Start the service:**
```bash
docker-compose up -d
```

**Connect from client:**
```python
import chromadb

client = chromadb.HttpClient(
    host="localhost",
    port=8000
)
```

### Authentication and Security

```python
from chromadb.config import Settings

# Client with authentication
client = chromadb.HttpClient(
    host="your-server.com",
    port=8000,
    settings=Settings(
        chroma_client_auth_provider="token",
        chroma_client_auth_credentials="your-auth-token"
    )
)
```

### Environment-Based Configuration

```python
import os
from chromadb.config import Settings

def get_client():
    """Get ChromaDB client based on environment."""
    env = os.getenv("ENVIRONMENT", "development")
    
    if env == "production":
        return chromadb.HttpClient(
            host=os.getenv("CHROMA_HOST"),
            port=int(os.getenv("CHROMA_PORT", 8000)),
            settings=Settings(
                chroma_client_auth_provider="token",
                chroma_client_auth_credentials=os.getenv("CHROMA_AUTH_TOKEN")
            )
        )
    elif env == "staging":
        return chromadb.PersistentClient(
            path=os.getenv("CHROMA_PATH", "./staging_data")
        )
    else:  # development
        return chromadb.Client()  # In-memory

# Usage
client = get_client()
```

### Monitoring and Logging

```python
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MonitoredCollection:
    """Wrapper for collection with monitoring."""
    
    def __init__(self, collection):
        self.collection = collection
        self.stats = {
            'queries': 0,
            'adds': 0,
            'updates': 0,
            'deletes': 0
        }
    
    def add(self, **kwargs):
        """Add with logging."""
        start = datetime.now()
        try:
            result = self.collection.add(**kwargs)
            duration = (datetime.now() - start).total_seconds()
            self.stats['adds'] += 1
            logger.info(f"Added {len(kwargs.get('ids', []))} documents in {duration:.2f}s")
            return result
        except Exception as e:
            logger.error(f"Add failed: {e}")
            raise
    
    def query(self, **kwargs):
        """Query with logging."""
        start = datetime.now()
        try:
            result = self.collection.query(**kwargs)
            duration = (datetime.now() - start).total_seconds()
            self.stats['queries'] += 1
            logger.info(f"Query completed in {duration:.2f}s")
            return result
        except Exception as e:
            logger.error(f"Query failed: {e}")
            raise
    
    def get_stats(self):
        """Get usage statistics."""
        return self.stats

# Usage
collection = MonitoredCollection(client.get_collection("my_collection"))
```

### Backup and Recovery

```python
import shutil
from datetime import datetime
import json

def backup_collection(collection, backup_dir="./backups"):
    """Backup a collection to JSON."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{backup_dir}/{collection.name}_{timestamp}.json"
    
    # Get all data
    data = collection.get()
    
    # Save to JSON
    backup_data = {
        'metadata': collection.metadata,
        'documents': data['documents'],
        'metadatas': data['metadatas'],
        'ids': data['ids'],
        'timestamp': timestamp
    }
    
    os.makedirs(backup_dir, exist_ok=True)
    with open(backup_path, 'w') as f:
        json.dump(backup_data, f)
    
    logger.info(f"Backed up {len(data['ids'])} documents to {backup_path}")
    return backup_path

def restore_collection(client, backup_path, collection_name=None):
    """Restore a collection from backup."""
    with open(backup_path, 'r') as f:
        backup_data = json.load(f)
    
    # Create collection
    name = collection_name or backup_data['metadata'].get('name', 'restored')
    collection = client.get_or_create_collection(
        name=name,
        metadata=backup_data['metadata']
    )
    
    # Restore data in batches
    batch_size = 100
    ids = backup_data['ids']
    documents = backup_data['documents']
    metadatas = backup_data['metadatas']
    
    for i in range(0, len(ids), batch_size):
        collection.add(
            ids=ids[i:i+batch_size],
            documents=documents[i:i+batch_size],
            metadatas=metadatas[i:i+batch_size]
        )
    
    logger.info(f"Restored {len(ids)} documents to {name}")
    return collection
```

---

## Performance Optimization

### 1. Embedding Caching

```python
class CachedEmbeddingFunction:
    """Cache embeddings to avoid recomputation."""
    
    def __init__(self, base_function, cache_size=10000):
        self.base_function = base_function
        self.cache = {}
        self.cache_size = cache_size
    
    def __call__(self, texts):
        embeddings = []
        uncached_texts = []
        uncached_indices = []
        
        # Check cache
        for i, text in enumerate(texts):
            if text in self.cache:
                embeddings.append(self.cache[text])
            else:
                uncached_texts.append(text)
                uncached_indices.append(i)
                embeddings.append(None)  # Placeholder
        
        # Compute uncached embeddings
        if uncached_texts:
            new_embeddings = self.base_function(uncached_texts)
            
            # Update cache
            for text, embedding in zip(uncached_texts, new_embeddings):
                if len(self.cache) >= self.cache_size:
                    # Remove oldest entry
                    self.cache.pop(next(iter(self.cache)))
                self.cache[text] = embedding
            
            # Fill in placeholders
            for idx, new_emb in zip(uncached_indices, new_embeddings):
                embeddings[idx] = new_emb
        
        return embeddings
```

### 2. Batch Processing

```python
def process_large_dataset(collection, documents, batch_size=1000):
    """Process large datasets efficiently."""
    total = len(documents)
    
    for i in range(0, total, batch_size):
        batch = documents[i:i+batch_size]
        
        collection.add(
            documents=[d['text'] for d in batch],
            metadatas=[d['metadata'] for d in batch],
            ids=[d['id'] for d in batch]
        )
        
        # Progress tracking
        processed = min(i + batch_size, total)
        progress = (processed / total) * 100
        print(f"Progress: {processed}/{total} ({progress:.1f}%)")
```

### 3. Query Optimization

```python
# Use metadata filters to reduce search space
def optimized_search(collection, query, filters=None):
    """Perform optimized search."""
    
    # Start with broad metadata filter
    base_filters = filters or {}
    
    # Get initial candidates
    results = collection.query(
        query_texts=[query],
        where=base_filters,
        n_results=100  # Get more candidates
    )
    
    # Re-rank or post-process as needed
    return results
```

### 4. Index Optimization

```python
# Use appropriate distance metric
collection = client.create_collection(
    name="optimized",
    metadata={
        "hnsw:space": "cosine",  # Best for normalized embeddings
        "hnsw:construction_ef": 200,  # Higher = better recall, slower build
        "hnsw:search_ef": 100  # Higher = better recall, slower search
    }
)
```

### 5. Memory-Efficient Queries

```python
def memory_efficient_scan(collection, process_fn, batch_size=100):
    """Process all documents without loading everything into memory."""
    offset = 0
    
    while True:
        # Get batch
        results = collection.get(
            limit=batch_size,
            offset=offset,
            include=["documents", "metadatas"]
        )
        
        if not results['ids']:
            break
        
        # Process batch
        process_fn(results)
        
        offset += batch_size
        print(f"Processed {offset} documents")
```

---

## Common Use Cases

### 1. RAG (Retrieval-Augmented Generation) System

```python
import chromadb
from sentence_transformers import SentenceTransformer

class RAGSystem:
    """Simple RAG system using ChromaDB."""
    
    def __init__(self, collection_name="knowledge_base"):
        self.client = chromadb.PersistentClient(path="./rag_data")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        from chromadb.utils import embedding_functions
        self.ef = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.ef
        )
    
    def add_documents(self, documents, metadatas=None):
        """Add documents to knowledge base."""
        ids = [f"doc_{i}" for i in range(len(documents))]
        
        self.collection.add(
            documents=documents,
            metadatas=metadatas or [{} for _ in documents],
            ids=ids
        )
        print(f"Added {len(documents)} documents")
    
    def retrieve(self, query, n_results=5, filters=None):
        """Retrieve relevant documents for a query."""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results,
            where=filters
        )
        
        return {
            'documents': results['documents'][0],
            'metadatas': results['metadatas'][0],
            'distances': results['distances'][0]
        }
    
    def generate_prompt(self, query, context_docs):
        """Generate prompt with retrieved context."""
        context = "\n\n".join([
            f"Document {i+1}:\n{doc}"
            for i, doc in enumerate(context_docs)
        ])
        
        prompt = f"""Answer the question based on the following context:

Context:
{context}

Question: {query}

Answer:"""
        
        return prompt
    
    def answer_question(self, query, llm_client, n_results=5):
        """Complete RAG pipeline."""
        # Retrieve relevant documents
        retrieved = self.retrieve(query, n_results=n_results)
        
        # Generate prompt
        prompt = self.generate_prompt(query, retrieved['documents'])
        
        # Generate answer
        answer = llm_client.generate(prompt)
        
        return {
            'answer': answer,
            'sources': retrieved['metadatas'],
            'context': retrieved['documents']
        }

# Usage
rag = RAGSystem()

# Add knowledge
documents = [
    "Paris is the capital of France.",
    "The Eiffel Tower is located in Paris.",
    "France is in Western Europe."
]
metadatas = [
    {"source": "geography", "topic": "capitals"},
    {"source": "tourism", "topic": "landmarks"},
    {"source": "geography", "topic": "regions"}
]
rag.add_documents(documents, metadatas)

# Query
result = rag.answer_question(
    "What is the capital of France?",
    llm_client=your_llm_client
)
```

### 2. Semantic Search Engine

```python
class SemanticSearchEngine:
    """Semantic search engine for documents."""
    
    def __init__(self):
        self.client = chromadb.PersistentClient(path="./search_data")
        
        from chromadb.utils import embedding_functions
        self.ef = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-mpnet-base-v2"
        )
        
        self.collection = self.client.get_or_create_collection(
            name="documents",
            embedding_function=self.ef,
            metadata={"hnsw:space": "cosine"}
        )
    
    def index_documents(self, documents):
        """Index documents for search."""
        self.collection.add(
            documents=[d['content'] for d in documents],
            metadatas=[d['metadata'] for d in documents],
            ids=[d['id'] for d in documents]
        )
    
    def search(self, query, filters=None, n_results=10):
        """Search for documents."""
        results = self.collection.query(
            query_texts=[query],
            where=filters,
            n_results=n_results
        )
        
        # Format results
        formatted = []
        for i in range(len(results['ids'][0])):
            formatted.append({
                'id': results['ids'][0][i],
                'document': results['documents'][0][i],
                'metadata': results['metadatas'][0][i],
                'score': 1 - results['distances'][0][i]  # Convert distance to similarity
            })
        
        return formatted
    
    def suggest_similar(self, doc_id, n_results=5):
        """Find similar documents to a given document."""
        # Get the document
        doc = self.collection.get(ids=[doc_id])
        
        if not doc['documents']:
            return []
        
        # Search for similar
        results = self.collection.query(
            query_texts=doc['documents'],
            n_results=n_results + 1  # +1 because it will include itself
        )
        
        # Remove the document itself from results
        similar = []
        for i, id in enumerate(results['ids'][0]):
            if id != doc_id:
                similar.append({
                    'id': id,
                    'document': results['documents'][0][i],
                    'similarity': 1 - results['distances'][0][i]
                })
        
        return similar[:n_results]

# Usage
engine = SemanticSearchEngine()

# Index documents
docs = [
    {
        'id': 'doc1',
        'content': 'Machine learning is a subset of artificial intelligence',
        'metadata': {'category': 'AI', 'author': 'Alice'}
    },
    {
        'id': 'doc2',
        'content': 'Deep learning uses neural networks',
        'metadata': {'category': 'AI', 'author': 'Bob'}
    }
]
engine.index_documents(docs)

# Search
results = engine.search("What is AI?", n_results=5)

# Find similar documents
similar = engine.suggest_similar('doc1', n_results=3)
```

### 3. Document Q&A System

```python
class DocumentQA:
    """Question answering over documents."""
    
    def __init__(self):
        self.client = chromadb.PersistentClient(path="./qa_data")
        
        from chromadb.utils import embedding_functions
        self.ef = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="multi-qa-mpnet-base-dot-v1"  # Optimized for Q&A
        )
        
        self.collection = self.client.get_or_create_collection(
            name="qa_documents",
            embedding_function=self.ef
        )
    
    def load_document(self, doc_id, content, chunk_size=500):
        """Load and chunk a document."""
        # Split into chunks
        chunks = []
        for i in range(0, len(content), chunk_size):
            chunk = content[i:i+chunk_size]
            chunks.append({
                'text': chunk,
                'metadata': {
                    'doc_id': doc_id,
                    'chunk_index': i // chunk_size,
                    'start_char': i,
                    'end_char': i + len(chunk)
                }
            })
        
        # Add to collection
        self.collection.add(
            documents=[c['text'] for c in chunks],
            metadatas=[c['metadata'] for c in chunks],
            ids=[f"{doc_id}_chunk_{c['metadata']['chunk_index']}" for c in chunks]
        )
        
        return len(chunks)
    
    def ask(self, question, doc_id=None, n_context=3):
        """Ask a question about documents."""
        # Build filter
        where = {"doc_id": doc_id} if doc_id else None
        
        # Retrieve relevant chunks
        results = self.collection.query(
            query_texts=[question],
            where=where,
            n_results=n_context
        )
        
        # Combine chunks for context
        context = "\n\n".join(results['documents'][0])
        
        return {
            'context': context,
            'sources': results['metadatas'][0],
            'relevance_scores': [1 - d for d in results['distances'][0]]
        }

# Usage
qa = DocumentQA()

# Load a document
document = """
ChromaDB is an open-source embedding database.
It provides a simple API for storing and querying embeddings.
ChromaDB supports multiple embedding functions including OpenAI and Sentence Transformers.
"""
qa.load_document("chromadb_doc", document, chunk_size=100)

# Ask questions
result = qa.ask("What embedding functions does ChromaDB support?")
print(f"Context: {result['context']}")
```

### 4. Chatbot with Memory

```python
class ChatbotMemory:
    """Chatbot with long-term memory using ChromaDB."""
    
    def __init__(self, user_id):
        self.user_id = user_id
        self.client = chromadb.PersistentClient(path="./chat_memory")
        
        from chromadb.utils import embedding_functions
        self.ef = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        
        self.collection = self.client.get_or_create_collection(
            name="chat_history",
            embedding_function=self.ef
        )
        
        self.conversation_count = 0
    
    def add_exchange(self, user_message, bot_response, metadata=None):
        """Store a conversation exchange."""
        from datetime import datetime
        
        timestamp = datetime.now().isoformat()
        self.conversation_count += 1
        
        # Store both messages
        messages = [
            {
                'content': user_message,
                'role': 'user',
                'metadata': {
                    'user_id': self.user_id,
                    'timestamp': timestamp,
                    'conversation_id': self.conversation_count,
                    **(metadata or {})
                }
            },
            {
                'content': bot_response,
                'role': 'assistant',
                'metadata': {
                    'user_id': self.user_id,
                    'timestamp': timestamp,
                    'conversation_id': self.conversation_count,
                    **(metadata or {})
                }
            }
        ]
        
        self.collection.add(
            documents=[m['content'] for m in messages],
            metadatas=[m['metadata'] for m in messages],
            ids=[
                f"{self.user_id}_{self.conversation_count}_user",
                f"{self.user_id}_{self.conversation_count}_bot"
            ]
        )
    
    def recall_relevant(self, current_message, n_results=5):
        """Recall relevant past conversations."""
        results = self.collection.query(
            query_texts=[current_message],
            where={"user_id": self.user_id},
            n_results=n_results
        )
        
        # Format as conversation history
        history = []
        for i in range(len(results['ids'][0])):
            metadata = results['metadatas'][0][i]
            history.append({
                'role': metadata['role'],
                'content': results['documents'][0][i],
                'timestamp': metadata['timestamp'],
                'relevance': 1 - results['distances'][0][i]
            })
        
        return history
    
    def get_recent_history(self, n=10):
        """Get recent conversation history."""
        results = self.collection.get(
            where={"user_id": self.user_id},
            limit=n * 2  # User + bot messages
        )
        
        # Sort by timestamp
        exchanges = []
        for i in range(len(results['ids'])):
            exchanges.append({
                'role': results['metadatas'][i]['role'],
                'content': results['documents'][i],
                'timestamp': results['metadatas'][i]['timestamp']
            })
        
        exchanges.sort(key=lambda x: x['timestamp'], reverse=True)
        return exchanges[:n*2]

# Usage
memory = ChatbotMemory(user_id="user123")

# Store conversation
memory.add_exchange(
    user_message="What's the weather like?",
    bot_response="I don't have access to real-time weather data.",
    metadata={'topic': 'weather'}
)

# Later, recall relevant context
relevant_context = memory.recall_relevant("Tell me about the weather again")
```

---

## Troubleshooting

### Common Issues

#### Issue 1: "Collection already exists"

**Problem:**
```python
collection = client.create_collection("my_collection")
# Error: Collection my_collection already exists
```

**Solution:**
```python
# Use get_or_create
collection = client.get_or_create_collection("my_collection")

# Or delete first
try:
    client.delete_collection("my_collection")
except:
    pass
collection = client.create_collection("my_collection")
```

#### Issue 2: "Dimension mismatch"

**Problem:**
```
Embedding dimension mismatch: expected 384, got 768
```

**Solution:**
```python
# Ensure consistent embedding function
# All documents in a collection must use the same embedding function

# ✅ Correct
from chromadb.utils import embedding_functions

ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"  # 384 dimensions
)

collection = client.create_collection(
    name="consistent",
    embedding_function=ef
)

# All adds will use this same embedding function
```

#### Issue 3: Slow queries

**Problem:**
```
Queries taking too long to execute
```

**Solution:**
```python
# 1. Use metadata filters to reduce search space
results = collection.query(
    query_texts=["query"],
    where={"category": "relevant"},  # Pre-filter
    n_results=10
)

# 2. Reduce n_results if you don't need many
results = collection.query(
    query_texts=["query"],
    n_results=5  # Instead of 100
)

# 3. Use cosine distance for normalized embeddings
collection = client.create_collection(
    name="optimized",
    metadata={"hnsw:space": "cosine"}
)

# 4. Don't request embeddings if not needed
results = collection.query(
    query_texts=["query"],
    include=["documents", "metadatas"]  # Exclude embeddings
)
```

#### Issue 4: Out of memory

**Problem:**
```
MemoryError when loading large collections
```

**Solution:**
```python
# 1. Use persistent storage
client = chromadb.PersistentClient(path="./data")

# 2. Process in batches
def process_in_batches(collection, process_fn, batch_size=100):
    offset = 0
    while True:
        batch = collection.get(limit=batch_size, offset=offset)
        if not batch['ids']:
            break
        process_fn(batch)
        offset += batch_size

# 3. Use client-server mode for very large datasets
client = chromadb.HttpClient(host="localhost", port=8000)
```

#### Issue 5: "Embedding function not serializable"

**Problem:**
```
Can't persist collection with custom embedding function
```

**Solution:**
```python
# Use built-in embedding functions when possible
from chromadb.utils import embedding_functions

# ✅ These are serializable
ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# ❌ Custom functions may not be
class CustomEF:
    def __call__(self, texts):
        return custom_logic(texts)
```

### Debugging Tips

#### Enable Logging
```python
import logging

# Enable ChromaDB logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("chromadb")
logger.setLevel(logging.DEBUG)
```

#### Inspect Collection State
```python
# Check collection size
print(f"Documents in collection: {collection.count()}")

# Peek at first few documents
print(collection.peek(limit=3))

# Check metadata
print(f"Collection metadata: {collection.metadata}")
```

#### Validate Data
```python
def validate_collection_data(collection):
    """Validate collection for common issues."""
    data = collection.get()
    
    print(f"Total documents: {len(data['ids'])}")
    print(f"Unique IDs: {len(set(data['ids']))}")
    
    # Check for duplicates
    if len(data['ids']) != len(set(data['ids'])):
        print("WARNING: Duplicate IDs found!")
    
    # Check metadata consistency
    if data['metadatas']:
        keys = set()
        for metadata in data['metadatas']:
            keys.update(metadata.keys())
        print(f"Metadata keys used: {keys}")
    
    # Check embedding dimensions
    if data['embeddings']:
        dims = set(len(e) for e in data['embeddings'])
        print(f"Embedding dimensions: {dims}")
        if len(dims) > 1:
            print("WARNING: Inconsistent embedding dimensions!")

# Usage
validate_collection_data(collection)
```

---

## Conclusion

ChromaDB provides a powerful, flexible solution for managing embeddings in AI applications. By mastering CRUD operations, metadata filtering, and advanced features, you can build sophisticated semantic search, RAG systems, and more.

### Key Takeaways

1. **Start Simple**: Use in-memory mode for development, persistent for production
2. **Plan Your Schema**: Design metadata structure upfront
3. **Batch Operations**: Always use batch operations for better performance
4. **Use Metadata**: Leverage metadata filtering to improve relevance
5. **Choose Right Embedding**: Select embedding models based on your use case
6. **Monitor Performance**: Track query times and optimize as needed
7. **Test Thoroughly**: Validate your data and queries

### Next Steps

1. Experiment with different embedding models for your domain
2. Build a simple RAG system for your documents
3. Implement semantic search for your application
4. Set up production deployment with Docker
5. Optimize for your specific use case

### Additional Resources

- [ChromaDB Documentation](https://docs.trychroma.com/)
- [API Reference](https://docs.trychroma.com/reference)
- [GitHub Repository](https://github.com/chroma-core/chroma)
- [Discord Community](https://discord.gg/MMeYNTmh3x)

---

**Version:** 1.0.0  
**Last Updated:** February 2026  
**Author:** MicroDegree - Gen AI Developers Team