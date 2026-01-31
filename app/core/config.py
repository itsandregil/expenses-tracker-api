from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    PROJECT_NAME: str
    API_V1_STR: str = "/api/v1"

    POSTGRES_DATABASE_URI: PostgresDsn


settings = Settings()  # pyright: ignore
