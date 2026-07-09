from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.domain.document import DocumentUploadResponse, DocumentStatusResponse
from app.services.document_service import DocumentService
from app.queues.ingestion_queue import IngestionQueue

router = APIRouter()


@router.post("/v1/documents", response_model=DocumentUploadResponse)
async def upload_document(
    file: UploadFile,
    db: Session = Depends(get_db),
):
    service = DocumentService(db)
    queue = IngestionQueue()

    response = await service.upload_document(file)
    queue.enqueue_document(response.document_id)

    return response

@router.get("/v1/documents/{document_id}", response_model=DocumentStatusResponse)
def get_document_status(
    document_id: str,
    db: Session = Depends(get_db),
):
    service = DocumentService(db)
    return service.get_document_status(document_id)