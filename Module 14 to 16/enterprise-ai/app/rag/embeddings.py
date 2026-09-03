from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"


embedding_model = SentenceTransformer(
    MODEL_NAME
)


def create_embeddings(
    texts: list[str]
):

    embeddings = embedding_model.encode(
        texts
    )

    return embeddings.tolist()


def create_embedding(
    text: str
):

    embedding = embedding_model.encode(
        text
    )

    return embedding.tolist()