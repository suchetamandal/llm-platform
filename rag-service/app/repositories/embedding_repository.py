import json
from pathlib import Path

from app.domain.embedding import ChunkEmbedding


class EmbeddingRepository:
    def save_embeddings(
        self,
        document_dir: Path,
        embeddings: list[ChunkEmbedding],
    ) -> Path:
        output_path = document_dir / "embeddings.json"

        data = [embedding.model_dump() for embedding in embeddings]

        output_path.write_text(
            json.dumps(data, indent=2),
            encoding="utf-8",
        )

        return output_path