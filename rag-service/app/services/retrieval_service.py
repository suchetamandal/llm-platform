from sqlalchemy.orm import Session

from app.domain.chunk import DocumentChunk
from app.providers.embedding_provider_factory import EmbeddingProviderFactory
from app.repositories.vector_repository import VectorRepository
from app.services.embedding_service import EmbeddingService


class RetrievalService:
    def __init__(self, db: Session):
        provider = EmbeddingProviderFactory.create()
        self.embedding_service = EmbeddingService(provider)
        self.vector_repository = VectorRepository(db)

    async def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[DocumentChunk]:
        query_embedding = await self.embedding_service.embed_query(query)

        return self.vector_repository.similarity_search(
            query_embedding=query_embedding,
            top_k=top_k,
        )