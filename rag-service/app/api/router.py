from fastapi import APIRouter
from app.api.routes import health, documents, retrieval, rag

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(documents.router,tags=["documents"])
api_router.include_router(retrieval.router)
api_router.include_router(rag.router)