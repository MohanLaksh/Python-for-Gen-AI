from langchain_core.runnables import RunnablePassthrough, RunnableParallel, RunnableLambda
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

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
print(rag_chain.invoke("What is LCEL?"))