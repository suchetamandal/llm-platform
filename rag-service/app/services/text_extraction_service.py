from pathlib import Path

from pypdf import PdfReader


class TextExtractionService:
    def extract_text(self, file_path: str, content_type: str) -> str:
        if content_type == "text/plain":
            return Path(file_path).read_text(encoding="utf-8")

        if content_type == "application/pdf":
            return self._extract_pdf_text(file_path)

        raise ValueError(f"unsupported content type: {content_type}")

    def _extract_pdf_text(self, file_path: str) -> str:
        reader = PdfReader(file_path)

        pages = []
        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            pages.append(f"\n\n--- Page {page_number} ---\n{text}")

        return "\n".join(pages).strip()