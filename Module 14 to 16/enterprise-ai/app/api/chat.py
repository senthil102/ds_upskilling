from fastapi import APIRouter

from app.models.schemas import (
    ChatRequest,
    ChatResponse
)

from app.llm.ollama import MODEL
from app.llm.rag_service import ask_rag


router = APIRouter(
    prefix="/api/v1",
    tags=["Chat"]
)


@router.post(
    "/chat",
    response_model=ChatResponse
)
async def chat(request: ChatRequest):

    result = ask_rag(
        request.message
    )

    return ChatResponse(
        answer=result["answer"],
        model=MODEL,
        conversation_id=request.conversation_id
    )