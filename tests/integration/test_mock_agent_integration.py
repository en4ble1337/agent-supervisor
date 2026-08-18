import multiprocessing
import time
from unittest.mock import patch

import pytest
import uvicorn
from httpx import AsyncClient

from backend.services.ssh_service import SSHService
from scripts.mock_agent import DEFAULT_WORKSPACE_ROOT, start_ssh_server
from scripts.mock_agent import app as mock_app


def run_mock_agent():
    uvicorn.run(mock_app, host="127.0.0.1", port=8082)


@pytest.fixture(scope="module")
def mock_agent_process():
    p = multiprocessing.Process(target=run_mock_agent)
    p.start()
    time.sleep(2)  # Wait for startup
    yield
    p.terminate()


@pytest.mark.asyncio
async def test_add_and_query_mock_agent(async_client: AsyncClient, db_session, mock_agent_process):
    # This test verifies that the supervisor can successfully communicate with a running mock agent
    # For SSH, we will still mock validation because starting a real SSH server in a test is flaky

    with patch("backend.api.agents.ssh_service.validate_connection", return_value=True):
        payload = {
            "name": "Integration Mock",
            "ip_address": "127.0.0.1",
            "ssh_username": "agent",
            "ssh_password": "agent_pass",
            "api_endpoint": "http://127.0.0.1:8082",
            "business_group": "Test Group",
        }

        # 1. Add Agent
        add_resp = await async_client.post("/api/agents", json=payload)
        assert add_resp.status_code == 201
        agent_id = add_resp.json()["id"]

        # 2. Get Status (Proxied to mock agent)
        status_resp = await async_client.get(f"/api/agents/{agent_id}/status")
        assert status_resp.status_code == 200
        assert status_resp.json()["status"] == "online"
        assert "Mocking around" in status_resp.json()["active_tasks"][0]["description"]


@pytest.mark.asyncio
async def test_mock_agent_ssh_sftp_supports_validation_listing_and_reading(tmp_path):
    acceptor = await start_ssh_server(host="127.0.0.1", port=0, filesystem_root=tmp_path)
    target = f"127.0.0.1:{acceptor.get_port()}"
    service = SSHService()

    try:
        assert await service.validate_connection(target, "agent", "agent_pass") is True

        files = await service.list_directory(target, "agent", "agent_pass", DEFAULT_WORKSPACE_ROOT)
        assert {"name": "notes.md", "type": "file"} in files
        assert {"name": "reports", "type": "directory"} in files

        content = await service.read_file(target, "agent", "agent_pass", f"{DEFAULT_WORKSPACE_ROOT}/notes.md")
        assert "Mock workspace notes" in content
    finally:
        acceptor.close()
        await acceptor.wait_closed()
