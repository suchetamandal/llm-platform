from app.domain.chunk import DocumentChunk


class ChunkingService:
    def __init__(self, chunk_size: int = 1200, chunk_overlap: int = 200):
        if chunk_overlap >= chunk_size:
            raise ValueError("chunk_overlap must be smaller than chunk_size")

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_text(self, document_id: str, text: str) -> list[DocumentChunk]:
        chunks: list[DocumentChunk] = []

        text = text.strip()
        if not text:
            return chunks

        start = 0
        index = 0

        while start < len(text):
            end = min(start + self.chunk_size, len(text))
            chunk_text = text[start:end].strip()

            if chunk_text:
                chunks.append(
                    DocumentChunk(
                        document_id=document_id,
                        chunk_id=f"{document_id}_chunk_{index}",
                        chunk_index=index,
                        text=chunk_text,
                        char_start=start,
                        char_end=end,
                        token_estimate=max(1, len(chunk_text) // 4),
                    )
                )
                index += 1

            if end == len(text):
                break

            start = end - self.chunk_overlap

        return chunks