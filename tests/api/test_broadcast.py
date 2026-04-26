from unittest.mock import patch

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.agent import Agent


@pytest.mark.asyncio
@patch("backend.api.broadcast.broadcast_service.broadcast")
async def test_broadcast_endpoint_business_group(mock_broadcast, async_client: AsyncClient, db_session: AsyncSession):
    mock_broadcast.return_value = {"1": {"status": "success", "reply": "ok"}}

    # Create agents in different groups
    a1 = Agent(
        id="1",
        name="A1",
        ip_address="1",
        ssh_username="u",
        ssh_password="p",
        api_endpoint="http://1",
        business_group="Acme",
    )
    a2 = Agent(
        id="2",
        name="A2",
        ip_address="2",
        ssh_username="u",
        ssh_password="p",
        api_endpoint="http://2",
        business_group="Stark",
    )
    db_session.add_all([a1, a2])
    await db_session.commit()

    payload = {"content": "Hello Acme", "business_group": "Acme"}
    response = await async_client.post("/api/broadcast", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "1" in data
    assert "2" not in data  # Should only target Acme

    # Verify service was called with the right agents
    args, _ = mock_broadcast.call_args
    target_agents = args[0]
    assert len(target_agents) == 1
    assert target_agents[0].id == "1"


@pytest.mark.asyncio
@patch("backend.api.broadcast.broadcast_service.broadcast")
async def test_broadcast_endpoint_ids(mock_broadcast, async_client: AsyncClient, db_session: AsyncSession):
    mock_broadcast.return_value = {"2": {"status": "success", "reply": "ok"}}

    a1 = Agent(
        id="1",
        name="A1",
        ip_address="1",
        ssh_username="u",
        ssh_password="p",
        api_endpoint="http://1",
        business_group="Acme",
    )
    a2 = Agent(
        id="2",
        name="A2",
        ip_address="2",
        ssh_username="u",
        ssh_password="p",
        api_endpoint="http://2",
        business_group="Stark",
    )
    db_session.add_all([a1, a2])
    await db_session.commit()

    payload = {"content": "Hello ID 2", "agent_ids": ["2"]}
    response = await async_client.post("/api/broadcast", json=payload)

    assert response.status_code == 200
    assert "2" in response.json()
    assert "1" not in response.json()
