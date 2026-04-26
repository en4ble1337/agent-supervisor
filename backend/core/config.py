from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ENCRYPTION_KEY: str = Field(..., description="A 32-byte base64 encoded key for Fernet encryption")
    DATABASE_URL: str = Field("sqlite+aiosqlite:///./agent_supervisor.db", description="The SQLite database URL")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()  # type: ignore[call-arg]
