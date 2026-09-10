import chromadb

class SemanticCache:
    def __init__(self):
        self.client = chromadb.PersistentClient(path="./cache_db")
        self.collection = self.client.get_or_create_collection(name="sales_intelligence_cache")

    def get_cached_response(self, question: str, max_distance: float = 0.5):
        results = self.collection.query(
            query_texts=[question],
            n_results=1,
            include=["documents", "metadatas", "distances"],
        )

        if not results["documents"][0]:
            return None

        distance = results["distances"][0][0]
        print(f"Cache distance: {distance}")

        if distance > max_distance:
            return None

        return results["metadatas"][0][0]["response"]

    def save_response(self, question: str, response: str):
        count = self.collection.count()

        self.collection.add(
            documents=[question],
            metadatas=[{"response": response}],
            ids=[f"question_{count + 1}"],
        )