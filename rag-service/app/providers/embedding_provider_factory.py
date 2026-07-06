from app.core.config import settings
from app.providers.embedding_provider import EmbeddingProvider
from app.providers.mock_embedding_provider import MockEmbeddingProvider
from app.providers.openai_embedding_provider import OpenAIEmbeddingProvider


class EmbeddingProviderFactory:
    @staticmethod
    def create() -> EmbeddingProvider:
        provider = settings.embedding_provider.lower()

        if provider == "mock":
            return MockEmbeddingProvider(
                dimensions=settings.embedding_dimensions or 8,
            )

        if provider == "openai":
            if not settings.openai_api_key:
                raise ValueError("OPENAI_API_KEY is required when EMBEDDING_PROVIDER=openai")

            return OpenAIEmbeddingProvider(
                api_key=settings.openai_api_key,
                model=settings.embedding_model,
                dimensions=settings.embedding_dimensions,
                base_url=settings.openai_base_url,
            )

        raise ValueError(f"unsupported embedding provider: {provider}")