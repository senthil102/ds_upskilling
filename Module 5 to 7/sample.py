import os
import fitz
import chromadb
import streamlit as st
from sentence_transformers import SentenceTransformer
from openai import OpenAI


CHUNK_SIZE = 500
COLLECTION_NAME = "pdf_collection"

# OpenAI Client
client = OpenAI(api_key=os.getenv("--"))

# Embedding Model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Chroma DB
chroma_client = chromadb.PersistentClient(path="./chroma_db")

collection = chroma_client.get_or_create_collection(
    name=COLLECTION_NAME
)


def read_pdf(uploaded_file):

    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")

    text = ""

    for page in doc:
        text += page.get_text()

    doc.close()

    return text



def split_text(text, chunk_size=CHUNK_SIZE):

    chunks = []

    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i+chunk_size])

    return chunks


def create_vector_store(chunks):

    try:
        chroma_client.delete_collection(COLLECTION_NAME)
    except:
        pass

    collection = chroma_client.get_or_create_collection(
        name=COLLECTION_NAME
    )

    embeddings = embedding_model.encode(chunks)

    for i, chunk in enumerate(chunks):

        collection.add(
            ids=[str(i)],
            documents=[chunk],
            embeddings=[embeddings[i].tolist()]
        )

    return collection



def search(collection, question):

    question_embedding = embedding_model.encode(question)

    results = collection.query(

        query_embeddings=[question_embedding.tolist()],

        n_results=3

    )

    return results["documents"][0]


def ask_gpt(question, context):

    prompt = f"""
You are an AI assistant.

Answer ONLY using the context below.

If the answer is not found in the document, reply:

"I couldn't find that information in the uploaded PDF."

Context:

{context}

Question:

{question}
"""

    response = client.responses.create(
        model="gpt-4.1",
        input=prompt
    )

    return response.output_text



st.title("📄 PDF RAG Chatbot")

uploaded_file = st.file_uploader(
    "Upload PDF",
    type="pdf"
)

if uploaded_file:

    with st.spinner("Reading PDF..."):

        text = read_pdf(uploaded_file)

    st.success("PDF Loaded")

    chunks = split_text(text)

    st.write(f"Total Chunks : {len(chunks)}")

    with st.spinner("Creating Embeddings..."):

        collection = create_vector_store(chunks)

    st.success("Vector Database Ready")

    question = st.text_input(
        "Ask a Question"
    )

    if st.button("Get Answer"):

        docs = search(collection, question)

        context = "\n\n".join(docs)

        answer = ask_gpt(question, context)

        st.subheader("Answer")

        st.write(answer)

        st.subheader("Retrieved Context")

        for i, d in enumerate(docs):

            st.write(f"Chunk {i+1}")

            st.info(d)