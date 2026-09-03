from app.rag.embeddings import (
    create_embedding
)

from app.rag.vector_store import (
    search_documents
)


def retrieve_context(
    question: str,
    top_k: int = 5
):

    query_embedding = create_embedding(
        question
    )

    result = search_documents(
        query_embedding,
        top_k
    )

    documents = result.get(
        "documents",
        [[]]
    )[0]

    metadatas = result.get(
        "metadatas",
        [[]]
    )[0]

    return documents, metadatas