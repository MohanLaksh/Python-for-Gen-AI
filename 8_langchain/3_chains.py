"""
3. Chains — LCEL (LangChain Expression Language) — Official docs

Compose with pipe: prompt | llm | parser
Sequential flow: chain1 outputs feed into chain2
"""
from dotenv import load_dotenv
load_dotenv()

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

try:
    from langchain.chat_models import init_chat_model
    llm = init_chat_model("openai:gpt-4o-mini", temperature=0.7)
except ImportError:
    from langchain_openai import ChatOpenAI
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# Chain 1: Get capital
prompt_capital = ChatPromptTemplate.from_template("What is the capital of {country}?")
chain_capital = prompt_capital | llm | StrOutputParser()

# Chain 2: Translate (uses output of chain 1)
prompt_translate = ChatPromptTemplate.from_template(
    "Translate the following text into {language}: {capital}"
)
chain_translate = prompt_translate | llm | StrOutputParser()

# Sequential: compose so capital output feeds into translate
def run_sequential(country: str, language: str):
    capital = chain_capital.invoke({"country": country})
    return chain_translate.invoke({"capital": capital, "language": language})

result = run_sequential("India", "Kannada")
print("Sequential LCEL:", result)

# Single pipe chain (simple)
chain = ChatPromptTemplate.from_template("Translate to Spanish: {text}") | llm | StrOutputParser()
print("Simple chain:", chain.invoke({"text": "Hello, world!"}))
