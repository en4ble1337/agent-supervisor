import multiprocessing
import time
from unittest.mock import patch

import pytest
import uvicorn
from httpx import AsyncClient

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
