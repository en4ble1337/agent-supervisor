import uuid
from unittest.mock import AsyncMock, patch

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.config import settings
from backend.models.agent import Agent
from backend.services.crypto_service import CryptoService


async def create_ssh_agent(db_session: AsyncSession, *, agent_id: str | None = None) -> str:
    cs = CryptoService(settings.ENCRYPTION_KEY)
    encrypted_pwd = cs.encrypt("password")

    resolved_id = agent_id or str(uuid.uuid4())
    agent = Agent(
        id=resolved_id,
        name="SSH Agent",
        ip_address="10.0.0.1",
        ssh_username="admin",
        ssh_password=encrypted_pwd,
        api_endpoint="http://10",
        business_group="Acme",
    )
    db_session.add(agent)
    await db_session.commit()
    return resolved_id


@pytest.mark.asyncio
@patch("backend.api.ssh.ssh_service.list_directory")
@patch("backend.api.ssh.ssh_service.resolve_workspace_root", new_callable=AsyncMock, create=True)
async def test_get_agent_files_success(
    mock_resolve_workspace, mock_list, async_client: AsyncClient, db_session: AsyncSession
):
    mock_resolve_workspace.return_value = "/home/admin/.hermes/workspaces"
    mock_list.return_value = [{"name": "file1.txt", "type": "file"}]

    agent_id = await create_ssh_agent(db_session)

    response = await async_client.get(f"/api/agents/{agent_id}/files")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "file1.txt"
    mock_resolve_workspace.assert_awaited_once_with("10.0.0.1", "admin", "password")
    mock_list.assert_awaited_once_with("10.0.0.1", "admin", "password", "/home/admin/.hermes/workspaces")


@pytest.mark.asyncio
@patch("backend.api.ssh.ssh_service.list_directory")
@patch("backend.api.ssh.ssh_service.resolve_workspace_root", new_callable=AsyncMock, create=True)
async def test_get_agent_files_resolves_relative_paths_under_workspace(
    mock_resolve_workspace, mock_list, async_client: AsyncClient, db_session: AsyncSession
):
    mock_resolve_workspace.return_value = "/home/admin/.hermes/workspaces"
    mock_list.return_value = []
    agent_id = await create_ssh_agent(db_session)

    response = await async_client.get(f"/api/agents/{agent_id}/files", params={"path": "reports"})

    assert response.status_code == 200
    mock_list.assert_awaited_once_with("10.0.0.1", "admin", "password", "/home/admin/.hermes/workspaces/reports")


@pytest.mark.asyncio
@patch("backend.api.ssh.ssh_service.list_directory")
@patch("backend.api.ssh.ssh_service.resolve_workspace_root", new_callable=AsyncMock, create=True)
async def test_get_agent_files_rejects_traversal(
    mock_resolve_workspace, mock_list, async_client: AsyncClient, db_session: AsyncSession
):
    agent_id = await create_ssh_agent(db_session)

    response = await async_client.get(f"/api/agents/{agent_id}/files", params={"path": "../etc"})

    assert response.status_code == 400
    assert response.json()["error"]["code"] == "VALIDATION_ERROR"
    mock_resolve_workspace.assert_not_called()
    mock_list.assert_not_called()


@pytest.mark.asyncio
@patch("backend.api.ssh.ssh_service.read_file")
@patch("backend.api.ssh.ssh_service.resolve_workspace_root", new_callable=AsyncMock, create=True)
async def test_get_agent_file_content_success(
    mock_resolve_workspace, mock_read, async_client: AsyncClient, db_session: AsyncSession
):
    mock_resolve_workspace.return_value = "/home/admin/.hermes/workspaces"
    mock_read.return_value = "# Daily Notes\nAll systems nominal."
    agent_id = await create_ssh_agent(db_session)

    response = await async_client.get(f"/api/agents/{agent_id}/files/content", params={"path": "notes.md"})

    assert response.status_code == 200
    assert response.json() == {
        "path": "notes.md",
        "content": "# Daily Notes\nAll systems nominal.",
        "encoding": "utf-8",
    }
    mock_read.assert_awaited_once_with("10.0.0.1", "admin", "password", "/home/admin/.hermes/workspaces/notes.md")


@pytest.mark.asyncio
@patch("backend.api.ssh.ssh_service.read_log_file")
@patch("backend.api.ssh.ssh_service.resolve_log_path", new_callable=AsyncMock, create=True)
async def test_get_agent_logs_success(mock_resolve_log, mock_read, async_client: AsyncClient, db_session: AsyncSession):
    mock_resolve_log.return_value = "/home/admin/.hermes/logs/gateway.log"
    mock_read.return_value = "log content"

    agent_id = await create_ssh_agent(db_session)

    response = await async_client.get(f"/api/agents/{agent_id}/logs")

    assert response.status_code == 200
    assert response.json()["logs"] == "log content"
    mock_resolve_log.assert_awaited_once_with("10.0.0.1", "admin", "password")
    mock_read.assert_awaited_once_with("10.0.0.1", "admin", "password", "/home/admin/.hermes/logs/gateway.log", lines=100)


@pytest.mark.asyncio
async def test_ssh_api_not_found(async_client: AsyncClient):
    random_id = str(uuid.uuid4())
    response = await async_client.get(f"/api/agents/{random_id}/files")
    assert response.status_code == 404
