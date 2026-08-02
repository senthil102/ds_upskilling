from openai import OpenAI

client = OpenAI()

response = client.embeddings.create(
    model="text-embedding-3-small",
    input="Artificial Intelligence is transforming software."
)

embedding = response.data[0].embedding

print(len(embedding))