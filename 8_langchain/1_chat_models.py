"""
1. LLMs & Chat Models — Official docs: python.langchain.com/docs/concepts/chat_models

Initialize: init_chat_model() (provider-agnostic) or ChatOpenAI/ChatAnthropic
Invoke: single message, list of messages (dict or Message objects)
Stream: model.stream() yields chunks
Batch: model.batch() for parallel requests
"""
import os
from dotenv import load_dotenv
load_dotenv()

try:
    from langchain.chat_models import init_chat_model
    model = init_chat_model("openai:gpt-4o-mini", temperature=0.7)
except ImportError:
    from langchain_openai import ChatOpenAI
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# Single message
response = model.invoke("Why do parrots have colorful feathers?")
print("Invoke:", response.content if hasattr(response, "content") else response.text)

# List of messages (dict format)
conversation = [
    {"role": "system", "content": "You are a helpful assistant that translates English to French."},
    {"role": "user", "content": "Translate: I love programming."},
]
response = model.invoke(conversation)
print("Dict messages:", response.content if hasattr(response, "content") else response.text)

# Message objects
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

messages = [
    SystemMessage(content="You are a concise Python tutor."),
    HumanMessage(content="What is a list comprehension? One sentence."),
]
response = model.invoke(messages)
print("Message objects:", response.content)

# Streaming
print("Streaming:")
for chunk in model.stream("What color is the sky?"):
    text = chunk.content if hasattr(chunk, "content") else getattr(chunk, "text", "")
    if text:
        print(text, end="", flush=True)
print()

# Batch
responses = model.batch([
    "Why do parrots have colorful feathers?",
    "How do airplanes fly?",
])
print("Batch:", [r.content[:50] + "..." for r in responses])
