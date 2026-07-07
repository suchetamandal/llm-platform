from app.domain.chunk import DocumentChunk


class ContextBuilder:
    def build(self, chunks: list[DocumentChunk]) -> str:
        parts = []

        for chunk in chunks:
            parts.append(
                f"[chunk_id={chunk.chunk_id}]\n{chunk.text}"
            )

        return "\n\n---\n\n".join(parts)