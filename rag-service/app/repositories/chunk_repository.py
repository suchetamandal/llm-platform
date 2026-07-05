import json
from pathlib import Path

from app.domain.chunk import DocumentChunk


class ChunkRepository:
    def save_chunks(self, document_dir: Path, chunks: list[DocumentChunk]) -> Path:
        output_path = document_dir / "chunks.json"

        with output_path.open("w", encoding="utf-8") as f:
            json.dump(
                [chunk.model_dump() for chunk in chunks],
                f,
                ensure_ascii=False,
                indent=2,
            )

        return output_path

    def load_chunks(self, document_dir: Path) -> list[DocumentChunk]:
        input_path = document_dir / "chunks.json"

        with input_path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        return [DocumentChunk(**item) for item in data]