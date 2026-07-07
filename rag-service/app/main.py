from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import settings
from app.middleware.request_id import RequestIDMiddleware
from app.db.init_db import init_db


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        description="Document ingestion and retrieval service for the LLM Platform",
    )

    app.add_middleware(RequestIDMiddleware)
    app.include_router(api_router)

    return app


app = create_app()

@app.on_event("startup")
def on_startup():
    init_db()