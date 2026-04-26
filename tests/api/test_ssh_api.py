import uuid
from unittest.mock import patch

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.config import settings
from backend.models.agent import Agent
from backend.services.crypto_service import CryptoService


@pytest.mark.asyncio
@patch("backend.api.ssh.ssh_service.list_directory")
async def test_get_agent_files_success(mock_list, async_client: AsyncClient, db_session: AsyncSession):
    mock_list.return_value = [{"name": "file1.txt", "type": "file"}]

    # Encrypt a dummy password
    cs = CryptoService(settings.ENCRYPTION_KEY)
    encrypted_pwd = cs.encrypt("password")

    agent_id = str(uuid.uuid4())
    agent = Agent(
        id=agent_id,
        name="SSH Agent",
        ip_address="10.0.0.1",
        ssh_username="admin",
        ssh_password=encrypted_pwd,
        api_endpoint="http://10",
        business_group="Acme",
    )
    db_session.add(agent)
    await db_session.commit()

    response = await async_client.get(f"/api/agents/{agent_id}/files?path=/tmp")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "file1.txt"
    mock_list.assert_called_once()


@pytest.mark.asyncio
@patch("backend.api.ssh.ssh_service.read_log_file")
async def test_get_agent_logs_success(mock_read, async_client: AsyncClient, db_session: AsyncSession):
    mock_read.return_value = "log content"

    # Encrypt a dummy password
    cs = CryptoService(settings.ENCRYPTION_KEY)
    encrypted_pwd = cs.encrypt("password")

    agent_id = str(uuid.uuid4())
    agent = Agent(
        id=agent_id,
        name="Log Agent",
        ip_address="10.0.0.2",
        ssh_username="admin",
        ssh_password=encrypted_pwd,
        api_endpoint="http://10",
        business_group="Acme",
    )
    db_session.add(agent)
    await db_session.commit()

    response = await async_client.get(f"/api/agents/{agent_id}/logs")

    assert response.status_code == 200
    assert response.json()["logs"] == "log content"
    mock_read.assert_called_once()


@pytest.mark.asyncio
async def test_ssh_api_not_found(async_client: AsyncClient):
    random_id = str(uuid.uuid4())
    response = await async_client.get(f"/api/agents/{random_id}/files")
    assert response.status_code == 404
