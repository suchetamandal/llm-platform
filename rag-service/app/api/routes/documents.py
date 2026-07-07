from fastapi import APIRouter, File, UploadFile

from app.domain.document import DocumentUploadResponse
from app.services.document_service import DocumentService
from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.orm import Session

from app.db.dependencies import get_db

router = APIRouter(prefix="/v1/documents", tags=["documents"])


@router.post("", response_model=DocumentUploadResponse)
async def upload_document(file: UploadFile = File(...) , db: Session = Depends(get_db)):
	document_service = DocumentService(db)
	return await document_service.upload_document(file)