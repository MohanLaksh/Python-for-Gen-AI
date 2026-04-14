"""
Assignment 2: Multi-Source Research Assistant with Branching Chains
====================================================================
Topics covered:
  - Multi-source document loading (DirectoryLoader, WikipediaLoader, PythonLoader)
  - Adaptive text splitting (MarkdownHeader, PythonCode, RecursiveCharacter)
  - Two LCEL sub-chains (summarise + extract)
  - RunnableLambda router
  - RunnableParallel merge
  - Fallback chains with .with_fallbacks()
"""

import os
import json
from pathlib import Path

# ── LangChain imports ────────────────────────────────────────────────────────
from langchain_community.document_loaders import (
    DirectoryLoader,
    TextLoader,
    PythonLoader,
)
from langchain_community.document_loaders import WikipediaLoader

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    MarkdownHeaderTextSplitter,
    PythonCodeTextSplitter,
)

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.runnables import RunnableLambda, RunnableParallel

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

# ─────────────────────────────────────────────────────────────────────────────
# SETUP: create sample files so the assignment runs without external data
# ─────────────────────────────────────────────────────────────────────────────

def create_sample_files():
    """Create sample .txt, .md, and .py files for the DirectoryLoader."""

    os.makedirs("sample_docs", exist_ok=True)

    # Plain text file
    Path("sample_docs/history.txt").write_text(
        "The Python programming language was created by Guido van Rossum "
        "and first released in 1991. It emphasises code readability and "
        "supports multiple programming paradigms including procedural, "
        "object-oriented, and functional programming. Python 3.0 was "
        "released in December 2008 and introduced several backward-"
        "incompatible changes. Today, Python is one of the most popular "
        "programming languages in the world, used extensively in data "
        "science, web development, and artificial intelligence."
    )

    # Markdown file
    Path("sample_docs/guide.md").write_text(
        "# Introduction\n\n"
        "LangChain is a framework for building LLM-powered applications.\n\n"
        "## Core Concepts\n\n"
        "LCEL (LangChain Expression Language) lets you compose chains using "
        "the pipe operator. It supports streaming, batching, and async.\n\n"
        "## Document Loaders\n\n"
        "Document loaders ingest data from PDFs, web pages, databases, and "
        "more. Each loader returns a list of Document objects with "
        "page_content and metadata.\n\n"
        "## Text Splitters\n\n"
        "Text splitters divide large documents into smaller chunks that fit "
        "within an LLM context window. Common splitters include "
        "RecursiveCharacterTextSplitter and TokenTextSplitter."
    )

    # Python file
    Path("sample_docs/utils.py").write_text(
        '"""Utility functions for data processing."""\n\n'
        "def clean_text(text: str) -> str:\n"
        '    """Remove extra whitespace from text."""\n'
        "    return ' '.join(text.split())\n\n"
        "def chunk_list(lst: list, size: int) -> list:\n"
        '    """Split a list into chunks of given size."""\n'
        "    return [lst[i:i+size] for i in range(0, len(lst), size)]\n\n"
        "def count_tokens(text: str) -> int:\n"
        '    """Approximate token count (words / 0.75)."""\n'
        "    return int(len(text.split()) / 0.75)\n"
    )

    print("✅ Sample files created in ./sample_docs/")


# ─────────────────────────────────────────────────────────────────────────────
# TASK 1 — Multi-Source Loading
# ─────────────────────────────────────────────────────────────────────────────

def task1_load_documents():
    """
    Load documents from three different sources and print metadata.
    Returns a combined list of Document objects.
    """
    print("\n" + "="*60)
    print("TASK 1 — Multi-Source Document Loading")
    print("="*60)

    all_docs = []

    # ── 1a. DirectoryLoader — loads all .txt files ──────────────────────────
    print("\n📁 Loading from DirectoryLoader (*.txt) ...")
    dir_loader = DirectoryLoader(
        path="./sample_docs",
        glob="**/*.txt",        # only .txt files
        loader_cls=TextLoader,
        show_progress=True,
    )
    dir_docs = dir_loader.load()
    all_docs.extend(dir_docs)

    for doc in dir_docs:
        print(f"   source  : {doc.metadata.get('source')}")
        print(f"   length  : {len(doc.page_content)} chars")

    # ── 1b. WikipediaLoader ─────────────────────────────────────────────────
    print("\n🌐 Loading from WikipediaLoader (topic: LangChain) ...")
    wiki_loader = WikipediaLoader(query="LangChain AI framework", load_max_docs=1)
    wiki_docs = wiki_loader.load()
    all_docs.extend(wiki_docs)

    for doc in wiki_docs:
        print(f"   source  : {doc.metadata.get('source')}")
        print(f"   title   : {doc.metadata.get('title')}")
        print(f"   length  : {len(doc.page_content)} chars")

    # ── 1c. PythonLoader — loads .py file ───────────────────────────────────
    print("\n🐍 Loading from PythonLoader (utils.py) ...")
    py_loader = PythonLoader("./sample_docs/utils.py")
    py_docs = py_loader.load()
    all_docs.extend(py_docs)

    for doc in py_docs:
        print(f"   source  : {doc.metadata.get('source')}")
        print(f"   length  : {len(doc.page_content)} chars")

    print(f"\n✅ Total documents loaded: {len(all_docs)}")
    return all_docs


# ─────────────────────────────────────────────────────────────────────────────
# TASK 2 — Adaptive Text Splitting
# ─────────────────────────────────────────────────────────────────────────────

def split_by_type(doc):
    """
    Choose the right splitter based on the document's source file extension.
      .md  → MarkdownHeaderTextSplitter
      .py  → PythonCodeTextSplitter
      else → RecursiveCharacterTextSplitter
    """
    source = doc.metadata.get("source", "")

    if source.endswith(".md"):
        print(f"   → Using MarkdownHeaderTextSplitter for: {source}")
        splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=[
                ("#",  "Header1"),
                ("##", "Header2"),
            ]
        )
        # MarkdownHeaderTextSplitter works directly on text
        chunks = splitter.split_text(doc.page_content)

    elif source.endswith(".py"):
        print(f"   → Using PythonCodeTextSplitter for: {source}")
        splitter = PythonCodeTextSplitter(chunk_size=300, chunk_overlap=30)
        chunks = splitter.split_documents([doc])

    else:
        print(f"   → Using RecursiveCharacterTextSplitter for: {source}")
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=400,
            chunk_overlap=50,
        )
        chunks = splitter.split_documents([doc])

    return chunks


def task2_adaptive_splitting(all_docs):
    """
    Apply split_by_type() to every document.
    Returns a flat list of all chunks with their metadata preserved.
    """
    print("\n" + "="*60)
    print("TASK 2 — Adaptive Text Splitting")
    print("="*60 + "\n")

    all_chunks = []

    for doc in all_docs:
        chunks = split_by_type(doc)
        all_chunks.extend(chunks)
        print(f"   chunks produced: {len(chunks)}\n")

    print(f"✅ Total chunks after splitting: {len(all_chunks)}")
    return all_chunks


# ─────────────────────────────────────────────────────────────────────────────
# TASK 3 — Build Two Sub-Chains
# ─────────────────────────────────────────────────────────────────────────────

def build_chains():
    """
    Build summarise_chain and extract_chain using LCEL pipe operator.
    Each chain: ChatPromptTemplate | ChatModel | OutputParser
    """
    print("\n" + "="*60)
    print("TASK 3 — Building Sub-Chains")
    print("="*60)

    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

    # ── Fallback chains (returned on error) ─────────────────────────────────
    fallback_summarise = RunnableLambda(
        lambda _: "⚠️ Summarisation failed — empty or invalid input."
    )
    fallback_extract = RunnableLambda(
        lambda _: []   # JsonOutputParser expects a list
    )

    # ── Summarise chain ──────────────────────────────────────────────────────
    summarise_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a concise summariser. Respond with exactly 3 bullet points."),
        ("human",  "Summarise this text:\n\n{text}"),
    ])

    summarise_chain = (
        summarise_prompt
        | llm
        | StrOutputParser()
    ).with_fallbacks([fallback_summarise])

    # ── Extract chain ────────────────────────────────────────────────────────
    extract_prompt = ChatPromptTemplate.from_messages([
        ("system",
         "You are an information extractor. "
         "Return ONLY a valid JSON object with keys: "
         "'proper_nouns', 'dates', 'numbers'. "
         "Each key maps to a list of strings. No extra text."),
        ("human", "Extract from this text:\n\n{text}"),
    ])

    extract_chain = (
        extract_prompt
        | llm
        | JsonOutputParser()
    ).with_fallbacks([fallback_extract])

    print("   ✅ summarise_chain built  (Prompt | LLM | StrOutputParser)")
    print("   ✅ extract_chain built    (Prompt | LLM | JsonOutputParser)")
    print("   ✅ Fallbacks attached to both chains")

    return summarise_chain, extract_chain


# ─────────────────────────────────────────────────────────────────────────────
# TASK 4 — RunnableLambda Router
# ─────────────────────────────────────────────────────────────────────────────

def build_router(summarise_chain, extract_chain):
    """
    RunnableLambda wraps a plain Python function.
    The function receives the full input dict and RETURNS a chain.
    LangChain then calls .invoke() on that returned chain with the same input.
    """
    def route(input: dict):
        mode = input.get("mode", "summarise")
        if mode == "summarise":
            return summarise_chain
        else:
            return extract_chain

    router = RunnableLambda(route)
    print("\n   ✅ RunnableLambda router built")
    return router


def task4_router_demo(router, sample_text):
    """Test the router with both modes on the same text."""
    print("\n" + "="*60)
    print("TASK 4 — RunnableLambda Router Demo")
    print("="*60)

    print("\n📋 Mode: summarise")
    print("-" * 40)
    result = router.invoke({"mode": "summarise", "text": sample_text})
    print(result)

    print("\n🔍 Mode: extract")
    print("-" * 40)
    result = router.invoke({"mode": "extract", "text": sample_text})
    print(json.dumps(result, indent=2))


# ─────────────────────────────────────────────────────────────────────────────
# TASK 5 — RunnableParallel Merge
# ─────────────────────────────────────────────────────────────────────────────

def task5_parallel_merge(summarise_chain, extract_chain, sample_text):
    """
    Run both chains simultaneously on the same input.
    RunnableParallel executes them concurrently and merges into one dict.
    Output: { "summary": "...", "entities": {...} }
    """
    print("\n" + "="*60)
    print("TASK 5 — RunnableParallel Merge")
    print("="*60)

    parallel_chain = RunnableParallel(
        summary=summarise_chain,
        entities=extract_chain,
    )

    print("\n⚡ Running both chains in parallel on the same chunk...")
    result = parallel_chain.invoke({"text": sample_text})

    print("\n📦 Merged Output:")
    print("-" * 40)
    print("SUMMARY:")
    print(result["summary"])
    print("\nENTITIES:")
    print(json.dumps(result["entities"], indent=2))

    return result


# ─────────────────────────────────────────────────────────────────────────────
# TASK 6 — Fallback Demo
# ─────────────────────────────────────────────────────────────────────────────

def task6_fallback_demo(summarise_chain, extract_chain):
    """
    Verify fallbacks work by passing an empty string.
    The LLM may error or return unusable output; fallback catches it.

    We demonstrate by deliberately breaking the chain with a
    RunnableLambda that always raises, then calling .with_fallbacks().
    """
    print("\n" + "="*60)
    print("TASK 6 — Fallback Chain Demo")
    print("="*60)

    # Create a chain that always fails
    def always_fail(input):
        raise ValueError("Simulated chain failure!")

    broken_chain = RunnableLambda(always_fail)

    # Attach summarise_chain as fallback
    safe_chain = broken_chain.with_fallbacks([summarise_chain])

    print("\n💥 Invoking a broken chain (will trigger fallback) ...")
    result = safe_chain.invoke({
        "text": "Python was created by Guido van Rossum in 1991."
    })

    print("✅ Fallback activated — got result from summarise_chain:")
    print(result)


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    print("╔══════════════════════════════════════════════════════════╗")
    print("║   Assignment 2 — Multi-Source Research Assistant         ║")
    print("╚══════════════════════════════════════════════════════════╝")

    # ── Setup sample files ───────────────────────────────────────────────────
    create_sample_files()

    # ── Task 1: Load documents ───────────────────────────────────────────────
    all_docs = task1_load_documents()

    # ── Task 2: Adaptive splitting ───────────────────────────────────────────
    all_chunks = task2_adaptive_splitting(all_docs)

    print("all_chunks", all_chunks)

    # ── Tasks 3–6 require OpenAI key ─────────────────────────────────────────
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  OPENAI_API_KEY not set.")
        print("   Tasks 3–6 require a valid API key.")
        print("   Set it with:  export OPENAI_API_KEY='sk-...'")
        return

    # Pick a representative chunk as sample text
    sample_text = all_chunks[0].page_content if all_chunks else (
        "Python was created by Guido van Rossum and released in 1991. "
        "It is widely used in AI and data science."
    )

    print(f"\n📝 Sample text for chain demos:\n   {sample_text[:120]}...")

    # ── Task 3: Build chains ─────────────────────────────────────────────────
    summarise_chain, extract_chain = build_chains()

    # ── Task 4: Router demo ──────────────────────────────────────────────────
    router = build_router(summarise_chain, extract_chain)
    task4_router_demo(router, sample_text)

    # ── Task 5: Parallel merge ───────────────────────────────────────────────
    task5_parallel_merge(summarise_chain, extract_chain, sample_text)

    # ── Task 6: Fallback demo ────────────────────────────────────────────────
    task6_fallback_demo(summarise_chain, extract_chain)

    print("\n\n✅ Assignment 2 complete!")


if __name__ == "__main__":
    main()