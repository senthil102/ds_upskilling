
from fastapi import APIRouter, BackgroundTasks, UploadFile, File
from fastapi.responses import StreamingResponse

from app.models.schemas import ChatRequest, ChatResponse
from app.services.llm_service import ask_llm

import asyncio
import ollama
import os


router = APIRouter()

MODEL = "llama3.1"



@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):

    answer = ask_llm(request.message)

    return ChatResponse(
        answer=answer,
        model=MODEL
    )



@router.post("/chat/stream")
async def chat_stream(request: ChatRequest):

    async def generate():

        response = ollama.chat(
            model=MODEL,
            messages=[
                {
                    "role": "user",
                    "content": request.message
                }
            ],
            stream=True
        )

        for chunk in response:

            content = chunk["message"]["content"]

            yield content

            await asyncio.sleep(0)

    return StreamingResponse(
        generate(),
        media_type="text/plain"
    )



def process_file(path: str):

    print(f"Processing file: {path}")

    print("File processing completed")


@router.post("/upload")
async def upload_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):

    os.makedirs("uploads", exist_ok=True)

    path = f"uploads/{file.filename}"

    with open(path, "wb") as buffer:
        buffer.write(await file.read())

    background_tasks.add_task(
        process_file,
        path
    )

    return {
        "message": "File uploaded",
        "status": "processing",
        "file": file.filename
    }