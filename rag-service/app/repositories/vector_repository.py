from sqlalchemy.orm import Session

from app.models.document_chunk import DocumentChunkModel
from app.domain.chunk import DocumentChunk


class VectorRepository:
    def __init__(self, db: Session):
        self.db = db

    def save_chunks(
        self,
        document_id: str,
        chunks: list,
        embeddings: list,
    ) -> None:
        records = []

        for index, (chunk, chunk_embedding) in enumerate(zip(chunks, embeddings)):
            records.append(
                DocumentChunkModel(
                    document_id=document_id,
                    chunk_id=chunk.chunk_id,
                    chunk_index=chunk.chunk_index,
                    text=chunk.text,
                    char_start=chunk.char_start,
                    char_end=chunk.char_end,
                    token_estimate=chunk.token_estimate,
                    embedding=chunk_embedding.embedding,
                )
            )

        self.db.add_all(records)
        self.db.commit()

    def similarity_search(
        self,
        query_embedding: list[float],
        top_k: int = 5,
    ) -> list[DocumentChunk]:
        rows = (
            self.db.query(DocumentChunkModel)
            .order_by(DocumentChunkModel.embedding.cosine_distance(query_embedding))
            .limit(top_k)
            .all()
        )

        return [
            DocumentChunk(
                document_id=row.document_id,
                chunk_id=row.chunk_id,
                chunk_index=row.chunk_index,
                text=row.text,
                char_start=row.char_start,
                char_end=row.char_end,
                token_estimate=row.token_estimate,
            )
            for row in rows
        ]