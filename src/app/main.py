"""Application entry point for FastAPI services."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from .api import router as api_router
from .config import get_settings
from .dependencies import ensure_corpus_indexed
from .logging_config import configure_logging
from .workers import SCHEDULER


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle events."""
    # Startup
    ensure_corpus_indexed()
    await SCHEDULER.start()
    yield
    # Shutdown
    await SCHEDULER.stop()


def create_app() -> FastAPI:
    """Instantiate and configure the FastAPI application."""

    configure_logging()
    settings = get_settings()
    app = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
        lifespan=lifespan
    )
    app.include_router(api_router, prefix=settings.api_prefix)

    return app


app = create_app()
