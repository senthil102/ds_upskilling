from fastapi import FastAPI

from app.api.chat import router as chat_router
from app.api.documents import (
    router as document_router
)


app = FastAPI(
    title="Enterprise AI Assistant",
    version="1.0.0"
)


app.include_router(
    chat_router
)

app.include_router(
    document_router
)


@app.get("/health")
async def health():

    return {
        "status": "healthy"
    }