from sqlalchemy import text

from app.db.base import Base
from app.db.session import engine
from app.models.document_chunk import DocumentChunkModel  # noqa: F401


def init_db() -> None:
    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        conn.commit()

    Base.metadata.create_all(bind=engine)