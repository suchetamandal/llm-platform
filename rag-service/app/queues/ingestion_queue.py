import redis

from app.core.config import settings


class IngestionQueue:
    def __init__(self):
        self.client = redis.Redis.from_url(
            settings.redis_url,
            decode_responses=True,
            socket_timeout=10,
            socket_connect_timeout=5,
        )
        self.queue_name = settings.ingestion_queue_name

    def enqueue_document(self, document_id: str) -> None:
        self.client.lpush(self.queue_name, document_id)

    def dequeue_document(self, timeout_seconds: int = 5) -> str | None:
        result = self.client.brpop(
            self.queue_name,
            timeout=timeout_seconds,
        )

        if result is None:
            return None

        _, document_id = result
        return document_id