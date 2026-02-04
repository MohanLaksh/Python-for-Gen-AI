import os
import chromadb
from chromadb.config import Settings
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
DATA_PATH = "data/faqs.txt"
CHROMA_PERSIST_DIR = "./chroma_db"
COLLECTION_NAME = "faqs"
EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_DIMENSIONS = 300
GENERATION_MODEL = "gpt-4o"
CHUNK_SIZE = 300
CHUNK_OVERLAP = 200
TOP_K_RETRIEVAL = 3

# Initialize OpenAI Client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize ChromaDB Client
chroma_client = chromadb.Client(
    Settings(
        persist_directory=CHROMA_PERSIST_DIR,
        anonymized_telemetry=True
    )
)

def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """
    Splits text into overlapping chunks.
    
    Args:
        text: The input text to split.
        chunk_size: The size of each chunk.
        overlap: The number of characters to overlap between chunks.
        
    Returns:
        A list of text chunks.
    """
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

def get_embeddings(text_list: list[str]) -> list[list[float]]:
    """
    Generates embeddings for a list of text strings using OpenAI.
    """
    response = client.embeddings.create(
        input=text_list, 
        model=EMBEDDING_MODEL, 
        dimensions=EMBEDDING_DIMENSIONS
    )
    return [e.embedding for e in response.data]

def setup_vector_db(docs_path: str):
    """
    Reads documents, chunks them, generates embeddings, and populates ChromaDB.
    """
    print("Loading documents...")
    with open(docs_path, "r") as f:
        content = f.read()

    # Create chunks
    chunks = chunk_text(content)
    print(f"Total chunks created: {len(chunks)}")
    if chunks:
        print(f"Sample chunk: {chunks[0][:100]}...") # Print first 100 chars of sample

    # Reset/Create Collection
    # Note: Using get_or_create_collection prevents errors if it explicitly exists 
    # but since we use an ephemeral/fresh client mostly, create_collection implies new.
    # To represent "simple" logic, we'll try to delete if exists or just create fresh name.
    # For now, we'll use get_or_create to be safe.
    try:
        chroma_client.delete_collection(name=COLLECTION_NAME)
    except Exception:
        pass
    
    collection = chroma_client.create_collection(name=COLLECTION_NAME)

    # Embed chunks
    print("Generating embeddings...")
    embeddings = get_embeddings(chunks)
    
    if embeddings:
        print(f"Embedding dimensions: {len(embeddings[0])}")

    # Add to collection
    print("Populating vector database...")
    collection.add(
        ids=[str(i) for i in range(len(chunks))],
        documents=chunks,
        embeddings=embeddings,
    )
    return collection

def retrieve_context(collection, query: str, k: int = TOP_K_RETRIEVAL) -> list[str]:
    """
    Retrieves relevant documents from ChromaDB based on query.
    """
    query_embedding = get_embeddings([query])[0]
    
    print(f"\nQuerying for: {query}")
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
    )
    
    top_docs = results['documents'][0]
    print(f"Top {k} Results found.")
    return top_docs

def generate_answer(query: str, context_docs: list[str]) -> str:
    """
    Generates an answer using the LLM with the provided context.
    """
    context_text = "\n\n".join(context_docs)
    print(f"\nRetrieved Context:\n{context_text}\n")
    
    prompt = f"""
    Answer the question using ONLY the content below strictly. If no relevent information is found in the context, say "I don't know".
    Context: {context_text}
    Question: {query}
    """
    
    response = client.chat.completions.create(
        model=GENERATION_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    return response.choices[0].message.content

def main():
    print("--- Simple RAG System Initializing ---")
    
    # Setup
    collection = setup_vector_db(DATA_PATH)
    print("--- System Ready ---\n")

    # Interactive Loop
    while True:
        try:
            user_input = input("Enter your question (or 'exit' to quit): ").strip()
            if user_input.lower() in ['exit', 'quit']:
                print("Exiting...")
                break
            if not user_input:
                continue
            
            # Application Logic
            contexts = retrieve_context(collection, user_input)
            answer = generate_answer(user_input, contexts)
            
            print(f"\nAI Answer:\n{answer}\n")
            print("-" * 50)
            
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()