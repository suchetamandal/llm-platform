from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile


class DocumentRepository:
    def __init__(self, storage_root: str = "storage/documents"):
        self.storage_root = Path(storage_root)
        self.storage_root.mkdir(parents=True, exist_ok=True)

    def create_document_directory(self) -> tuple[str, Path]:
        """
        Creates a new directory for a document and returns:
        - document_id
        - document directory Path
        """
        document_id = str(uuid4())
        document_dir = self.storage_root / document_id
        document_dir.mkdir(parents=True, exist_ok=True)

        return document_id, document_dir

    async def save_uploaded_file(
        self,
        document_dir: Path,
        file: UploadFile,
    ) -> Path:
        """
        Saves the uploaded file to disk.
        """
        file_path = document_dir / file.filename

        with open(file_path, "wb") as f:
            while chunk := await file.read(1024 * 1024):
                f.write(chunk)

        return file_path

    def save_extracted_text(
        self,
        document_dir: Path,
        text: str,
    ) -> Path:
        """
        Saves extracted text to extracted.txt.
        """
        output_path = document_dir / "extracted.txt"

        output_path.write_text(
            text,
            encoding="utf-8",
        )

        return output_path

    def get_document_directory(self, document_id: str) -> Path:
        """
        Returns the directory for a document.
        """
        return self.storage_root / document_id