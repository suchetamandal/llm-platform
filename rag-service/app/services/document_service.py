import uuid
from pathlib import Path

from fastapi import HTTPException, UploadFile

from app.core.config import settings
from app.domain.document import DocumentUploadResponse
from app.repositories.chunk_repository import ChunkRepository
from app.repositories.document_storage import LocalDocumentStorage
from app.services.chunking_service import ChunkingService
from app.services.text_extraction_service import TextExtractionService


class DocumentService:
    def __init__(self):
        self.storage = LocalDocumentStorage(settings.storage_dir)
        self.text_extractor = TextExtractionService()
        self.chunking_service = ChunkingService()
        self.chunk_repository = ChunkRepository()

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

        extracted_text = self.text_extractor.extract_text(
            storage_path,
            file.content_type or "application/octet-stream",
        )

        extracted_text_path = self.storage.save_extracted_text(
            document_id,
            extracted_text,
        )

        document_dir = Path(storage_path).parent

        chunks = self.chunking_service.chunk_text(
            document_id=document_id,
            text=extracted_text,
        )

        self.chunk_repository.save_chunks(
            document_dir=document_dir,
            chunks=chunks,
        )

        return DocumentUploadResponse(
            document_id=document_id,
            filename=file.filename,
            content_type=file.content_type or "application/octet-stream",
            storage_path=storage_path,
            extracted_text_path=extracted_text_path,
            status="chunked",
            extracted_chars=len(extracted_text),
            chunk_count=len(chunks),
        )