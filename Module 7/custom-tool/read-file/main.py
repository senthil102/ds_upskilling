import os
import json
import ollama
from pypdf import PdfReader

MODEL = "llama3.1"
ALLOWED_DIR = os.path.abspath(r"C:\GENAI\GenAI\Module 7\custom-tool\read-file\documents")
MAX_FILE_SIZE = 5_000_000


def read_file(filename: str):
    target_path = os.path.abspath(os.path.join(ALLOWED_DIR, filename))

    if not target_path.startswith(ALLOWED_DIR):
        return {"error": "Access denied: file is outside the allowed directory."}

    if not os.path.isfile(target_path):
        available = os.listdir(ALLOWED_DIR)
        return {"error": f"File not found: {filename}", "available_files": available}

    if os.path.getsize(target_path) > MAX_FILE_SIZE:
        return {"error": f"File too large to read (max {MAX_FILE_SIZE} bytes)."}

    ext = os.path.splitext(target_path)[1].lower()

    try:
        if ext == ".pdf":
            reader = PdfReader(target_path)
            content = "\n".join(page.extract_text() or "" for page in reader.pages)
        else:
            with open(target_path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
    except Exception as e:
        return {"error": f"Could not read file: {e}"}

    return {"filename": filename, "content": content[:20000]}


def list_files():
    return {"files": os.listdir(ALLOWED_DIR)}


tools = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": (
                "Read the text contents of a file by name from the documents folder. "
                "Only works for files inside the allowed documents directory."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {"type": "string", "description": "Name of the file to read"},
                },
                "required": ["filename"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "List all files currently available to read in the documents folder.",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
]

available_functions = {"read_file": read_file, "list_files": list_files}

messages = [{
    "role": "user",
    "content": "List the available files, then read whichever one you find and summarize it."
}]

response = ollama.chat(model=MODEL, messages=messages, tools=tools)
msg = response["message"]
print("DEBUG tool_calls:", msg.get("tool_calls"))
messages.append(msg)

if msg.get("tool_calls"):
    for call in msg["tool_calls"]:
        func_name = call["function"]["name"]
        args = call["function"]["arguments"]

        if func_name not in available_functions:
            result = {"error": f"Unknown tool '{func_name}'"}
        else:
            result = available_functions[func_name](**args)

        messages.append({"role": "tool", "content": json.dumps(result)})

    final = ollama.chat(model=MODEL, messages=messages)
    print(final["message"]["content"])
else:
    print(msg["content"])