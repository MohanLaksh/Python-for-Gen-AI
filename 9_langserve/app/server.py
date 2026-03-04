from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from langserve import add_routes
import os
from dotenv import load_dotenv

load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

app = FastAPI()

llm = ChatOpenAI(
    model="gpt-5-nano",
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=.8,
)


@app.get("/")
async def redirect_root_to_docs() -> RedirectResponse:
    return RedirectResponse("/docs")

prompt = PromptTemplate.from_template(" Genarate a joke on {topic}")

chain = prompt | llm


add_routes(app, chain, path="/joke")


# Edit this to add the chain you want to add
# add_routes(app, NotImplemented)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8100)
