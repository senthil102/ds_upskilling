from fastapi import APIRouter

from app.models.schemas import (
    ChatRequest,
    ChatResponse
)

from app.llm.ollama import (
    ask_llama,
    MODEL
)


router = APIRouter(
    prefix="/api/v1",
    tags=["Chat"]
)


@router.post(
    "/chat",
    response_model=ChatResponse
)
async def chat(request: ChatRequest):

    answer = ask_llama(
        request.message
    )

    return ChatResponse(
        answer=answer,
        model=MODEL,
        conversation_id=request.conversation_id
    )