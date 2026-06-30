"""
main.py
-------
FastAPI application entry point for the AI PDF Chatbot backend.

Phase 1 – FastAPI Foundation:
  * Application factory with lifespan context manager.
  * CORS middleware configured for Unity development.
  * GET /        → welcome message.
  * GET /health  → service health check.
  * Structured logging throughout.
"""

import logging
from contextlib import asynccontextmanager
from datetime import timezone, datetime
from typing import AsyncIterator

import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import get_settings
from app.models import ErrorResponse, HealthResponse, WelcomeResponse
from app.utils import setup_logging, utc_now

# ------------------------------------------------------------------ #
# Bootstrap logging before anything else runs.                        #
# get_settings() is safe to call here because the .env is at the      #
# project root and uvicorn is launched from that same directory.       #
# ------------------------------------------------------------------ #
_settings = get_settings()
setup_logging(_settings.LOG_LEVEL)

logger = logging.getLogger(__name__)


# ============================================================ #
# Lifespan – startup / shutdown hooks                           #
# ============================================================ #

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """
    FastAPI lifespan context manager.

    Code before ``yield`` runs on startup; code after ``yield`` runs on
    shutdown.  Phase 2+ will initialise the PDF index and HTTP client here.
    """
    logger.info(
        "Starting %s v%s | debug=%s",
        _settings.APP_NAME,
        _settings.APP_VERSION,
        _settings.DEBUG,
    )
    logger.info("Allowed CORS origins: %s", _settings.ALLOWED_ORIGINS)

    # ---- Phase 2+ hooks go here ------------------------------------ #
    # e.g. await pdf_reader.init()
    # e.g. openrouter_client = httpx.AsyncClient(...)
    # ---------------------------------------------------------------- #

    yield  # Application is running

    logger.info("Shutting down %s …", _settings.APP_NAME)
    # ---- Phase 2+ cleanup goes here -------------------------------- #
    # e.g. await openrouter_client.aclose()
    # ---------------------------------------------------------------- #


# ============================================================ #
# Application factory                                           #
# ============================================================ #

def create_app() -> FastAPI:
    """
    Construct and configure the FastAPI application.

    Returns:
        Configured FastAPI instance.
    """
    app = FastAPI(
        title=_settings.APP_NAME,
        version=_settings.APP_VERSION,
        description=_settings.APP_DESCRIPTION,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    # ---------------------------------------------------------------- #
    # CORS Middleware                                                    #
    # Allows Unity WebGL builds and the Unity editor to reach the API   #
    # during development.  Tighten allowed_origins before production.   #
    # ---------------------------------------------------------------- #
    app.add_middleware(
        CORSMiddleware,
        allow_origins=_settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["*"],
    )

    # ---------------------------------------------------------------- #
    # Global exception handler                                          #
    # Returns a structured ErrorResponse for any unhandled exception.   #
    # ---------------------------------------------------------------- #
    @app.exception_handler(Exception)
    async def global_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        logger.exception(
            "Unhandled exception on %s %s",
            request.method,
            request.url.path,
        )
        error = ErrorResponse(
            error="internal_server_error",
            detail="An unexpected error occurred. Please try again later.",
            timestamp=utc_now(),
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=error.model_dump(mode="json"),
        )

    # ---------------------------------------------------------------- #
    # Routes                                                            #
    # ---------------------------------------------------------------- #
    _register_routes(app)

    return app


# ============================================================ #
# Route registration                                            #
# ============================================================ #

def _register_routes(app: FastAPI) -> None:
    """Attach all route handlers to *app*."""

    @app.get(
        "/",
        response_model=WelcomeResponse,
        summary="Welcome",
        tags=["General"],
    )
    async def root() -> WelcomeResponse:
        """
        Welcome endpoint.

        Returns a friendly greeting and points consumers to the API docs.
        """
        logger.debug("GET / called")
        return WelcomeResponse(
            message=f"Welcome to the {_settings.APP_NAME} API!",
            version=_settings.APP_VERSION,
            docs_url="/docs",
        )

    @app.get(
        "/health",
        response_model=HealthResponse,
        summary="Health Check",
        tags=["General"],
    )
    async def health_check() -> HealthResponse:
        """
        Health-check endpoint.

        Returns ``{"status": "healthy"}`` together with the current
        application version and a UTC timestamp.  Use this endpoint for
        load-balancer / container orchestration health probes.
        """
        logger.debug("GET /health called")
        return HealthResponse(
            status="healthy",
            version=_settings.APP_VERSION,
            timestamp=utc_now(),
        )


# ============================================================ #
# Application instance (module-level for uvicorn / gunicorn)   #
# ============================================================ #

app: FastAPI = create_app()


# ============================================================ #
# Development entry point                                       #
# ============================================================ #

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=_settings.HOST,
        port=_settings.PORT,
        reload=_settings.DEBUG,
        log_level=_settings.LOG_LEVEL.lower(),
    )
