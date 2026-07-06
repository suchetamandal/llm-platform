from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "rag-service"
    storage_dir: str = "storage/documents"

    openai_api_key: str | None = None
    openai_base_url: str | None = None
    embedding_provider: str = "mock"
    embedding_model: str = "text-embedding-3-small"
    embedding_dimensions: int | None = None


settings = Settings()