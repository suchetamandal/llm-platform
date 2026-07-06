from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "rag-service"
    storage_dir: str = "storage/documents"

    embedding_provider: str = "mock"
    embedding_model: str = "mock-embedding-v1"
    embedding_dimensions: int = 8


settings = Settings()