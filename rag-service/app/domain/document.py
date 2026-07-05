from pydantic import BaseModel


class DocumentUploadResponse(BaseModel):
    document_id: str
    filename: str
    content_type: str
    storage_path: str
    extracted_text_path: str
    status: str
    extracted_chars: int