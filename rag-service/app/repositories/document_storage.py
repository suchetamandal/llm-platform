from pathlib import Path

from fastapi import UploadFile


class LocalDocumentStorage:
    def __init__(self, base_dir: str):
        self.base_dir = Path(base_dir)

    async def save(self, document_id: str, file: UploadFile) -> str:
        self.base_dir.mkdir(parents=True, exist_ok=True)

        safe_filename = file.filename or "uploaded_file"
        document_dir = self.base_dir / document_id
        document_dir.mkdir(parents=True, exist_ok=True)

        file_path = document_dir / safe_filename

        with open(file_path, "wb") as out:
            while chunk := await file.read(1024 * 1024):
                out.write(chunk)

        return str(file_path)

    def save_extracted_text(self, document_id: str, text: str) -> str:
        document_dir = self.base_dir / document_id
        document_dir.mkdir(parents=True, exist_ok=True)

        text_path = document_dir / "extracted.txt"
        text_path.write_text(text, encoding="utf-8")

        return str(text_path)