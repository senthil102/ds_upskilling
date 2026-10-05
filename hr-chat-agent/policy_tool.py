import os
import chromadb

from dotenv import load_dotenv
from pypdf import PdfReader
from langchain_core.tools import tool
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()


PDF_FILE = os.path.join(
    os.path.dirname(__file__),
    "data",
    "hr_policies",
    "company-policy.pdf"
)


CHROMA_PATH = os.path.join(
    os.path.dirname(__file__),
    "hr_policy_db"
)


COLLECTION_NAME = "hr_policies"


embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001"
)


def load_policy_document():

    reader = PdfReader(
        PDF_FILE
    )

    full_text = ""

    for page in reader.pages:

        text = page.extract_text()

        if text:
            full_text += text + "\n"

    return full_text


def create_chunks():

    text = load_policy_document()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = splitter.split_text(
        text
    )

    return chunks


def create_vector_store():

    chunks = create_chunks()

    client = chromadb.PersistentClient(
        path=CHROMA_PATH
    )

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME
    )

    # Avoid inserting the same document repeatedly
    if collection.count() > 0:

        return collection

    documents = chunks

    ids = [
        f"policy_{index}"
        for index in range(len(chunks))
    ]

    vectors = embeddings.embed_documents(
        documents
    )

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=vectors
    )

    return collection


@tool
def search_hr_policy(question: str) -> str:
    """Search the company HR policy documents for policy-related information."""

    collection = create_vector_store()

    query_vector = embeddings.embed_query(question)

    results = collection.query(
        query_embeddings=[query_vector],
        n_results=3
    )

    documents = results.get("documents", [[]])[0]

    if not documents:
        return "No relevant HR policy information was found."

    return "\n\n".join(documents)
