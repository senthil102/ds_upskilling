import chromadb

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_collection("products")

results = collection.query(
    query_texts=["Apple Mobile"],
    n_results=2
)

print(results["documents"][0])