import requests
import time

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.1"

MAX_RETRIES = 3
TIMEOUT = 20


# Call Llama
def call_llama(prompt):
    data = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(
        OLLAMA_URL,
        json=data,
        timeout=TIMEOUT
    )

    response.raise_for_status()

    return response.json()["response"]


# Retry Pattern
def retry_call(prompt):
    for attempt in range(1, MAX_RETRIES + 1):

        try:
            print(f"Attempt {attempt}")

            result = call_llama(prompt)

            if result.strip():
                return result

        except Exception as error:
            print(f"Error: {error}")

        if attempt < MAX_RETRIES:
            print("Retrying...")
            time.sleep(2)

    return None


# Guardrail Pattern
def validate_output(result):
    if result is None:
        return False

    if len(result.strip()) < 10:
        print("Guardrail: Response is too short")
        return False

    return True


# Fallback Pattern
def fallback_response():
    return "Sorry, the AI service is currently unavailable."


# Simple logger
def log(message):
    print(f"[LOG] {message}")