from app.domain.chunk import DocumentChunk
from app.domain.embedding import ChunkEmbedding
from app.providers.embedding_provider import EmbeddingProvider


class EmbeddingService:
    def __init__(self, provider: EmbeddingProvider):
        self.provider = provider

    async def embed_chunks(self, chunks: list[DocumentChunk]) -> list[ChunkEmbedding]:
        texts = [chunk.text for chunk in chunks]

        vectors = await self.provider.embed_texts(texts)

        return [
            ChunkEmbedding(
                document_id=chunk.document_id,
                chunk_index=chunk.chunk_index,
                embedding=vector,
                provider=getattr(self.provider, "provider", "unknown"),
                model=getattr(self.provider, "model", "unknown"),
            )
            for chunk, vector in zip(chunks, vectors)
        ]