"""
9. Retrievers — Fetch relevant documents from any source
Based on LangChain v0.3 Components Guide

Strategies:
- Similarity — default nearest-neighbour
- MMR — Max Marginal Relevance (relevance + diversity)
- Multi-Query — multiple query variants
"""
from dotenv import load_dotenv
load_dotenv()

from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

docs = [
    Document(page_content="LCEL is LangChain Expression Language. Pipe components with |.", metadata={}),
    Document(page_content="RAG retrieves relevant docs before generating.", metadata={}),
    Document(page_content="Embeddings enable semantic search.", metadata={}),
]

try:
    from langchain_community.vectorstores import Chroma

    # Create ChromaDB vector store (persists automatically)
    vectorstore = Chroma.from_documents(
        docs,
        embeddings,
        persist_directory="./chroma_retrievers",
        collection_name="retrievers_demo",
    )

    # Basic retriever
    retriever = vectorstore.as_retriever(search_kwargs={"k": 2})
    results = retriever.invoke("Explain LCEL")
    print("Basic retriever:", results[0].page_content[:50] + "...")

    # MMR retriever — balance relevance and diversity
    mmr_retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 2, "fetch_k": 3},
    )
    mmr_results = mmr_retriever.invoke("LCEL and RAG")
    print("MMR retriever:", len(mmr_results), "docs")

    # RAG chain — retriever | prompt | llm
    rag_prompt = ChatPromptTemplate.from_messages([
        ("system", "Answer based on context.\nContext:\n{context}"),
        ("human", "{question}"),
    ])

    def format_docs(docs):
        return "\n".join(d.page_content for d in docs)

    rag = (
        RunnableParallel({
            "context": retriever | RunnableLambda(format_docs),
            "question": RunnablePassthrough(),
        })
        | rag_prompt
        | llm
        | StrOutputParser()
    )
    answer = rag.invoke("What is LCEL?")
    print("RAG answer:", answer[:80] + "..." if len(answer) > 80 else answer)

except ImportError:
    print("Retrievers: pip install langchain-community chromadb")
