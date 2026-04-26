import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.config import settings
from backend.core.database import engine, get_db


@pytest.mark.asyncio
async def test_get_db_yields_session():
    # Test that get_db is an async generator yielding an AsyncSession
    gen = get_db()
    session = await anext(gen)

    assert isinstance(session, AsyncSession)

    # Clean up the session
    try:
        await anext(gen)
    except StopAsyncIteration:
        pass


@pytest.mark.asyncio
async def test_database_engine_url():
    # Test that the engine URL matches settings
    # For SQLite, the 'sqlite+aiosqlite' is normalized in SQLAlchemy to some extent
    assert str(engine.url) == settings.DATABASE_URL
