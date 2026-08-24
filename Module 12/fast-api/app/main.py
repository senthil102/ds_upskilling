from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.middleware.auth import auth_middleware


app = FastAPI(
    title="GenAI FastAPI API",
    version="1.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.middleware("http")
async def authentication(request, call_next):

    return await auth_middleware(
        request,
        call_next
    )


app.include_router(
    router,
    prefix="/api"
)


@app.get("/")
async def root():

    return {
        "message": "GenAI API is running"
    }