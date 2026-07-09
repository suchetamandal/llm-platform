import asyncio

from app.db.session import SessionLocal
from app.queues.ingestion_queue import IngestionQueue
from app.services.document_service import DocumentService


async def run_worker() -> None:
    queue = IngestionQueue()

    print("Document ingestion worker started")

    while True:
        document_id = queue.dequeue_document(timeout_seconds=5)

        if document_id is None:
            await asyncio.sleep(1)
            continue

        db = SessionLocal()

        try:
            service = DocumentService(db)
            await service.process_document(document_id)
        finally:
            db.close()


if __name__ == "__main__":
    asyncio.run(run_worker())