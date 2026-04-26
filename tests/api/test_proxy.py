import uuid
from unittest.mock import patch

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.agent import Agent


@pytest.mark.asyncio
async def test_get_agent_status_not_found(async_client: AsyncClient):
    random_id = str(uuid.uuid4())
    response = await async_client.get(f"/api/agents/{random_id}/status")
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "NOT_FOUND"


@pytest.mark.asyncio
@patch("backend.api.proxy.HermesAdapter.get_status")
async def test_get_agent_status_success(mock_get_status, async_client: AsyncClient, db_session: AsyncSession):
    mock_get_status.return_value = {
        "status": "idle",
        "active_tasks": [],
        "cron_jobs": [{"id": "1", "schedule": "0 * * * *"}],
    }

    agent_id = str(uuid.uuid4())
    agent = Agent(
        id=agent_id,
        name="Test Agent",
        ip_address="10.0.0.1",
        ssh_username="admin",
        ssh_password="encrypted_password",
        api_endpoint="http://10.0.0.1:8000",
        business_group="Acme Corp",
    )
    db_session.add(agent)
    await db_session.commit()

    response = await async_client.get(f"/api/agents/{agent_id}/status")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == agent_id
    assert data["status"] == "idle"
    assert len(data["cron_jobs"]) == 1
    mock_get_status.assert_called_once_with("http://10.0.0.1:8000")
