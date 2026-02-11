"""
10. Memory & History — Session-based conversation persistence
Based on LangChain v0.3 Components Guide

Key concepts:
- RunnableWithMessageHistory — wraps any LCEL chain
- ChatMessageHistory — in-memory (development)
- RedisChatMessageHistory — persistent across restarts
"""
from dotenv import load_dotenv
load_dotenv()

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Store: session_id -> ChatMessageHistory
store = {}

try:
    from langchain_community.chat_message_histories import ChatMessageHistory
    from langchain_core.runnables.history import RunnableWithMessageHistory

    def get_history(session_id: str):
        if session_id not in store:
            store[session_id] = ChatMessageHistory()
        return store[session_id]

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant."),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ])

    chain = prompt | llm | StrOutputParser()

    chain_with_memory = RunnableWithMessageHistory(
        chain,
        get_history,
        input_messages_key="input",
        history_messages_key="history",
    )

    config = {"configurable": {"session_id": "user-42"}}

    r1 = chain_with_memory.invoke({"input": "My name is Alice."}, config)
    print("R1:", r1)

    r2 = chain_with_memory.invoke({"input": "What is my name?"}, config)
    print("R2:", r2)

except ImportError:
    print("Memory: pip install langchain-community")
