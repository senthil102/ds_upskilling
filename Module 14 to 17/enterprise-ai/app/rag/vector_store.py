import chromadb


client = chromadb.PersistentClient(
    path="./data/chroma"
)


collection = client.get_or_create_collection(
    name="documents"
)


def add_documents(
    chunks: list[str],
    embeddings: list[list[float]],
    document_id: str
):

    ids = [
        f"{document_id}_{index}"
        for index in range(len(chunks))
    ]

    metadatas = [
        {
            "document": document_id,
            "chunk": index
        }
        for index in range(len(chunks))
    ]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas
    )


def search_documents(
    query_embedding: list[float],
    top_k: int = 5
):

    return collection.query(
        query_embeddings=[
            query_embedding
        ],
        n_results=top_k
    )