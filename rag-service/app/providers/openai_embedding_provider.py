from openai import AsyncOpenAI

from app.providers.embedding_provider import EmbeddingProvider


class OpenAIEmbeddingProvider(EmbeddingProvider):
    def __init__(
        self,
        api_key: str,
        model: str = "text-embedding-3-small",
        dimensions: int | None = None,
        base_url: str | None = None,
    ):
        self.provider = "openai"
        self.model = model
        self.dimensions = dimensions
        self.client = AsyncOpenAI(
            api_key=api_key,
            base_url=base_url,
        )

    async def embed_texts(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []

        kwargs = {
            "model": self.model,
            "input": texts,
        }

        if self.dimensions is not None:
            kwargs["dimensions"] = self.dimensions

        response = await self.client.embeddings.create(**kwargs)

        return [item.embedding for item in response.data]