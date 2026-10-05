import os

import chromadb

from dotenv import load_dotenv
from pypdf import PdfReader
from docx import Document

from langchain_core.tools import tool
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from database import get_connection


load_dotenv()


BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DOCUMENTS_DIR = os.path.join(
    BASE_DIR,
    "data",
    "hr_documents"
)


CHROMA_PATH = os.path.join(
    BASE_DIR,
    "hr_policy_db"
)


COLLECTION_NAME = "hr_policies_dynamic"

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001"
)


splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)


def get_collection():

    client = chromadb.PersistentClient(
        path=CHROMA_PATH
    )

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME
    )

    return collection


def extract_pdf_text(file_path):

    reader = PdfReader(
        file_path
    )

    full_text = ""

    for page in reader.pages:

        text = page.extract_text()

        if text:

            full_text += text + "\n"

    return full_text


def extract_docx_text(file_path):

    document = Document(
        file_path
    )

    paragraphs = []

    for paragraph in document.paragraphs:

        if paragraph.text.strip():

            paragraphs.append(
                paragraph.text
            )

    return "\n".join(
        paragraphs
    )


def extract_txt_text(file_path):

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        return file.read()


def extract_text(file_path):

    extension = os.path.splitext(
        file_path
    )[1].lower()


    if extension == ".pdf":

        return extract_pdf_text(
            file_path
        )


    if extension == ".docx":

        return extract_docx_text(
            file_path
        )


    if extension == ".txt":

        return extract_txt_text(
            file_path
        )


    return ""


def get_active_documents():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            file_name,
            file_path
        FROM documents
        WHERE status = 'ACTIVE'
        ORDER BY id
        """
    )

    documents = cursor.fetchall()

    connection.close()

    return documents


def sync_documents():

    collection = get_collection()

    documents = get_active_documents()

    existing = collection.get(
        include=["metadatas"]
    )

    existing_ids = set(
        existing.get("ids", [])
    )

    current_document_ids = {
        str(document[0])
        for document in documents
    }


    if existing.get("ids"):

        ids_to_delete = []

        for index, vector_id in enumerate(
            existing["ids"]
        ):

            metadata = (
                existing
                .get("metadatas", [])[index]
            )

            if metadata:

                document_id = str(
                    metadata.get(
                        "document_id",
                        ""
                    )
                )

                if (
                    document_id
                    not in current_document_ids
                ):

                    ids_to_delete.append(
                        vector_id
                    )


        if ids_to_delete:

            collection.delete(
                ids=ids_to_delete
            )


    for document in documents:

        document_id = document[0]

        file_name = document[1]

        file_path = document[2]


        if not os.path.exists(
            file_path
        ):

            continue


        # Check whether this document
        # has already been indexed.

        already_indexed = False

        for vector_id in existing_ids:

            existing_data = collection.get(
                ids=[vector_id],
                include=["metadatas"]
            )

            metadatas = existing_data.get(
                "metadatas",
                []
            )

            if metadatas:

                metadata = metadatas[0]

                if str(
                    metadata.get(
                        "document_id"
                    )
                ) == str(document_id):

                    already_indexed = True

                    break


        if already_indexed:

            continue


        text = extract_text(
            file_path
        )


        if not text.strip():

            continue

        chunks = splitter.split_text(
            text
        )


        if not chunks:

            continue

        vectors = embeddings.embed_documents(
            chunks
        )

        ids = []

        for index in range(
            len(chunks)
        ):

            ids.append(
                f"doc_{document_id}_chunk_{index}"
            )

        metadatas = []

        for _ in chunks:

            metadatas.append(
                {
                    "document_id": str(
                        document_id
                    ),
                    "file_name": file_name
                }
            )


        collection.add(
            ids=ids,
            documents=chunks,
            embeddings=vectors,
            metadatas=metadatas
        )


    return collection

@tool
def search_hr_policy(
    question: str
) -> str:
    """Search the company HR policy documents for policy-related information."""

    collection = sync_documents()


    if collection.count() == 0:

        return (
            "No HR policy documents are "
            "currently available."
        )

    query_vector = embeddings.embed_query(
        question
    )

    results = collection.query(
        query_embeddings=[query_vector],
        n_results=3
    )


    documents = results.get(
        "documents",
        [[]]
    )[0]


    if not documents:

        return (
            "No relevant HR policy "
            "information was found."
        )


    return "\n\n".join(
        documents
    )