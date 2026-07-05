from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "rag-service"
    env: str = "dev"
    log_level: str = "INFO"

    storage_dir: str = "storage/documents"
    max_upload_size_mb: int = 25

    class Config:
        env_file = ".env"


settings = Settings()