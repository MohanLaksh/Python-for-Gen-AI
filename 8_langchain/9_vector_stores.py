"""
8. Vector Stores — Index embeddings for fast semantic search
Based on LangChain v0.3 Components Guide

Popular backends:
- FAISS — in-memory, local (no server)
- Chroma — persistent, open-source (used in this example)
- Pinecone — managed cloud
"""
from dotenv import load_dotenv
load_dotenv()

from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# Sample documents
docs = [
    Document(page_content="LCEL is LangChain Expression Language. Use pipe | to compose.", metadata={"source": "lcel"}),
    Document(page_content="RAG combines retrieval with generation for better answers.", metadata={"source": "rag"}),
    Document(page_content="Embeddings convert text to vectors for similarity search.", metadata={"source": "emb"}),
]

try:
    from langchain_community.vectorstores import Chroma

    # Create ChromaDB vector store (persists automatically)
    vectorstore = Chroma.from_documents(
        docs,
        embeddings,
        persist_directory="./chroma_index",
        collection_name="vector_store_demo",
    )

    # Similarity search
    results = vectorstore.similarity_search("What is LCEL?", k=2)
    print("ChromaDB similarity search:")
    for r in results:
        print(" -", r.page_content)
        print("--------------------------------")

    # ChromaDB persists automatically, reload by creating new instance
    loaded = Chroma(
        persist_directory="./chroma_index",
        embedding_function=embeddings,
        collection_name="vector_store_demo",
    )
    reloaded_results = loaded.similarity_search("What is RAG?", k=1)
    print("Reloaded from disk:", reloaded_results[0].page_content[:50] + "...")
    print("Persisted and reloaded OK")

except ImportError:
    print("ChromaDB: pip install langchain-community chromadb")
