import os
import json
import re
import ollama

MODEL = "llama3.1"
ALLOWED_DIR = os.path.abspath(r"C:\GENAI\GenAI\Module 9\react_agent_prompt\doc")


# TOOLS
def read_file(filename: str):
    """Read raw text contents of any file in the documents folder."""
    path = os.path.join(ALLOWED_DIR, filename)
    if not os.path.isfile(path):
        return {"error": f"File not found: {filename}"}
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return {"content": f.read()}


def get_salaries(filename: str):
    """Read a JSON salary file and return just the list of salary numbers (parsed by code, not the model)."""
    path = os.path.join(ALLOWED_DIR, filename)
    if not os.path.isfile(path):
        return {"error": f"File not found: {filename}"}
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        salaries = [emp["salary"] for emp in data.get("employees", [])]
        names = [emp["name"] for emp in data.get("employees", [])]
        return {"names": names, "salaries": salaries, "count": len(salaries)}
    except Exception as e:
        return {"error": f"Could not parse JSON: {e}"}


def calculator(expression: str):
    """Safely evaluate a math expression (digits, + - * / ( ) . only)."""
    try:
        if not re.fullmatch(r"[0-9+\-*/(). ]+", expression):
            return {"error": "Invalid characters in expression"}
        result = eval(expression)
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}


available_functions = {
    "read_file": read_file,
    "get_salaries": get_salaries,
    "calculator": calculator,
}


# REACT SYSTEM PROMPT
REACT_PROMPT = """Answer the question using this exact format, one step at a time:

Thought: <your reasoning about what to do next>
Action: <tool name, one of: read_file, get_salaries, calculator>
Action Input: <JSON arguments for the tool>

Wait for an Observation after each Action before continuing.
When you have enough information, respond with:

Thought: <final reasoning>
Final Answer: <your answer to the user>

Available tools:
- read_file: takes {"filename": "..."}, returns raw file text
- get_salaries: takes {"filename": "..."}, returns {"names": [...], "salaries": [...], "count": N}
- calculator: takes {"expression": "..."}, evaluates ONE complete arithmetic expression using only numbers, +, -, *, /, (, ). 
  Never use function names like sum(), avg(), or variable names — always write out the full expression with actual numbers, e.g. "(55000 + 62000 + 48000 + 71000) / 4".

IMPORTANT: 
- Compute the full answer in a SINGLE calculator call whenever possible.
- As soon as a calculator Observation gives you the number the question asked for, STOP and give your Final Answer immediately. Do not call calculator again on a number you already have.

Begin.
"""

messages = [
    {"role": "system", "content": REACT_PROMPT},
    {"role": "user", "content": "What is the average salary in salary.json?"},
]


MAX_STEPS = 6

for step in range(MAX_STEPS):
    print(f"\n--- Step {step + 1} ---")

    response = ollama.chat(model=MODEL, messages=messages)
    text = response["message"]["content"]
    print(text)

    messages.append({"role": "assistant", "content": text})

    # Stop condition: model gave its final answer
    if "Final Answer:" in text:
        break

    # Parse Action + Action Input from the model's text
    action_match = re.search(r"Action:\s*(\w+)", text)
    input_match = re.search(r"Action Input:\s*(\{.*\})", text, re.DOTALL)

    if not action_match:
        print("No action found — stopping.")
        break

    tool_name = action_match.group(1).strip()
    try:
        tool_args = json.loads(input_match.group(1)) if input_match else {}
    except json.JSONDecodeError:
        tool_args = {}

    # Act
    result = available_functions.get(
        tool_name, lambda **_: {"error": f"unknown tool '{tool_name}'"}
    )(**tool_args)

    # Observe: feed result back into the conversation
    observation = f"Observation: {json.dumps(result)}"
    print(observation)
    messages.append({"role": "user", "content": observation})

else:
    print("\nStopped: hit max steps without a Final Answer.")