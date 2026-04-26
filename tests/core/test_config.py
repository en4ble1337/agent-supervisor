import pytest
from pydantic import ValidationError

from backend.core.config import Settings


def test_settings_load_from_env(monkeypatch):
    monkeypatch.setenv("ENCRYPTION_KEY", "test_key_12345678901234567890123")
    monkeypatch.setenv("DATABASE_URL", "sqlite+aiosqlite:///./test.db")

    settings = Settings()

    assert settings.ENCRYPTION_KEY == "test_key_12345678901234567890123"
    assert settings.DATABASE_URL == "sqlite+aiosqlite:///./test.db"


def test_settings_validation_error_missing_key(monkeypatch):
    monkeypatch.delenv("ENCRYPTION_KEY", raising=False)

    with pytest.raises(ValidationError):
        Settings(_env_file=None)
