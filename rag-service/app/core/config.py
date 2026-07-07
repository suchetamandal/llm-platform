from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "rag-service"
    storage_dir: str = "storage/documents"

    embedding_provider: str = "mock"
    embedding_batch_size: int = 32
    embedding_dimension: int = 768

    openai_api_key: str | None = None
    openai_embedding_model: str = "text-embedding-3-small"


    ollama_base_url: str = "http://localhost:11434"
    ollama_embedding_model: str = "nomic-embed-text"
    ollama_chat_model: str = "llama3.1"


    database_url: str = "postgresql+psycopg://llm:llm@localhost:5432/rag"

    class Config:
        env_file = ".env"


settings = Settings()