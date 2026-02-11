"""
5. Document Loaders — Ingest content from diverse sources
Based on LangChain v0.3 Components Guide

Common loaders:
- PyPDFLoader — PDF files
- TextLoader — plain text files
- WebBaseLoader — web scraping
- CSVLoader — one Document per row
- DirectoryLoader — bulk loading

Requires: pip install langchain-community
"""
from pathlib import Path

# TextLoader — plain text
try:
    from langchain_community.document_loaders import TextLoader

    text_loader = TextLoader("sample.txt")
    docs = text_loader.load()
    print("TextLoader:", docs[0].page_content[:100] + "...")
    print("Metadata:", docs[0].metadata)
except ImportError:
    print("TextLoader: pip install langchain-community")

# PyPDFLoader — requires: pip install pypdf langchain-community
try:
    from langchain_community.document_loaders import PyPDFLoader
    # Use a PDF if available; otherwise skip
    pdf_path = Path("sample.pdf")
    if pdf_path.exists():
        pdf_loader = PyPDFLoader(str(pdf_path))
        pdf_docs = pdf_loader.load()
        print("PyPDFLoader:", pdf_docs[0].page_content[:100] if pdf_docs else "empty")
    else:
        print("PyPDFLoader: (create sample.pdf to test)")
except ImportError:
    print("PyPDFLoader: pip install langchain-community pypdf")

# WebBaseLoader — requires: pip install beautifulsoup4 langchain-community
try:
    from langchain_community.document_loaders import WebBaseLoader
    loader = WebBaseLoader("https://python.langchain.com")
    web_docs = loader.load()
    print("WebBaseLoader:", web_docs[0].page_content[:150] + "..." if web_docs else "empty")
except ImportError:
    print("WebBaseLoader: pip install langchain-community beautifulsoup4")
except Exception as e:
    print("WebBaseLoader: (network/config)", str(e)[:80])

# DirectoryLoader — bulk load
try:
    from langchain_community.document_loaders import DirectoryLoader
    dir_loader = DirectoryLoader(".", glob="*.txt", loader_cls=TextLoader)
    all_docs = dir_loader.load()
    print("DirectoryLoader: loaded", len(all_docs), "txt files")
except ImportError:
    print("DirectoryLoader: pip install langchain-community")
