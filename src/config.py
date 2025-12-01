from pydantic_settings import BaseSettings, SettingsConfigDict
import os


class Settings(BaseSettings):
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = "gpt-4o-mini"
    chroma_persist_directory: str = "./chroma_db"
    documents_directory: str = "./documents"
    chunk_size: int = 1000
    chunk_overlap: int = 200
    retrieval_top_k: int = 3

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )


settings = Settings()
