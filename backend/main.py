from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from backend.api import agents, broadcast, proxy, ssh

app = FastAPI(title="Agent Supervisor API")


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    # If the detail is already a dict with "code" and "message", use it directly
    error_content: dict[str, Any]
    if isinstance(exc.detail, dict) and "code" in exc.detail:
        error_content = exc.detail
    else:
        error_content = {
            "code": "INTERNAL_ERROR" if exc.status_code >= 500 else "BAD_REQUEST",
            "message": str(exc.detail),
            "details": {},
        }
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": error_content},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Request body fails schema validation",
                "details": exc.errors(),
            }
        },
    )


app.include_router(agents.router, prefix="/api/agents", tags=["agents"])
app.include_router(proxy.router, prefix="/api/agents", tags=["proxy"])
app.include_router(ssh.router, prefix="/api/agents", tags=["ssh"])
app.include_router(broadcast.router, prefix="/api/broadcast", tags=["broadcast"])
