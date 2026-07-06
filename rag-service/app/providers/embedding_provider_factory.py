from app.core.config import settings
from app.providers.embedding_provider import EmbeddingProvider
from app.providers.mock_embedding_provider import MockEmbeddingProvider


class EmbeddingProviderFactory:
    @staticmethod
    def create() -> EmbeddingProvider:
        provider = settings.embedding_provider.lower()

        if provider == "mock":
            return MockEmbeddingProvider(
                dimensions=settings.embedding_dimensions,
            )

        raise ValueError(f"unsupported embedding provider: {provider}")