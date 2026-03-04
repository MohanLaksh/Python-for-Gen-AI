from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from langserve import add_routes
from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from langserve.schema import CustomUserType
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv
import os
import base64

load_dotenv()

app = FastAPI(
    title="Code Debugger Assistant",
    description="AI powered code debugger assistant using LangChain + LCEL and LangServe",
    version="1.0.0",
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

@app.get("/")
async def redirect_root_to_docs() -> RedirectResponse:
    return RedirectResponse("/docs")

class DebugRequest(CustomUserType):
    """Input schema for code debugger assistant"""
    code: str = Field(default="", description="Buggy code")
    error_messages: str = Field(default="", description="Error message")
    files: str = Field(default="", description="File name")
    language: str = Field(default="", description="Language")
    generate_test: bool = Field(default=True, description="Whether to generate a unit test")

class DebugResponse(CustomUserType):
    """Output schema for code debugger assistant"""
    root_cause: str = Field(..., description="Root cause of the bug")
    corrected_code: str = Field(..., description="Corrected code")
    explanation: str = Field(..., description="Explanation of the fix")
    test_code: str = Field(..., description="Unit test for the corrected code (empty if not requested)")


def preprocess(request: DebugRequest) -> dict:
    """Preprocess the input request"""
    
    code_content = request.code
    if request.files and os.path.exists(request.files):
        with open(request.files, "r") as f:
            raw_b64 = f.split(",", 1)[-1] if "," in f else f
            code_content = base64.b64decode(raw_b64).decode("utf-8", errors="replace")

    return {
        "code": code_content,
        "error_messages": request.error_messages,
        "language": request.language,
        "generate_test": request.generate_test
    }


SYSTEM_PROMPT = """
You are an expert code debugging assistant. Your job is to analyze the buggy code and optional error message provided by the user and provide a corrected version of the code along with an explanation of the fix.
"""

DEBUG_PROMPT = ChatPromptTemplate.from_messages([
    SystemMessage(content=SYSTEM_PROMPT),
    ("human", """
    ## Buggy Code
    {code}
    
    ## Error Message
    {error_messages}
    
    ## Language
    {language}
    
    ## Generate Unit Test
    {generate_test}

    # Respond in JSON format as below:
   {{
        "root_cause": "The root cause in 2-4 sentences",
        "corrected_code": "The full corrected code block",
        "explanation": "Explanation of the fix justifying why it works in 2-4 sentences",
        "test_code": "The unit test code block (if Generate Unit Test is True, else leave empty '')"
    }}
    """)
])

llm = ChatOpenAI(
    model="gpt-5-nano",
    temperature=0,
)


debug_chain = (
    RunnableLambda(preprocess)
    |DEBUG_PROMPT
    |llm
    |JsonOutputParser()
).with_types(input_type=DebugRequest, output_type=DebugResponse)

add_routes(
    app,
    debug_chain,
    path="/debug"
)



if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
