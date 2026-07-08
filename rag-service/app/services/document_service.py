import uuid

from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.domain.document import DocumentStatus, DocumentUploadResponse, DocumentStatusResponse
from app.repositories.document_metadata_repository import DocumentMetadataRepository
from app.providers.embedding_provider_factory import EmbeddingProviderFactory
from app.repositories.vector_repository import VectorRepository
from app.services.chunking_service import ChunkingService
from app.services.embedding_service import EmbeddingService
from app.repositories.document_storage import LocalDocumentStorage
from app.services.text_extraction_service import TextExtractionService
from app.core.config import settings


class DocumentService:
    def __init__(self, db: Session):
        self.storage = LocalDocumentStorage(settings.storage_dir)
        self.text_extractor = TextExtractionService()
        self.chunking_service = ChunkingService()
        embedding_provider = EmbeddingProviderFactory.create()
        self.embedding_service = EmbeddingService(embedding_provider)
        self.vector_repository = VectorRepository(db)
        self.document_metadata_repository = DocumentMetadataRepository(db)

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

        self.document_metadata_repository.create(
            document_id=document_id,
            filename=file.filename,
            content_type=file.content_type,
            storage_path=storage_path,
        )

        return DocumentUploadResponse(
            document_id=document_id,
            filename=file.filename,
            content_type=file.content_type,
            status=DocumentStatus.UPLOADED,
        )

    async def process_document(self, document_id: str) -> None:
        doc = self.document_metadata_repository.get(document_id)

        if doc is None:
            return

        try:
            self.document_metadata_repository.update_status(
                document_id=document_id,
                status=DocumentStatus.PROCESSING,
            )

            extracted_text = self.text_extractor.extract_text(
                doc.storage_path,
                doc.content_type,
            )

            chunks = self.chunking_service.chunk_text(
                document_id=document_id,
                text=extracted_text,
            )

            embeddings = await self.embedding_service.embed_chunks(
                document_id=document_id,
                chunks=chunks,
            )

            self.vector_repository.save_chunks(
                document_id=document_id,
                chunks=chunks,
                embeddings=embeddings,
            )

            self.document_metadata_repository.update_status(
                document_id=document_id,
                status=DocumentStatus.READY,
            )

        except Exception as e:
            self.document_metadata_repository.update_status(
                document_id=document_id,
                status=DocumentStatus.FAILED,
                error_message=str(e),
            )

    def get_document_status(self, document_id: str) -> DocumentStatusResponse:
        doc = self.document_metadata_repository.get(document_id)

        if doc is None:
            raise HTTPException(status_code=404, detail="document not found")

        return DocumentStatusResponse(
            document_id=doc.document_id,
            filename=doc.filename,
            content_type=doc.content_type,
            status=DocumentStatus(doc.status),
            error_message=doc.error_message,
        )