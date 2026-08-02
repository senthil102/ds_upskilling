import chromadb


client = chromadb.PersistentClient(path="./chroma_db")


collection = client.get_or_create_collection(
    name="products"
)


collection.add(
    ids=[
        "1",
        "2",
        "3",
        "4"
    ],
    documents=[
        "Apple MacBook Pro Laptop",
        "Dell Inspiron Laptop",
        "Samsung Galaxy Mobile",
        "Apple iPhone 16 Pro"
    ],
    metadatas=[
        {"brand": "Apple", "category": "Laptop"},
        {"brand": "Dell", "category": "Laptop"},
        {"brand": "Samsung", "category": "Mobile"},
        {"brand": "Apple", "category": "Mobile"}
    ]
)

print("Documents Added Successfully")
