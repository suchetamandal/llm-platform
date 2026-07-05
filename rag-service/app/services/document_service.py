import uuid
from pathlib import Path

from fastapi import HTTPException, UploadFile

from app.core.config import settings
from app.domain.document import DocumentUploadResponse
from app.providers.mock_embedding_provider import MockEmbeddingProvider
from app.repositories.chunk_repository import ChunkRepository
from app.repositories.document_storage import LocalDocumentStorage
from app.repositories.embedding_repository import EmbeddingRepository
from app.services.embedding_service import EmbeddingService
from app.services.text_extraction_service import TextExtractionService
from app.services.token_chunking_service import TokenChunkingService


class DocumentService:
    def __init__(self):
        self.storage = LocalDocumentStorage(settings.storage_dir)
        self.text_extractor = TextExtractionService()
        self.chunker = TokenChunkingService()
        self.chunk_repository = ChunkRepository()

        self.embedding_service = EmbeddingService(MockEmbeddingProvider())
        self.embedding_repository = EmbeddingRepository()

    async def upload_document(self, file: UploadFile) -> DocumentUploadResponse:
        if not file.filename:
            raise HTTPException(status_code=400, detail="filename is required")

        allowed_types = {
            "application/pdf",
            "text/plain",
        }

        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=400,
                detail=f"unsupported file type: {file.content_type}",
            )

        document_id = str(uuid.uuid4())

        storage_path = await self.storage.save(document_id, file)
        document_dir = Path(storage_path).parent

        extracted_text = self.text_extractor.extract_text(storage_path, file.content_type)

        extracted_path = document_dir / "extracted.txt"
        extracted_path.write_text(extracted_text, encoding="utf-8")

        chunks = self.chunker.chunk(
            document_id=document_id,
            text=extracted_text,
        )

        self.chunk_repository.save_chunks(
            document_dir=document_dir,
            chunks=chunks,
        )

        embeddings = await self.embedding_service.embed_chunks(chunks)

        self.embedding_repository.save_embeddings(
            document_dir=document_dir,
            embeddings=embeddings,
        )

        return DocumentUploadResponse(
            document_id=document_id,
            filename=file.filename,
            content_type=file.content_type,
            storage_path=str(storage_path),
            extracted_text_path=str(extracted_path),
            status="uploaded",
            extracted_chars=len(extracted_text),
            chunk_count=len(chunks),
)