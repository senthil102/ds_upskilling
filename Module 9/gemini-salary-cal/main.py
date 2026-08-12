import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langchain.tools import tool
from dotenv import load_dotenv

load_dotenv()

ALLOWED_DIR = os.path.abspath(r"C:\GENAI\GenAI\Module 9\gemini-salary-cal\doc")


@tool
def get_salaries(filename: str) -> str:
    """Return names and salaries from a JSON salary file."""
    import json
    path = os.path.join(ALLOWED_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    salaries = [e["salary"] for e in data["employees"]]
    names = [e["name"] for e in data["employees"]]
    return str({"names": names, "salaries": salaries, "count": len(salaries)})


@tool
def calculator(expression: str) -> str:
    """Evaluate a simple arithmetic expression (numbers and + - * / only)."""
    import re
    if not re.fullmatch(r"[0-9+\-*/(). ]+", expression):
        return "Invalid expression"
    return str(eval(expression))


llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash", temperature=0)
tools = [get_salaries, calculator]

agent = create_agent(model=llm, tools=tools)

print("=== Agent trace ===")
for step in agent.stream(
    {"messages": [{"role": "user", "content": "What is the average salary in salary.json?"}]},
    stream_mode="values"
):
    last_msg = step["messages"][-1]

print("\n=== Final Answer ===")
if isinstance(last_msg.content, list):
    text = " ".join(block["text"] for block in last_msg.content if block.get("type") == "text")
else:
    text = last_msg.content
print(text)