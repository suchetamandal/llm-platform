from typing import Optional

from sqlalchemy.orm import Session

from app.models.document import DocumentModel
from app.domain.document import DocumentStatus


class DocumentMetadataRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        document_id: str,
        filename: str,
        content_type: str,
        storage_path: str,
    ) -> DocumentModel:
        doc = DocumentModel(
            document_id=document_id,
            filename=filename,
            content_type=content_type,
            storage_path=storage_path,
            status=DocumentStatus.UPLOADED.value,
        )

        self.db.add(doc)
        self.db.commit()
        self.db.refresh(doc)

        return doc

    def get(self, document_id: str) -> Optional[DocumentModel]:
        return (
            self.db.query(DocumentModel)
            .filter(DocumentModel.document_id == document_id)
            .first()
        )

    def update_status(
        self,
        document_id: str,
        status: DocumentStatus,
        error_message: str | None = None,
    ) -> None:
        doc = self.get(document_id)

        if doc is None:
            return

        doc.status = status.value
        doc.error_message = error_message

        self.db.commit()