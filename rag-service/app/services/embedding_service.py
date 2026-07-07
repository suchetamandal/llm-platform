from app.core.config import settings
from app.domain.chunk import DocumentChunk
from app.domain.embedding import ChunkEmbedding
from app.providers.embedding_provider import EmbeddingProvider


class EmbeddingService:
    def __init__(self, provider: EmbeddingProvider):
        self.provider = provider
        self.batch_size = settings.embedding_batch_size

    async def embed_chunks(
        self,
        document_id: str,
        chunks: list[DocumentChunk],
    ) -> list[ChunkEmbedding]:
        embeddings: list[ChunkEmbedding] = []

        for i in range(0, len(chunks), self.batch_size):
            batch = chunks[i : i + self.batch_size]
            texts = [chunk.text for chunk in batch]

            vectors = await self.provider.embed_texts(texts)

            if len(vectors) != len(batch):
                raise ValueError(
                    f"Embedding provider returned {len(vectors)} vectors "
                    f"for {len(batch)} chunks"
                )

            for chunk, vector in zip(batch, vectors):
                embeddings.append(
                    ChunkEmbedding(
                        document_id=document_id,
                        chunk_index=chunk.chunk_index,
                        embedding=vector,
                        provider=settings.embedding_provider,
                        model=self.provider.model,
                    )
                )

        return embeddings

    async def embed_query(self, query: str) -> list[float]:
        vectors = await self.provider.embed_texts([query])

        if len(vectors) != 1:
            raise ValueError(
                f"Embedding provider returned {len(vectors)} vectors for query"
            )

        return vectors[0]