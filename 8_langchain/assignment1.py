"""
Assignment 1: Multi-Format Document Processor
==============================================
Topics covered:
  - Document loading  : PyPDFLoader, TextLoader, WebBaseLoader
  - Text splitting    : RecursiveCharacterTextSplitter, CharacterTextSplitter
  - LCEL chain        : ChatPromptTemplate | ChatModel | StrOutputParser
  - Invocation modes  : .invoke()  |  .stream()  |  .batch()
"""

import os
import time
from pathlib import Path

# ── LangChain imports ────────────────────────────────────────────────────────
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    WebBaseLoader,
)
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    CharacterTextSplitter,
)
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI


# ─────────────────────────────────────────────────────────────────────────────
# SETUP — create sample files so the assignment runs without external data
# ─────────────────────────────────────────────────────────────────────────────

def create_sample_files():
    """
    Creates a sample .txt file used by TextLoader.
    For PyPDFLoader a real PDF path is needed — we fall back to TextLoader
    if no PDF is available, so the rest of the assignment still runs.
    """
    os.makedirs("sample_docs", exist_ok=True)

    Path("sample_docs/ai_overview.txt").write_text(
        "Artificial Intelligence (AI) refers to the simulation of human "
        "intelligence processes by computer systems. These processes include "
        "learning, reasoning, and self-correction.\n\n"
        "Machine Learning (ML) is a subset of AI that enables systems to "
        "learn from data without being explicitly programmed. Key algorithms "
        "include linear regression, decision trees, and neural networks.\n\n"
        "Deep Learning is a further subset of ML that uses multi-layered "
        "neural networks. It powers breakthroughs in image recognition, "
        "natural language processing, and speech synthesis.\n\n"
        "Large Language Models (LLMs) such as GPT-4, Claude, and Gemini are "
        "trained on massive text corpora. They can generate, summarise, "
        "translate, and reason over text with remarkable fluency.\n\n"
        "Retrieval-Augmented Generation (RAG) combines LLMs with external "
        "knowledge bases. A retriever fetches relevant documents; the LLM "
        "then uses them as context to produce grounded, accurate answers.\n\n"
        "Prompt Engineering is the practice of crafting inputs to LLMs in "
        "order to guide their outputs. Techniques include zero-shot, "
        "few-shot, chain-of-thought, and role prompting.\n\n"
        "Ethical AI considers fairness, accountability, transparency, and "
        "privacy in AI systems. Bias in training data can propagate into "
        "model predictions with harmful real-world consequences.\n\n"
        "The future of AI includes multimodal models that process text, "
        "images, audio, and video simultaneously. Autonomous AI agents that "
        "plan and execute multi-step tasks are an active research frontier."
    )

    print("✅ Sample files created in ./sample_docs/")


# ─────────────────────────────────────────────────────────────────────────────
# TASK 1 — Document Loading
# ─────────────────────────────────────────────────────────────────────────────

def task1_load_documents():
    """
    Load documents from three different sources:
      1. PyPDFLoader    — PDF file  (falls back to TextLoader if no PDF found)
      2. TextLoader     — plain .txt file
      3. WebBaseLoader  — Wikipedia article URL

    Prints page_content (first 200 chars) and metadata for each document.
    Returns a combined list of Document objects.
    """
    print("\n" + "=" * 60)
    print("TASK 1 — Document Loading")
    print("=" * 60)

    all_docs = []

    # ── 1a. PyPDFLoader ──────────────────────────────────────────────────────
    # Change PDF_PATH to point to a real PDF on your machine.
    PDF_PATH = "sample_docs/sample.pdf"

    print("\n📄 Loading PDF ...")
    if os.path.exists(PDF_PATH):
        pdf_loader = PyPDFLoader(PDF_PATH)
        pdf_docs = pdf_loader.load()
        all_docs.extend(pdf_docs)
        for i, doc in enumerate(pdf_docs):
            print(f"   [PDF page {i+1}]")
            print(f"   source   : {doc.metadata.get('source')}")
            print(f"   page     : {doc.metadata.get('page')}")
            print(f"   preview  : {doc.page_content[:200].strip()!r}")
    else:
        print(f"   ⚠️  No PDF found at '{PDF_PATH}'.")
        print("   → Falling back to TextLoader for demo purposes.")
        fallback_loader = TextLoader("sample_docs/ai_overview.txt")
        fallback_docs = fallback_loader.load()
        # Mark them so we can distinguish during splitting
        for doc in fallback_docs:
            doc.metadata["source"] = PDF_PATH + " (fallback)"
        all_docs.extend(fallback_docs)
        print(f"   Loaded {len(fallback_docs)} fallback document(s).")

    # ── 1b. TextLoader ───────────────────────────────────────────────────────
    print("\n📃 Loading plain text file ...")
    txt_loader = TextLoader("sample_docs/ai_overview.txt", encoding="utf-8")
    txt_docs = txt_loader.load()
    all_docs.extend(txt_docs)

    for doc in txt_docs:
        print(f"   source   : {doc.metadata.get('source')}")
        print(f"   length   : {len(doc.page_content)} chars")
        print(f"   preview  : {doc.page_content[:200].strip()!r}")

    # ── 1c. WebBaseLoader ────────────────────────────────────────────────────
    print("\n🌐 Loading web page ...")
    url = "https://en.wikipedia.org/wiki/Artificial_intelligence"
    web_loader = WebBaseLoader(url)
    web_docs = web_loader.load()
    all_docs.extend(web_docs)

    for doc in web_docs:
        print(f"   source   : {doc.metadata.get('source')}")
        print(f"   title    : {doc.metadata.get('title', 'N/A')}")
        print(f"   length   : {len(doc.page_content)} chars")
        print(f"   preview  : {doc.page_content[:200].strip()!r}")

    print(f"\n✅ Total documents loaded: {len(all_docs)}")
    return all_docs


# ─────────────────────────────────────────────────────────────────────────────
# TASK 2 — Text Splitting + Comparison
# ─────────────────────────────────────────────────────────────────────────────

def task2_text_splitting(all_docs):
    """
    Apply two splitters to the same documents and compare results.

    RecursiveCharacterTextSplitter:
      Tries to split on paragraphs → sentences → words in order,
      so chunks preserve natural boundaries.

    CharacterTextSplitter:
      Splits only on a single separator (default: '\\n\\n').
      Chunks can be uneven; may exceed chunk_size if separator is rare.

    Prints chunk counts and 3 observations. Returns recursive chunks.
    """
    print("\n" + "=" * 60)
    print("TASK 2 — Text Splitting & Comparison")
    print("=" * 60)

    CHUNK_SIZE    = 500
    CHUNK_OVERLAP = 50

    # ── Splitter A: RecursiveCharacterTextSplitter ───────────────────────────
    recursive_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],  # priority order
    )
    recursive_chunks = recursive_splitter.split_documents(all_docs)

    # ── Splitter B: CharacterTextSplitter ────────────────────────────────────
    character_splitter = CharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separator="\n\n",   # splits ONLY on double newline
    )
    character_chunks = character_splitter.split_documents(all_docs)

    # ── Comparison table ─────────────────────────────────────────────────────
    print(f"\n{'Metric':<40} {'Recursive':>12} {'Character':>12}")
    print("-" * 66)
    print(f"{'Total chunks':<40} {len(recursive_chunks):>12} {len(character_chunks):>12}")

    rec_sizes = [len(c.page_content) for c in recursive_chunks]
    cha_sizes = [len(c.page_content) for c in character_chunks]

    print(f"{'Avg chunk size (chars)':<40} {sum(rec_sizes)//len(rec_sizes):>12} {sum(cha_sizes)//len(cha_sizes):>12}")
    print(f"{'Max chunk size (chars)':<40} {max(rec_sizes):>12} {max(cha_sizes):>12}")
    print(f"{'Min chunk size (chars)':<40} {min(rec_sizes):>12} {min(cha_sizes):>12}")
    over_rec = sum(1 for s in rec_sizes if s > CHUNK_SIZE)
    over_cha = sum(1 for s in cha_sizes if s > CHUNK_SIZE)
    print(f"{'Chunks exceeding chunk_size':<40} {over_rec:>12} {over_cha:>12}")

    # ── 3 Observations ───────────────────────────────────────────────────────
    print("\n📝 Observations:")
    print(
        "  1. RecursiveCharacterTextSplitter produces MORE chunks because it "
        "aggressively breaks on multiple separators, keeping each chunk "
        "within the size limit. CharacterTextSplitter only splits on "
        "'\\n\\n', so if a paragraph is long, the chunk exceeds chunk_size."
    )
    print(
        "  2. RecursiveCharacterTextSplitter has a lower max chunk size — "
        "it never breaches the limit as long as a valid separator exists. "
        "CharacterTextSplitter can produce chunks well above chunk_size "
        "when the document has long paragraphs with no double newline."
    )
    print(
        "  3. The chunk_overlap setting creates a small content overlap "
        "between consecutive chunks in both splitters. This ensures that "
        "a sentence spanning a chunk boundary is not lost — it appears "
        "at the end of one chunk AND the start of the next."
    )

    # Preview first 2 recursive chunks
    print("\n🔍 First 2 recursive chunks (preview):")
    for i, chunk in enumerate(recursive_chunks[:2]):
        print(f"\n  [Chunk {i+1}]  {len(chunk.page_content)} chars")
        print(f"  {chunk.page_content[:180].strip()!r}")

    print(f"\n✅ Using {len(recursive_chunks)} recursive chunks for Tasks 3–5.")
    return recursive_chunks


# ─────────────────────────────────────────────────────────────────────────────
# TASK 3 — LCEL Chain Construction
# ─────────────────────────────────────────────────────────────────────────────

def build_chain():
    """
    Build the LCEL chain:
      ChatPromptTemplate | ChatModel | StrOutputParser

    The prompt has:
      - A system message defining the assistant's role
      - A human message with the {text} placeholder

    .invoke() / .stream() / .batch() all accept {"text": "..."}
    """
    print("\n" + "=" * 60)
    print("TASK 3 — LCEL Chain Construction")
    print("=" * 60)

    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "You are a document analyst. Your job is to read a passage "
            "and produce a clear, concise summary in 2–3 sentences. "
            "Focus on the key idea. Do not add information not in the text."
        ),
        (
            "human",
            "Please summarise the following passage:\n\n{text}"
        ),
    ])

    chain = prompt | llm | StrOutputParser()

    print("\n   Chain structure:")
    print("   ChatPromptTemplate  →  ChatOpenAI  →  StrOutputParser")
    print("   (system + human {text})  (gpt-3.5-turbo)  (plain string)")
    print("\n✅ Chain built successfully.")
    return chain


# ─────────────────────────────────────────────────────────────────────────────
# TASK 4 — Batch Processing (.batch)
# ─────────────────────────────────────────────────────────────────────────────

def task4_batch(chain, chunks):
    """
    Pass the first 5 chunks to the chain using .batch().
    .batch() sends all inputs concurrently and returns a list of results
    in the same order as the inputs.
    """
    print("\n" + "=" * 60)
    print("TASK 4 — Batch Processing  (.batch)")
    print("=" * 60)

    # Take first 5 chunks (or fewer if not enough)
    batch_inputs = [
        {"text": chunk.page_content}
        for chunk in chunks[:5]
    ]

    print(f"\n⚡ Sending {len(batch_inputs)} chunks to chain via .batch() ...")
    start = time.time()
    results = chain.batch(batch_inputs)
    elapsed = time.time() - start

    print(f"   Completed in {elapsed:.2f}s\n")

    for i, (inp, out) in enumerate(zip(batch_inputs, results)):
        print(f"── Chunk {i+1} ──────────────────────────────────────")
        print(f"INPUT  ({len(inp['text'])} chars): {inp['text'][:100].strip()!r}...")
        print(f"OUTPUT : {out.strip()}")
        print()

    print("✅ Batch processing complete.")
    return results


# ─────────────────────────────────────────────────────────────────────────────
# TASK 5 — Streaming (.stream)
# ─────────────────────────────────────────────────────────────────────────────

def task5_stream(chain, chunks):
    """
    Stream the LLM response token-by-token using .stream().
    Tokens are printed immediately as they arrive, separated by ' | '.
    This shows the incremental generation rather than waiting for the full reply.
    """
    print("\n" + "=" * 60)
    print("TASK 5 — Streaming Response  (.stream)")
    print("=" * 60)

    # Pick the most content-rich chunk for a good streaming demo
    sample_chunk = max(chunks[:10], key=lambda c: len(c.page_content))

    print(f"\n📝 Streaming summary for chunk ({len(sample_chunk.page_content)} chars):")
    print(f"   Input preview: {sample_chunk.page_content[:150].strip()!r}...\n")
    print("─" * 60)
    print("STREAMED OUTPUT (tokens separated by  |):\n")

    token_count = 0
    full_response = ""

    for token in chain.stream({"text": sample_chunk.page_content}):
        print(token, end=" | ", flush=True)
        full_response += token
        token_count += 1

    print(f"\n{'─' * 60}")
    print(f"\n📊 Total tokens streamed : {token_count}")
    print(f"   Full response length  : {len(full_response)} chars")
    print(f"\n✅ Streaming complete.")

    return full_response


# ─────────────────────────────────────────────────────────────────────────────
# BONUS — Single .invoke() demo
# ─────────────────────────────────────────────────────────────────────────────

def bonus_invoke(chain, chunks):
    """
    Quick .invoke() demo — simplest way to call the chain.
    Returns a single string result for a single input.
    """
    print("\n" + "=" * 60)
    print("BONUS — Single Invocation  (.invoke)")
    print("=" * 60)

    text = chunks[0].page_content
    print(f"\n📝 Input ({len(text)} chars): {text[:150].strip()!r}...\n")

    result = chain.invoke({"text": text})

    print(f"OUTPUT:\n{result}")
    print("\n✅ invoke() complete.")


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    print("╔══════════════════════════════════════════════════════════╗")
    print("║   Assignment 1 — Multi-Format Document Processor         ║")
    print("╚══════════════════════════════════════════════════════════╝")

    # ── Setup ────────────────────────────────────────────────────────────────
    create_sample_files()

    # ── Task 1: Load documents ───────────────────────────────────────────────
    all_docs = task1_load_documents()

    # ── Task 2: Split + compare ──────────────────────────────────────────────
    chunks = task2_text_splitting(all_docs)

    # ── Tasks 3–5 require OpenAI key ─────────────────────────────────────────
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  OPENAI_API_KEY not set.")
        print("   Tasks 3–5 require a valid API key.")
        print("   Set it with:  export OPENAI_API_KEY='sk-...'")
        return

    # ── Task 3: Build chain ──────────────────────────────────────────────────
    chain = build_chain()

    # ── Task 4: Batch ────────────────────────────────────────────────────────
    task4_batch(chain, chunks)

    # ── Task 5: Stream ───────────────────────────────────────────────────────
    task5_stream(chain, chunks)

    # ── Bonus: Invoke ────────────────────────────────────────────────────────
    bonus_invoke(chain, chunks)

    print("\n\n✅ Assignment 1 complete!")


if __name__ == "__main__":
    main()