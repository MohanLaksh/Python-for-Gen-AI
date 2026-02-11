"""
4. LCEL & Runnables — Composability layer — pipe components with | operator
Based on LangChain v0.3 Components Guide

Core Runnables:
- RunnablePassthrough: pass input unchanged
- RunnableParallel: run branches in parallel
- RunnableLambda: wrap any Python callable
"""
from langchain_core.runnables import RunnablePassthrough, RunnableParallel, RunnableLambda
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# Basic pipe chain
prompt = ChatPromptTemplate.from_template("Translate to Spanish: {text}")
chain = prompt | llm | StrOutputParser()
result = chain.invoke({"text": "Hello, world!"})
print("Basic pipe:", result)

# RunnableParallel + RunnablePassthrough — RAG-style (simulated retriever)
from langchain_core.documents import Document

def mock_retriever(query: str):
    return [
        Document(page_content="LCEL is LangChain Expression Language. Pipe with |.", metadata={}),
    ]

retriever = RunnableLambda(mock_retriever)

def format_docs(docs):
    return "\n".join(d.page_content for d in docs) if docs else ""

# RunnableParallel runs retriever with input, passes input as "question"
retrieval = RunnableParallel({
    "context": retriever | RunnableLambda(format_docs),
    "question": RunnablePassthrough(),
})
rag_prompt = ChatPromptTemplate.from_messages([
    ("system", "Answer based on context only.\nContext:\n{context}"),
    ("human", "{question}"),
])
rag_chain = retrieval | rag_prompt | llm | StrOutputParser()
# When invoke is a string, RunnablePassthrough passes it; retriever receives it
answer = rag_chain.invoke("What is LCEL?")
print("RAG-style (RunnableParallel):", answer)

# RunnableLambda — custom processing
add_prefix = RunnableLambda(lambda x: {"text": f"Prefix: {x.get('text', x)}"})
chain_with_lambda = add_prefix | prompt | llm | StrOutputParser()
result2 = chain_with_lambda.invoke({"text": "Good morning"})
print("With RunnableLambda:", result2)

# Streaming
print("Streaming:")
for token in chain.stream({"text": "Good morning"}):
    print(token, end="", flush=True)
print()
