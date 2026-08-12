import os
import json
import ollama

MODEL = "llama3.1"
ALLOWED_DIR = os.path.abspath(r"C:\GENAI\GenAI\Module 9\scratchpad-readdata\doc") 
def list_files():
    """Real Python code — actually looks at the folder on disk."""
    return {"files": os.listdir(ALLOWED_DIR)}

def read_file(filename: str):
    """Real Python code — actually opens and reads the file."""
    path = os.path.join(ALLOWED_DIR, filename)
    if not os.path.isfile(path):
        return {"error": f"File not found: {filename}"}
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()
    return {"filename": filename, "content": content[:5000]}


tools = [
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "List all files available in the documents folder.",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read the contents of a specific file by name.",
            "parameters": {
                "type": "object",
                "properties": {"filename": {"type": "string"}},
                "required": ["filename"],
            },
        },
    },
]

# maps tool name -> the actual function to run
available_functions = {"list_files": list_files, "read_file": read_file}


#SYSTEM_PROMPT

SYSTEM_PROMPT = """You are a file-reading assistant.
You do NOT know file contents from training — you must use tools.
If unsure of the filename, call list_files first, then call read_file with the exact filename.

IMPORTANT: Never write tool calls as text in your answer. 
Only use the actual tool-calling mechanism provided to you.
Do not invent tools that were not given to you — only use list_files and read_file.
"""

messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": "Read 'list-of-banking-outlets.pdf' using the read_file tool and summarize it."},
]



MAX_STEPS = 5

for step in range(MAX_STEPS):
    print(f"\n--- Step {step + 1} ---")

    # PERCEIVE + THINK: model looks at scratchpad, decides next move
    response = ollama.chat(model=MODEL, messages=messages, tools=tools)
    msg = response["message"]
    messages.append(msg)  # add model's decision to scratchpad

    # STOP CONDITION: no more tools requested = model thinks it's done
    if not msg.get("tool_calls"):
        print("Agent finished. Final answer:\n")
        print(msg["content"])
        break

    # ACT: run whichever tool(s) the model asked for
    for call in msg["tool_calls"]:
        name = call["function"]["name"]
        args = call["function"]["arguments"]
        print(f"Agent is calling tool: {name}({args})")

        result = available_functions.get(name, lambda **_: {"error": "unknown tool"})(**args)

        # OBSERVE: put the result back into the scratchpad
        messages.append({"role": "tool", "content": json.dumps(result)})

else:
    print("Stopped: hit max steps without a final answer.")