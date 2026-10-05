import chromadb


class SemanticCache:

    def __init__(self):

        self.client = chromadb.PersistentClient(
            path="./hr_cache_db"
        )

        self.collection = self.client.get_or_create_collection(
            name="hr_chat_cache"
        )

    def get_cached_response(
        self,
        question: str,
        max_distance: float = 0.5
    ):

        results = self.collection.query(
            query_texts=[question],
            n_results=1,
            include=[
                "documents",
                "metadatas",
                "distances"
            ]
        )

        if not results["documents"][0]:
            return None

        distance = results["distances"][0][0]

        if distance > max_distance:
            return None

        return results["metadatas"][0][0]["response"]

    def save_response(
        self,
        question: str,
        response: str
    ):

        count = self.collection.count()

        self.collection.add(
            documents=[question],
            metadatas=[
                {
                    "response": response
                }
            ],
            ids=[
                f"hr_question_{count + 1}"
            ]
        )