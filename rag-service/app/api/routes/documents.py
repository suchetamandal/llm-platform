from fastapi import APIRouter, File, UploadFile

from app.domain.document import DocumentUploadResponse
from app.services.document_service import DocumentService

router = APIRouter(prefix="/v1/documents", tags=["documents"])

document_service = DocumentService()


@router.post("", response_model=DocumentUploadResponse)
async def upload_document(file: UploadFile = File(...)):
    return await document_service.upload_document(file)