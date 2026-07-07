from pydantic import BaseModel

from app.domain.chunk import DocumentChunk


class RetrievalRequest(BaseModel):
    query: str
    top_k: int = 5


class RetrievalResponse(BaseModel):
    chunks: list[DocumentChunk]