"""
8. Vector Stores — Index embeddings for fast semantic search
Based on LangChain v0.3 Components Guide

Popular backends:
- FAISS — in-memory, local (no server)
- Chroma — persistent, open-source
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
    from langchain_community.vectorstores import FAISS

    vectorstore = FAISS.from_documents(docs, embeddings)

    # Similarity search
    results = vectorstore.similarity_search("What is LCEL?", k=2)
    print("FAISS similarity search:")
    for r in results:
        print(" -", r.page_content[:60] + "...")

    # Persist and reload
    vectorstore.save_local("faiss_index")
    loaded = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    print("Persisted and reloaded OK")

except ImportError:
    print("FAISS: pip install langchain-community faiss-cpu")
