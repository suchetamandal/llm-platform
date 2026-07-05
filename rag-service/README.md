## Document Ingestion Pipeline

Upload
    ↓
Validation
    ↓
Local storage
    ↓
Text extraction
    ↓
Chunk generation
    ↓
Chunk persistence

Each uploaded document is stored under:

storage/documents/<document_id>/

Artifacts:
- Original document
- extracted.txt
- chunks.json