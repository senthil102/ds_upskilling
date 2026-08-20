import requests
from memory import AgentMemory


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.1"


def ask_llama(prompt):

    data = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(
        OLLAMA_URL,
        json=data,
        timeout=60
    )

    response.raise_for_status()

    return response.json()["response"]


def run():

    memory = AgentMemory()

    task = "Explain caching in .NET."


    # -------------------------
    # Short-term memory
    # -------------------------

    memory.add_conversation("user", task)

    print("Short-term memory:")
    print(memory.get_conversation())


    # -------------------------
    # Semantic memory
    # -------------------------

    if not memory.get_fact("language"):
        memory.add_fact("language", "C#")

    language = memory.get_fact("language")

    print("\nSemantic memory:")
    print(language)


    # -------------------------
    # Procedural memory
    # -------------------------

    if not memory.get_procedure("explain_concept"):

        memory.add_procedure(
            "explain_concept",
            [
                "Give a simple definition",
                "Give a real-world example",
                "Give a .NET example"
            ]
        )

    procedure = memory.get_procedure("explain_concept")

    print("\nProcedural memory:")
    print(procedure)


    # -------------------------
    # Build prompt
    # -------------------------

    prompt = f"""
Task:
{task}

Known fact:
Programming language = {language}

Procedure:
{procedure}

Explain the topic simply for a beginner.
"""

    # -------------------------
    # Call Llama
    # -------------------------

    result = ask_llama(prompt)

    print("\nAI Answer:")
    print(result)


    # -------------------------
    # Episodic memory
    # -------------------------

    memory.add_episode(task, result)

    print("\nEpisodic memory saved.")


if __name__ == "__main__":
    run()