"""
12. Callbacks — Hooks for logging, tracing, monitoring
Based on LangChain v0.3 Components Guide

Built-in:
- StreamingStdOutCallbackHandler — print tokens to stdout
- LangSmithTracer — automatic tracing (LANGCHAIN_TRACING_V2=true)
- Custom via BaseCallbackHandler
"""
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

# Streaming callback — tokens print as they arrive
try:
    from langchain_core.callbacks import StreamingStdOutCallbackHandler

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        streaming=True,
        callbacks=[StreamingStdOutCallbackHandler()],
    )
    print("Streaming with callback:")
    llm.invoke([HumanMessage(content="Say 'Hello' in exactly one word.")])
    print()
except ImportError:
    try:
        from langchain.callbacks import StreamingStdOutCallbackHandler
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            streaming=True,
            callbacks=[StreamingStdOutCallbackHandler()],
        )
        print("Streaming with callback:")
        llm.invoke([HumanMessage(content="Say 'Hello' in exactly one word.")])
        print()
    except ImportError:
        print("StreamingStdOutCallbackHandler: check langchain/langchain_core")

# Custom callback — token counter
from langchain_core.callbacks import BaseCallbackHandler


class TokenCounter(BaseCallbackHandler):
    def __init__(self):
        self.count = 0

    def on_llm_new_token(self, token: str, **kwargs):
        self.count += 1


counter = TokenCounter()
llm2 = ChatOpenAI(model="gpt-4o-mini", temperature=0)
llm2.invoke([HumanMessage(content="Hi")], config={"callbacks": [counter]})
print("Tokens counted:", counter.count)
