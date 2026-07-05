from pydantic import BaseModel


class DocumentChunk(BaseModel):
    document_id: str
    chunk_id: str
    chunk_index: int
    text: str
    char_start: int
    char_end: int
    token_estimate: int