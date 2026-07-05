import tiktoken

from app.domain.chunk import DocumentChunk


class TokenChunkingService:
    def __init__(
        self,
        model_name: str = "text-embedding-3-small",
        chunk_size: int = 500,
        chunk_overlap: int = 75,
    ):
        if chunk_overlap >= chunk_size:
            raise ValueError("chunk_overlap must be smaller than chunk_size")

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        try:
            self.encoding = tiktoken.encoding_for_model(model_name)
        except KeyError:
            self.encoding = tiktoken.get_encoding("cl100k_base")

    def chunk(self, document_id: str, text: str) -> list[DocumentChunk]:
        tokens = self.encoding.encode(text)

        chunks: list[DocumentChunk] = []
        start = 0
        chunk_index = 0

        while start < len(tokens):
            end = min(start + self.chunk_size, len(tokens))
            chunk_tokens = tokens[start:end]
            chunk_text = self.encoding.decode(chunk_tokens)

            char_start = text.find(chunk_text)
            if char_start == -1:
                char_start = 0

            char_end = char_start + len(chunk_text)

            chunks.append(
                DocumentChunk(
                    chunk_id=f"{document_id}:{chunk_index}",
                    document_id=document_id,
                    chunk_index=chunk_index,
                    text=chunk_text,
                    char_start=char_start,
                    char_end=char_end,
                    token_estimate=len(chunk_tokens),
                )
            )

            chunk_index += 1
            start += self.chunk_size - self.chunk_overlap

        return chunks