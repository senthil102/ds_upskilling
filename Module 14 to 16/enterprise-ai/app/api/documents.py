import os
import uuid

from fastapi import (
    APIRouter,
    UploadFile,
    File
)

from app.rag.loader import load_pdf
from app.rag.chunker import chunk_text
from app.rag.embeddings import create_embeddings
from app.rag.vector_store import add_documents

router = APIRouter(
    prefix="/api/v1/documents",
    tags=["Documents"]
)


UPLOAD_DIR = "uploads"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)


@router.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...)
):

    # Validate file
    if not file.filename:
        return {
            "error": "File name is required"
        }

    if not file.filename.lower().endswith(".pdf"):
        return {
            "error": "Only PDF files are supported"
        }

    # Generate document ID
    document_id = str(
        uuid.uuid4()
    )

    filename = (
        f"{document_id}.pdf"
    )

    path = os.path.join(
        UPLOAD_DIR,
        filename
    )

    # Save PDF
    contents = await file.read()

    with open(path, "wb") as f:
        f.write(contents)

    # Extract text
    text = load_pdf(path)

    if not text.strip():

        return {
            "error": "Could not extract text from PDF"
        }

    # Chunk text
    chunks = chunk_text(
        text,
        chunk_size=1000,
        overlap=200
    )

    # Create embeddings
    embeddings = create_embeddings(
        chunks
    )

    # Store in ChromaDB
    add_documents(
        chunks,
        embeddings,
        file.filename
    )

    return {
        "message": "PDF processed successfully",
        "filename": file.filename,
        "chunks": len(chunks),
        "document_id": document_id
    }