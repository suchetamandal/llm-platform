from app.core.config import settings
from app.providers.embedding_provider import EmbeddingProvider
from app.providers.mock_embedding_provider import MockEmbeddingProvider
from app.providers.openai_embedding_provider import OpenAIEmbeddingProvider
from app.providers.ollama_embedding_provider import OllamaEmbeddingProvider


class EmbeddingProviderFactory:
    @staticmethod
    def create() -> EmbeddingProvider:
        provider = settings.embedding_provider.lower()

        if provider == "mock":
            return MockEmbeddingProvider()

        if provider == "openai":
            if not settings.openai_api_key:
                raise ValueError("OPENAI_API_KEY is required when EMBEDDING_PROVIDER=openai")

            return OpenAIEmbeddingProvider(
                api_key=settings.openai_api_key,
                model=settings.openai_embedding_model,
            )

        if provider == "ollama":
            return OllamaEmbeddingProvider(
                base_url=settings.ollama_base_url,
                model=settings.ollama_embedding_model,
            )

        raise ValueError(f"Unsupported embedding provider: {settings.embedding_provider}")