# FAQ RAG Project

A simple Retrieval-Augmented Generation (RAG) implementation using **ChromaDB** for vector storage and **OpenAI** (GPT-4o) for generation.

## Features
- **Document Chunking**: Splits text into overlapping chunks.
- **Vector Embeddings**: Uses `text-embedding-3-small` (custom dimensions support).
- **Semantic Search**: Retrieves relevant context based on user queries.
- **RAG Pipeline**: Generates answers using retrieved context + GPT-4o.
- **Interactive Mode**: Allows asking questions via command line.

## Prerequisites
- Python 3.10+
- OpenAI API Key

## Setup

1. **Clone the repository** (if applicable).
2. **Install dependencies**:
   ```sh
   pip install -r requirements.txt
   ```
3. **Configure Environment**:
   Create a `.env` file in the root directory and add your OpenAI API key:
   ```env
   OPENAI_API_KEY=sk-your-api-key-here
   ```

## Usage

Run the main script:
```sh
python main.py
```

- The script will ingest `data/faqs.txt`.
- It will create embeddings and store them in an in-memory ChromaDB instance.
- You will be prompted to enter a question.
- Type `exit` or `quit` to stop.

## File Structure
- `main.py`: Core logic for RAG (chunking, embedding, retrieval, generation).
- `data/faqs.txt`: Source knowledge base.
- `requirements.txt`: Python dependencies.

## How it Works

The system operates in two main stages: Retrieval and Generation.

### 1. Retrieval (Vector Search)
*   **Ingestion**: The text from `data/faqs.txt` is split into smaller overlapping "chunks" (e.g., 300 characters).
*   **Embedding**: Each chunk is converted into a list of numbers (a vector) using OpenAI's `text-embedding-3-small` model. These vectors capture the *semantic meaning* of the text.
*   **Storage**: These vectors are stored in **ChromaDB**.
*   **Search**: When you ask a question, it is also converted into a vector. ChromaDB finds the "nearest neighbors" (most similar chunks) to your question vector.

### 2. Presentation (Generation)
*   **Context Assembly**: The best matching chunks are combined into a single text block called "Context".
*   **Prompting**: A structured prompt is sent to GPT-4o:
    > "Answer the question using ONLY the content below... Context: {retrieved_text} Question: {user_query}"
*   **Response**: The LLM generates a natural language answer based *strictly* on the provided context, reducing hallucinations.

## Example Questions

Try these questions to see how the system retrieves specific data:

*   **Free Courses**: *"What free courses are available?"*
*   **Pricing**: *"How much is the AWS course?"*
*   **Curriculum**: *"What is covered in the Web Development curriculum?"*
*   **Comparisons**: *"What is the difference between individual courses and MicroDegree Pro?"*
*   **Support**: *"Do you offer placement assistance?"*

## Available Embedding Models

This project uses `text-embedding-3-small` by default for efficiency. You can switch to other OpenAI embedding models by modifying the `EMBEDDING_MODEL` constant in `main.py`.

### 1. **text-embedding-3-small** (Default)
*   **Performance**: High efficiency, lower cost.
*   **Dimensions**: 1536 (default), but we use 300 to optimize storage.
*   **Best for**: Fast retrieval, general-purpose applications.

### 2. **text-embedding-3-large**
*   **Performance**: Higher accuracy than "small".
*   **Dimensions**: 3072 (default).
*   **Best for**: Complex semantic tasks where nuance is critical.

### 3. **text-embedding-ada-002**
*   **Performance**: Legacy standard.
*   **Dimensions**: 1536.
*   **Best for**: Backward compatibility with older systems.

> **Note**: If you change the model, you must delete the existing `chroma_db` folder to regenerate embeddings with the new model.

## Local Embeddings (Sentence Transformers)

If you prefer to run embeddings locally (no API cost, works offline) instead of using OpenAI, you can use **Sentence Transformers**.

### 1. Install Dependencies
```sh
pip install sentence-transformers
```

### 2. Update `main.py`
Replace the `get_embeddings` function and initialization to use `SentenceTransformer`:

```python
from sentence_transformers import SentenceTransformer

# Initialize
embedding_model = SentenceTransformer('all-MiniLM-L6-v2') 

def get_embeddings(text_list: list[str]) -> list[list[float]]:
    """
    Generates embeddings locally using Sentence Transformers.
    """
    embeddings = embedding_model.encode(text_list)
    return embeddings.tolist()
```

### 3. Recommended Model
*   **Model**: `all-MiniLM-L6-v2`
*   **Dimensions**: 384
*   **Performance**: Excellent balance of speed and accuracy for CPU inference.

