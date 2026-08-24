import time
import ollama

from dotenv import load_dotenv
from fastapi import FastAPI

from langfuse import get_client

#https://cloud.langfuse.com/project/cmt6zk7ho01ecad0d9fw0vubq/traces?utm_source=chatgpt.com
# Load .env
load_dotenv()

app = FastAPI()

MODEL = "llama3.1"

# Langfuse Cloud client
langfuse = get_client()


@app.get("/")
def home():
    return {
        "message": "Local Ollama + Langfuse is running"
    }


@app.get("/chat")
def chat(question: str):

    start_time = time.time()
    # Create Langfuse trace
    with langfuse.start_as_current_observation(
        as_type="span",
        name="ollama-chat"
    ) as trace:

        trace.update(
            input=question
        )

        # LLM generation
        with langfuse.start_as_current_observation(
            as_type="generation",
            name="llama3.1",
            model=MODEL
        ) as generation:

            response = ollama.chat(
                model=MODEL,
                messages=[
                    {
                        "role": "user",
                        "content": question
                    }
                ]
            )

            answer = response["message"]["content"]

            duration = round(
                time.time() - start_time,
                2
            )

            generation.update(
                input=question,
                output=answer
            )
        # Update trace
        trace.update(
            output=answer,
            metadata={
                "model": MODEL,
                "duration_seconds": duration,
                "provider": "ollama",
                "environment": "local"
            }
        )

    # Important for short-lived requests
    langfuse.flush()

    return {
        "question": question,
        "answer": answer,
        "model": MODEL,
        "duration": duration
    }