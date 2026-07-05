import uuid
from fastapi import UploadFile

from app.domain.document import DocumentUploadResponse


class DocumentService:
    async def upload_document(self, file: UploadFile) -> DocumentUploadResponse:
        document_id = str(uuid.uuid4())

        return DocumentUploadResponse(
            document_id=document_id,
            filename=file.filename or "unknown",
            content_type=file.content_type or "application/octet-stream",
            status="uploaded",
        )