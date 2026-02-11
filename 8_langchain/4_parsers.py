"""
4. Output Parsers — Official docs: reference.langchain.com/python/langchain_core/output_parsers

StrOutputParser: plain string
JsonOutputParser: JSON (handles markdown code fences)
PydanticOutputParser: validate into Pydantic model
CommaSeparatedListOutputParser: CSV to list
"""
from dotenv import load_dotenv
load_dotenv()

from langchain_core.output_parsers import (
    StrOutputParser,
    JsonOutputParser,
    CommaSeparatedListOutputParser,
)
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

try:
    from langchain.chat_models import init_chat_model
    llm = init_chat_model("openai:gpt-4o-mini", temperature=0.7)
except ImportError:
    from langchain_openai import ChatOpenAI
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# StrOutputParser
prompt = ChatPromptTemplate.from_template("Tell me a joke about {topic}.")
chain = prompt | llm | StrOutputParser()
print("StrOutputParser:", chain.invoke({"topic": "Python"}))

# JsonOutputParser
json_prompt = ChatPromptTemplate.from_messages([
    ("system", "Respond with valid JSON only. No markdown."),
    ("human", "List 3 benefits of {topic} as JSON array of strings."),
])
json_chain = json_prompt | llm | JsonOutputParser()
print("JsonOutputParser:", json_chain.invoke({"topic": "LangChain"}))

# CommaSeparatedListOutputParser
csv_prompt = ChatPromptTemplate.from_template(
    "List 3 colors. Return only comma-separated values, no numbers or bullets."
)
csv_chain = csv_prompt | llm | CommaSeparatedListOutputParser()
print("CommaSeparatedListOutputParser:", csv_chain.invoke({}))

# PydanticOutputParser
try:
    from langchain_core.output_parsers import PydanticOutputParser
except ImportError:
    from langchain_core.output_parsers.pydantic import PydanticOutputParser


class Joke(BaseModel):
    setup: str = Field(description="The setup of the joke")
    punchline: str = Field(description="The punchline")


parser = PydanticOutputParser(pydantic_object=Joke)
pydantic_prompt = ChatPromptTemplate.from_messages([
    ("system", "{format_instructions}"),
    ("human", "Tell me a joke about {topic}."),
])
pydantic_chain = pydantic_prompt | llm | parser
joke = pydantic_chain.invoke({
    "topic": "databases",
    "format_instructions": parser.get_format_instructions(),
})
print("PydanticOutputParser:", joke.setup, "—", joke.punchline)
