import ollama

MODEL = "llama3.1"

def ask_llm(message: str) -> str:

    response = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": message
            }
        ]
    )

    return response["message"]["content"]

