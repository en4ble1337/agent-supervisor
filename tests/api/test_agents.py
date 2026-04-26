import logging
from unittest.mock import patch

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from backend.main import app
from backend.models.agent import Agent


@pytest.mark.asyncio
async def test_get_agents_empty(async_client: AsyncClient):
    response = await async_client.get("/api/agents")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_get_agents_with_data(async_client: AsyncClient, db_session: AsyncSession):
    agent1 = Agent(
        name="Agent 1",
        ip_address="10.0.0.1",
        ssh_username="admin",
        ssh_password="pwd",
        api_endpoint="http://10.0.0.1:8000",
        business_group="Acme",
    )
    agent2 = Agent(
        name="Agent 2",
        ip_address="10.0.0.2",
        ssh_username="admin",
        ssh_password="pwd",
        api_endpoint="http://10.0.0.2:8000",
        business_group="Stark",
    )
    db_session.add_all([agent1, agent2])
    await db_session.commit()

    response = await async_client.get("/api/agents")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert "ssh_password" not in data[0]


@pytest.mark.asyncio
async def test_get_agents_filter_by_group(async_client: AsyncClient, db_session: AsyncSession):
    agent1 = Agent(
        name="Agent 1",
        ip_address="10.0.0.1",
        ssh_username="admin",
        ssh_password="pwd",
        api_endpoint="http://10.0.0.1:8000",
        business_group="Acme",
    )
    agent2 = Agent(
        name="Agent 2",
        ip_address="10.0.0.2",
        ssh_username="admin",
        ssh_password="pwd",
        api_endpoint="http://10.0.0.2:8000",
        business_group="Stark",
    )
    db_session.add_all([agent1, agent2])
    await db_session.commit()

    response = await async_client.get("/api/agents?business_group=Acme")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Agent 1"


@pytest.mark.asyncio
@patch("backend.api.agents.ssh_service.validate_connection")
@patch("backend.api.agents.HermesAdapter.validate_endpoint")
async def test_create_agent_success(
    mock_validate_api, mock_validate_ssh, async_client: AsyncClient, db_session: AsyncSession
):
    mock_validate_ssh.return_value = True
    mock_validate_api.return_value = True

    payload = {
        "name": "New Agent",
        "ip_address": "10.0.0.3",
        "ssh_username": "admin",
        "ssh_password": "supersecret",
        "api_endpoint": "http://10.0.0.3:8000",
        "business_group": "Wayne Ent",
    }

    response = await async_client.post("/api/agents", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "New Agent"
    assert "id" in data
    assert "ssh_password" not in data
    mock_validate_ssh.assert_awaited_once_with("10.0.0.3", "admin", "supersecret", raise_on_error=True)


@pytest.mark.asyncio
@patch("backend.api.agents.ssh_service.validate_connection")
async def test_create_agent_ssh_failed(mock_validate_ssh, async_client: AsyncClient):
    mock_validate_ssh.return_value = False

    payload = {
        "name": "Failed Agent",
        "ip_address": "10.0.0.4",
        "ssh_username": "admin",
        "ssh_password": "wrong",
        "api_endpoint": "http://10.0.0.4:8000",
        "business_group": "Wayne Ent",
    }

    response = await async_client.post("/api/agents", json=payload)
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "SSH_AUTH_FAILED"


@pytest.mark.asyncio
@patch("backend.api.agents.ssh_service.validate_connection")
async def test_create_agent_logs_ssh_validation_exception(
    mock_validate_ssh, db_session: AsyncSession, caplog: pytest.LogCaptureFixture
):
    mock_validate_ssh.side_effect = RuntimeError("asyncssh rejected user openclaw")

    payload = {
        "name": "Failed Agent",
        "ip_address": "10.0.0.4",
        "ssh_username": "admin",
        "ssh_password": "wrong-password",
        "api_endpoint": "http://10.0.0.4:8000",
        "business_group": "Wayne Ent",
    }

    async with AsyncClient(
        transport=ASGITransport(app=app, raise_app_exceptions=False),
        base_url="http://test",
    ) as client:
        with caplog.at_level(logging.ERROR, logger="backend.api.agents"):
            response = await client.post("/api/agents", json=payload)

    assert response.status_code == 401
    assert response.json()["error"]["code"] == "SSH_AUTH_FAILED"
    assert "asyncssh rejected user openclaw" in caplog.text
    assert "10.0.0.4" in caplog.text
    assert "wrong-password" not in caplog.text


@pytest.mark.asyncio
@patch("backend.api.agents.ssh_service.validate_connection")
@patch("backend.api.agents.HermesAdapter.validate_endpoint")
async def test_create_agent_api_failed(mock_validate_api, mock_validate_ssh, async_client: AsyncClient):
    mock_validate_ssh.return_value = True
    mock_validate_api.return_value = False

    payload = {
        "name": "Failed API Agent",
        "ip_address": "10.0.0.5",
        "ssh_username": "admin",
        "ssh_password": "password",
        "api_endpoint": "http://10.0.0.5:8000",
        "business_group": "Wayne Ent",
    }

    response = await async_client.post("/api/agents", json=payload)
    assert response.status_code == 502
    assert response.json()["error"]["code"] == "AGENT_UNREACHABLE"
