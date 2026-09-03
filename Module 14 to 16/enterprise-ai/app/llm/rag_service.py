from app.llm.ollama import ask_llama

from app.rag.retriever import (
    retrieve_context
)


def ask_rag(question: str):

    documents, metadatas = retrieve_context(
        question,
        top_k=5
    )

    if not documents:

        return {
            "answer": "No relevant information was found.",
            "sources": []
        }

    context = "\n\n".join(
        documents
    )

    prompt = f"""
You are an enterprise document assistant.

Answer the question using ONLY the
provided context.

Context:
{context}

Question:
{question}

Rules:
- Do not make up information.
- Use only the provided context.
- If the answer is not available,
  say "I don't know based on the provided document."

Answer:
"""

    answer = ask_llama(prompt)

    return {
        "answer": answer,
        "sources": metadatas
    }