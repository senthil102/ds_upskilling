from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

documents = [
    "Python is a programming language",
    "FastAPI is used for APIs",
    "Azure provides cloud services",
    "OpenAI develops GPT models"
]

embeddings = model.encode(documents)

print(embeddings.shape)