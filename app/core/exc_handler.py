from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
import logging
from .exceptions import BaseAppException
from jwt import PyJWTError
from sqlalchemy.exc import SQLAlchemyError

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

def register_exception_handlers(app: FastAPI):
    @app.exception_handler(BaseAppException)
    async def global_exception_handler(request: Request, exc: BaseAppException):
        logger.exception("Request failed: %s %s", request.method, request.url.path)
        return JSONResponse(
            status_code=exc.status_code if hasattr(exc, 'status_code') else 500,
            content={"detail": exc.message if hasattr(exc, 'message') else "Internal Server Error"},
        )

    @app.exception_handler(PyJWTError)
    async def jwt_exception_handler(request: Request, exc: PyJWTError):
        logger.exception("JWT error: %s %s", request.method, request.url.path)
        return JSONResponse(
            status_code=401,
            content={"detail": "Could not validate credentials"},
        )
    
    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        logger.exception("Unhandled exception: %s %s", request.method, request.url.path)
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal Server Error"},
        )
    
    @app.exception_handler(SQLAlchemyError)
    async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
        import logging
        logger = logging.getLogger("db_errors")
        logger.exception("Database error: %s %s", request.method, request.url.path)

        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error (database)"}
        )