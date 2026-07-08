from enum import Enum
from typing import Optional

from pydantic import BaseModel


class DocumentStatus(str, Enum):
    UPLOADED = "UPLOADED"
    PROCESSING = "PROCESSING"
    READY = "READY"
    FAILED = "FAILED"


class DocumentUploadResponse(BaseModel):
    document_id: str
    filename: str
    content_type: str
    status: DocumentStatus


class DocumentStatusResponse(BaseModel):
    document_id: str
    filename: str
    content_type: str
    status: DocumentStatus
    error_message: Optional[str] = None