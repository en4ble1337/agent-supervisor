import os

# Override the environment variable so that backend imports using settings don't fail
os.environ["ENCRYPTION_KEY"] = "e3GBeQLTet5hxPpq8q1Wfi2z5dqGmR2zWf9hPqDUb5M="

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from backend.core.database import Base, get_db
from backend.main import app

# Centralized Test DB Setup
test_engine = create_async_engine(
    "sqlite+aiosqlite:///:memory:", echo=False, poolclass=StaticPool, connect_args={"check_same_thread": False}
)
TestingSessionLocal = async_sessionmaker(bind=test_engine, class_=AsyncSession, expire_on_commit=False)


async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db


@pytest_asyncio.fixture(scope="function")
async def db_session():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with TestingSessionLocal() as session:
        yield session

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def async_client(db_session):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
