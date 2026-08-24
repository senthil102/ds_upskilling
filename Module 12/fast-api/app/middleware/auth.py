from fastapi import Request
from fastapi.responses import JSONResponse


async def auth_middleware(request: Request, call_next):

    # Allow Swagger
    if request.url.path in [
        "/docs",
        "/openapi.json"
    ]:
        return await call_next(request)

    api_key = request.headers.get("X-API-Key")

    if api_key != "my-secret-key":

        return JSONResponse(
            status_code=401,
            content={
                "error": "Invalid API key"
            }
        )

    return await call_next(request)