from pydantic import BaseModel


class ChunkEmbedding(BaseModel):
    document_id: str
    chunk_index: int
    embedding: list[float]
    provider: str
    model: str