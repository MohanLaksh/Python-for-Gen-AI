"""
7. Embeddings — Transform text into dense numeric vectors
Based on LangChain v0.3 Components Guide

Common providers:
- OpenAIEmbeddings — text-embedding-3-small / text-embedding-3-large
- HuggingFaceEmbeddings — local open-source
- GoogleGenerativeAIEmbeddings — Gemini models
"""
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# Embed a single query
query_vector = embeddings.embed_query("What is RAG?")
print("Query vector length:", len(query_vector))
print("First 5 dims:", query_vector[:5])

# Embed multiple documents
texts = [
    "RAG is retrieval-augmented generation.",
    "LCEL is LangChain's pipe syntax.",
]
doc_vectors = embeddings.embed_documents(texts)
print("Documents embedded:", len(doc_vectors), "x", len(doc_vectors[0]), "dims")
