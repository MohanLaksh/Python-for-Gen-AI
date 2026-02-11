"""
6. Text Splitters — Chunk documents for LLM context windows
Based on LangChain v0.3 Components Guide

Common splitters:
- RecursiveCharacterTextSplitter — default, splits on ¶ → sentences → words
- TokenTextSplitter — split by token count
- MarkdownHeaderTextSplitter — preserve structure
"""
from langchain_core.documents import Document

# RecursiveCharacterTextSplitter — recommended default
try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    long_text = """
    LangChain is a framework for developing applications powered by language models.
    It enables applications that are context-aware and reasoning-aware.
    LCEL is the LangChain Expression Language for composing chains.
    Use the pipe operator to connect components.
    """ * 5

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=150,
        chunk_overlap=30,
        add_start_index=True,
    )
    chunks = splitter.split_text(long_text)
    print("RecursiveCharacterTextSplitter: split into", len(chunks), "chunks")
    for i, c in enumerate(chunks[:2]):
        print(f"  Chunk {i+1}:", repr(c[:60]) + "...")

    # With documents (preserves metadata)
    docs = [Document(page_content=long_text, metadata={"source": "guide"})]
    doc_chunks = splitter.split_documents(docs)
    print("Document chunks:", len(doc_chunks))
    print("First chunk metadata:", doc_chunks[0].metadata if doc_chunks else "N/A")

except ImportError:
    print("RecursiveCharacterTextSplitter: pip install langchain-text-splitters")
