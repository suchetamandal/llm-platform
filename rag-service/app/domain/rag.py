from pydantic import BaseModel

from app.domain.chunk import DocumentChunk


class RagRequest(BaseModel):
    query: str
    top_k: int = 5


class RagResponse(BaseModel):
    answer: str
    chunks: list[DocumentChunk]