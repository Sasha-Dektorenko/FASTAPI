from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
import logging
from .exceptions import BaseAppException

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

def register_exception_handlers(app: FastAPI):
    @app.exception_handler(BaseAppException)
    async def global_exception_handler(request, exc: BaseAppException):
        logger.exception("Request failed: %s %s", request.method, request.url.path)
        return JSONResponse(
            status_code=exc.status_code if hasattr(exc, 'status_code') else 500,
            content={"detail": exc.message if hasattr(exc, 'message') else "Internal Server Error"},
        )