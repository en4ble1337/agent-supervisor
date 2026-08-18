import uuid
from unittest.mock import patch

import httpx
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.config import settings
from backend.models.agent import Agent
from backend.services.crypto_service import CryptoService


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


@pytest.mark.asyncio
@patch("backend.api.proxy.ssh_service.collect_runtime_intel")
@patch("backend.api.proxy.HermesAdapter.get_status")
async def test_get_agent_status_includes_ssh_cli_intel(
    mock_get_status, mock_collect_intel, async_client: AsyncClient, db_session: AsyncSession
):
    mock_get_status.return_value = {"status": "ok", "active_tasks": [], "cron_jobs": []}
    mock_collect_intel.return_value = {
        "source": "ssh-cli",
        "sections": [
            {"id": "hermes-status", "title": "Hermes Status", "content": "Gateway Service: running"},
            {"id": "hermes-crons", "title": "Cron Jobs", "content": "No scheduled jobs."},
        ],
    }

    agent_id = str(uuid.uuid4())
    encrypted_password = CryptoService(settings.ENCRYPTION_KEY).encrypt("password")
    agent = Agent(
        id=agent_id,
        name="Hermes Intel Agent",
        ip_address="10.1.20.201",
        ssh_username="transcribo",
        ssh_password=encrypted_password,
        api_endpoint="http://10.1.20.201:8642",
        business_group="Test",
    )
    db_session.add(agent)
    await db_session.commit()

    response = await async_client.get(f"/api/agents/{agent_id}/status")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["intel"]["source"] == "ssh-cli"
    assert data["intel"]["sections"][0]["content"] == "Gateway Service: running"
    mock_collect_intel.assert_awaited_once_with("10.1.20.201", "transcribo", "password")


@pytest.mark.asyncio
@patch("backend.api.proxy.ssh_service.inspect_runtime")
@patch("backend.api.proxy.HermesAdapter.get_status")
async def test_get_agent_status_falls_back_to_ssh_diagnostics_when_api_unreachable(
    mock_get_status, mock_inspect_runtime, async_client: AsyncClient, db_session: AsyncSession
):
    mock_get_status.side_effect = httpx.ConnectError("connection refused")
    mock_inspect_runtime.return_value = {
        "summary": "Hermes gateway process found, but API server is not listening.",
        "processes": ["/home/transcribo/.hermes/hermes-agent/venv/bin/python -m hermes_cli.main gateway run"],
        "listeners": ["0.0.0.0:22"],
        "api_hint": "Enable API_SERVER_ENABLED=true and bind a local API before chat/control will work.",
    }

    agent_id = str(uuid.uuid4())
    encrypted_password = CryptoService(settings.ENCRYPTION_KEY).encrypt("password")
    agent = Agent(
        id=agent_id,
        name="Hermes API Disabled",
        ip_address="10.1.20.201",
        ssh_username="transcribo",
        ssh_password=encrypted_password,
        api_endpoint="http://10.1.20.201:8642",
        business_group="Test",
    )
    db_session.add(agent)
    await db_session.commit()

    response = await async_client.get(f"/api/agents/{agent_id}/status")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "api_unreachable"
    assert data["active_tasks"][0]["id"] == "ssh-diagnostics"
    assert "Hermes gateway process found" in data["active_tasks"][0]["description"]
    mock_inspect_runtime.assert_awaited_once_with("10.1.20.201", "transcribo", "password")
