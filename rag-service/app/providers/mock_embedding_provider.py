import hashlib
import random

from app.providers.embedding_provider import EmbeddingProvider


class MockEmbeddingProvider(EmbeddingProvider):
    def __init__(self, dimensions: int = 8):
        self.dimensions = dimensions
        self.provider = "mock"
        self.model = "mock-embedding-v1"

    async def embed_texts(self, texts: list[str]) -> list[list[float]]:
        embeddings = []

        for text in texts:
            seed = int(hashlib.md5(text.encode("utf-8")).hexdigest(), 16)
            rng = random.Random(seed)

            vector = [rng.uniform(-1, 1) for _ in range(self.dimensions)]
            embeddings.append(vector)

        return embeddings