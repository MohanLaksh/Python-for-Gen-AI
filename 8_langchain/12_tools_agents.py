"""
11. Tools & Agents — LLM-driven decision-making & tool use
Based on LangChain v0.3 Components Guide

Key concepts:
- @tool decorator — define Python functions as tools
- create_react_agent — prebuilt agent (LangGraph)
"""
from dotenv import load_dotenv
load_dotenv()

from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


@tool
def get_weather(city: str) -> str:
    """Return the current weather for a given city."""
    return f"It's sunny and 22°C in {city}."


@tool
def calculate(expression: str) -> str:
    """Evaluate a simple math expression, e.g. '2 + 3', '10 * 5', or '2 ** 10'."""
    import ast
    import operator
    ops = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
           ast.Div: operator.truediv, ast.FloorDiv: operator.floordiv, ast.Pow: operator.pow}
    tree = ast.parse(expression, mode="eval")
    def eval_node(node):
        if isinstance(node, ast.Constant):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in ops:
            return ops[type(node.op)](eval_node(node.left), eval_node(node.right))
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            return -eval_node(node.operand)
        raise ValueError("Only simple math allowed")
    return str(eval_node(tree.body))


tools = [get_weather, calculate]

# Use the new create_agent API (LangChain v0.3+)
try:
    from langchain.agents import create_agent
    agent = create_agent(llm, tools)
    # Invoke with a question that may require tools
    result = agent.invoke({
        "messages": [HumanMessage(content="What is 2**10 and the weather in London?")],
    })
    # Last message is the agent's reply
    last_msg = result["messages"][-1]
    print("Agent response:", last_msg.content if hasattr(last_msg, "content") else last_msg)
except ImportError:
    # Fallback for older versions
    from langgraph.prebuilt import create_react_agent
    agent = create_react_agent(llm, tools)
    result = agent.invoke({
        "messages": [HumanMessage(content="What is 2**10 and the weather in London?")],
    })
    last_msg = result["messages"][-1]
    print("Agent response:", last_msg.content if hasattr(last_msg, "content") else last_msg)
