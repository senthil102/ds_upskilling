import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.1"


def ask_llama(prompt, role):
    data = {
        "model": MODEL,
        "prompt": prompt,
        "system": role,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=data)
    response.raise_for_status()

    return response.json()["response"]


def researcher(task):
    prompt = f"""
Task: {task}

Give 3 important points needed to complete this task.
"""

    return ask_llama(
        prompt,
        "You are a researcher. Give simple and short information."
    )


def planner(task, research):
    prompt = f"""
Task: {task}

Research:
{research}

Create 3 simple steps to complete the task.
"""

    return ask_llama(
        prompt,
        "You are a planner. Create a simple step-by-step plan."
    )


def executor(task, plan):
    prompt = f"""
Task: {task}

Plan:
{plan}

Follow the plan and create a draft answer.
"""

    return ask_llama(
        prompt,
        "You are an executor. Complete the task using the plan."
    )


def writer(task, draft):
    prompt = f"""
Task: {task}

Draft:
{draft}

Rewrite the draft in a clear and simple way.
"""

    return ask_llama(
        prompt,
        "You are a writer. Make the answer clear and easy to understand."
    )


def critic(task, answer):
    prompt = f"""
Task: {task}

Answer:
{answer}

Check the answer.

Reply only:
APPROVED

or

REJECTED: reason
"""

    return ask_llama(
        prompt,
        "You are a reviewer. Check whether the answer satisfies the task."
    )