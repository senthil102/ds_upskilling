import os
import ollama
from dotenv import load_dotenv


load_dotenv()


MODEL = os.getenv(
    "OLLAMA_MODEL",
    "llama3.1"
)


def ask_llama(prompt: str) -> str:

    response = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]